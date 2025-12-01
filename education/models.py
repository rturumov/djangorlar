from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings
from abstracts.models import AbstractSoftDeletableModel

class Course(AbstractSoftDeletableModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_courses"
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def lessons_count(self):
        return self.lessons.filter(deleted_at__isnull=True).count()
    
class Lesson(AbstractSoftDeletableModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    order = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    indentation = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])
    
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_courses"
    )
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.order} | {self.title}"