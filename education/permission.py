from rest_framework import permissions

class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'course'):
            return obj.course.owner == request.user
        
        return obj.owner == request.user
    
class IsAuthenticatedAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
      
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False