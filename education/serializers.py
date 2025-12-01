from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Lesson
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = fields 


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def validate_course(self, course):
        user = self.context['request'].user
        if self.instance is None:
            if course.owner != user:
                raise PermissionDenied("You are not the owner of this course")
        return course
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        
        course = validated_data['course']
        if 'order' not in validated_data or validated_data['order'] == 0:
            last_lesson = Lesson.objects.filter(
                course=course,
                deleted_at__isnull=True
            ).order_by('-order').first()
            
            if last_lesson:
                validated_data['order'] = last_lesson.order + 1.0
            else:
                validated_data['order'] = 1.0
        
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    owner = UserInfoSerializer(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'is_active', 'owner',
            'lessons_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'lessons_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CourseDetailSerializer(CourseSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['lessons']


class LessonMoveSerializer(serializers.Serializer):
    before_lesson_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_before_lesson_id(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("ID урока должен быть положительным числом.")
        return value