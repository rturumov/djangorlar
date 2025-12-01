from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    LessonSerializer,
    LessonMoveSerializer
)
from .models import Course, Lesson


class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(deleted_at__isnull=True)

    def get_course_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    def list(self, request):
        queryset = self.get_queryset()

        is_active_param = request.query_params.get('is_active')
        if is_active_param is not None:
            if is_active_param.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active_param.lower() == 'false':
                queryset = queryset.filter(is_active=False)

        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = self.get_course_object(pk)
        serializer = CourseDetailSerializer(course, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        course = self.get_course_object(pk)

        if course.owner != request.user:
            return Response(
                {'detail': 'У вас нет прав для изменения этого курса.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourseSerializer(course, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        course = self.get_course_object(pk)

        if course.owner != request.user:
            return Response(
                {'detail': 'У вас нет прав для удаления этого курса.'},
                status=status.HTTP_403_FORBIDDEN
            )

        course.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        course = self.get_course_object(pk)

        if course.owner != request.user:
            return Response(
                {'detail': 'У вас нет прав для активации этого курса.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if course.is_active:
            return Response(
                {'detail': 'Курс уже активен.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course.is_active = True
        course.save()
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        course = self.get_course_object(pk)

        if course.owner != request.user:
            return Response(
                {'detail': 'У вас нет прав для деактивации этого курса.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not course.is_active:
            return Response(
                {'detail': 'Курс уже неактивен.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course.is_active = False
        course.save()
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = self.get_course_object(pk)
        lessons = course.lessons.filter(deleted_at__isnull=True)
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if course.owner != self.request.user:
            raise PermissionDenied("У вас нет прав для добавления урока в этот курс.")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this lesson")
        instance.delete()

    def get_lesson_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    @action(detail=True, methods=['put'])
    def move(self, request, pk=None):
        lesson = self.get_lesson_object(pk)

        if lesson.course.owner != request.user:
            return Response(
                {'detail': 'У вас нет прав для перемещения этого урока.'},
                status=status.HTTP_403_FORBIDDEN
            )

        move_serializer = LessonMoveSerializer(data=request.data)
        if not move_serializer.is_valid():
            return Response(move_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        before_lesson_id = move_serializer.validated_data.get('before_lesson_id')

        try:
            with transaction.atomic():
                original_order = lesson.order
                lesson.order = Decimal('-99999.0')
                lesson.save()

                if before_lesson_id is not None:
                    before_lesson = Lesson.objects.filter(
                        id=before_lesson_id,
                        course=lesson.course,
                        deleted_at__isnull=True
                    ).first()
                    if not before_lesson:
                        lesson.order = original_order
                        lesson.save()
                        return Response(
                            {'detail': 'Урок для вставки не найден или принадлежит другому курсу.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    lessons_to_update = Lesson.objects.filter(
                        course=lesson.course,
                        deleted_at__isnull=True,
                        order__gte=before_lesson.order
                    ).exclude(id=lesson.id).order_by('-order')

                    for l in lessons_to_update:
                        l.order = Decimal(l.order) + Decimal('1.0')
                        l.save()

                    lesson.order = Decimal(before_lesson.order)
                    lesson.indentation = min(getattr(before_lesson, 'indentation', 0), 5)
                    lesson.save()
                else:
                    last = Lesson.objects.filter(
                        course=lesson.course,
                        deleted_at__isnull=True
                    ).exclude(id=lesson.id).order_by('-order').first()
                    lesson.order = Decimal(last.order + 1 if last else 1)
                    lesson.indentation = 0
                    lesson.save()

                return Response({'order': str(lesson.order), 'indentation': lesson.indentation})
        except Exception as e:
            return Response({'detail': 'Ошибка при перемещении урока.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        lesson = self.get_lesson_object(pk)

        if lesson.course.owner != request.user:
            return Response({'detail': 'У вас нет прав для публикации этого урока.'}, status=status.HTTP_403_FORBIDDEN)

        if lesson.is_published:
            return Response({'detail': 'Урок уже опубликован.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson.is_published = True
        lesson.save()
        return Response(LessonSerializer(lesson, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        lesson = self.get_lesson_object(pk)

        if lesson.course.owner != request.user:
            return Response({'detail': 'У вас нет прав для снятия публикации этого урока.'}, status=status.HTTP_403_FORBIDDEN)

        if not lesson.is_published:
            return Response({'detail': 'Урок уже не опубликован.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson.is_published = False
        lesson.save()
        return Response(LessonSerializer(lesson, context={'request': request}).data)