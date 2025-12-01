from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from os import path
from django.urls import path
from education.views import CourseViewSet, LessonViewSet


course_list = CourseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

course_detail = CourseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

course_activate = CourseViewSet.as_view({'post': 'activate'})
course_deactivate = CourseViewSet.as_view({'post': 'deactivate'})
course_lessons = CourseViewSet.as_view({'get': 'lessons'})

lesson_create = LessonViewSet.as_view({'post': 'create'})
lesson_move = LessonViewSet.as_view({'put': 'move'})
lesson_detail = LessonViewSet.as_view({'delete': 'destroy'})
lesson_publish = LessonViewSet.as_view({'post': 'publish'})
lesson_unpublish = LessonViewSet.as_view({'post': 'unpublish'})

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/education/courses/', course_list, name='course-list'),
    path('api/v1/education/courses/<int:pk>/', course_detail, name='course-detail'),
    path('api/v1/education/courses/<int:pk>/activate/', course_activate, name='course-activate'),
    path('api/v1/education/courses/<int:pk>/deactivate/', course_deactivate, name='course-deactivate'),
    path('api/v1/education/courses/<int:pk>/lessons/', course_lessons, name='course-lessons'),
    
    path('api/v1/education/lessons/', lesson_create, name='lesson-create'),
    path('api/v1/education/lessons/<int:pk>/move/', lesson_move, name='lesson-move'),
    path('api/v1/education/lessons/<int:pk>/', lesson_detail, name='lesson-detail'),
    path('api/v1/education/lessons/<int:pk>/publish/', lesson_publish, name='lesson-publish'),
    path('api/v1/education/lessons/<int:pk>/unpublish/', lesson_unpublish, name='lesson-unpublish'),
]