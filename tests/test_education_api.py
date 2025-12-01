from education.models import Course, Lesson
import pytest 
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

User = get_user_model()

# Fixtures

@pytest.fixture
def user(db):
    return User.objects.create_user(username='user1', email='user1@example.com', password='pass1234')

@pytest.fixture
def other_user(db):
    return User.objects.create_user(username='user2', email='user2@example.com', password='pass1234')

@pytest.fixture
def api_client():
    return APIClient()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

@pytest.fixture
def auth_client(api_client, user):
    tokens = get_tokens_for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    return api_client

@pytest.fixture
def auth_client_other(api_client, other_user):
    tokens = get_tokens_for_user(other_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    return api_client

# JWT Auth Test

@pytest.mark.django_db
def test_jwt_token_obtain_good(api_client, user):
    url = reverse('token_obtain_pair')
    resp = api_client.post(url, {'email': user.email, 'password': 'pass1234'}, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data and 'refresh' in resp.data
    
@pytest.mark.django_db
def test_jwt_token_obtain_bad(api_client):
    url = reverse('token_obtain_pair')
    resp = api_client.post(url, {'email': 'wrong', 'password': 'wrong'}, format='json')
    assert resp.status_code == 401
    
@pytest.mark.django_db
def test_jwt_token_refresh_good(api_client, user):
    tokens = get_tokens_for_user(user)
    url = reverse('token_refresh')
    resp = api_client.post(url, {'refresh': tokens['refresh']}, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data

@pytest.mark.django_db
def test_jwt_token_refresh_bad(api_client):
    url = reverse('token_refresh')
    resp = api_client.post(url, {'refresh': 'fake_token'}, format='json')
    assert resp.status_code == 401
    
#Course tests

@pytest.mark.django_db
def test_create_course_good(auth_client, user):
    url = reverse('course-list')
    resp = auth_client.post(url, {'title': 'C1', 'description': 'desc'}, format='json')
    assert resp.status_code == 201
    assert resp.data['title'] == 'C1'
    
@pytest.mark.django_db
def test_create_course_bad_missing_title(auth_client):
    url = reverse('course-list')
    resp = auth_client.post(url, {'description': 'desc'}, format='json')
    assert resp.status_code == 400

@pytest.mark.django_db
def test_list_courses_good(auth_client, user):
    Course.objects.create(title='A', owner=user)
    Course.objects.create(title='B', owner=user, is_active=False)
    url = reverse('course-list')
    resp = auth_client.get(url)
    assert resp.status_code == 200
    assert isinstance(resp.data, list)

@pytest.mark.django_db
def test_retrieve_course_good(auth_client, user):
    c = Course.objects.create(title='R', owner=user)
    url = reverse('course-detail', kwargs={'pk': c.id})
    resp = auth_client.get(url)
    assert resp.status_code == 200
    
@pytest.mark.django_db
def test_retrieve_course_bad_not_found(auth_client):
    url = reverse('course-detail', kwargs={'pk': 9999})
    resp = auth_client.get(url)
    assert resp.status_code == 404
    
@pytest.mark.django_db
def test_update_course_good(auth_client, user):
    c = Course.objects.create(title='Old', owner=user)
    url = reverse('course-detail', kwargs={'pk': c.id})
    resp = auth_client.put(url, {'title': 'New', 'description': 'd'}, format='json')
    assert resp.status_code == 200
    assert resp.data['title'] == 'New'

@pytest.mark.django_db
def test_update_course_bad_not_owner(auth_client_other, user):
    c = Course.objects.create(title='Old', owner=user)
    url = reverse('course-detail', kwargs={'pk': c.id})
    resp = auth_client_other.put(url, {'title': 'New', 'description': 'd'}, format='json')
    assert resp.status_code == 403

@pytest.mark.django_db
def test_update_course_bad_not_owner(auth_client_other, user):
    c = Course.objects.create(title='Old', owner=user)
    url = reverse('course-detail', kwargs={'pk': c.id})
    resp = auth_client_other.put(url, {'title': 'New', 'description': 'd'}, format='json')
    assert resp.status_code == 403

@pytest.mark.django_db
def test_delete_course_bad_not_owner(auth_client_other, user):
    c = Course.objects.create(title='ToDel', owner=user)
    url = reverse('course-detail', kwargs={'pk': c.id})
    resp = auth_client_other.delete(url)
    assert resp.status_code == 403

@pytest.mark.django_db
def test_activate_deactivate_good(auth_client, user):
    c = Course.objects.create(title='T', owner=user, is_active=False)
    url = reverse('course-activate', kwargs={'pk': c.id})
    resp = auth_client.post(url)
    assert resp.data['is_active'] is True

    url2 = reverse('course-deactivate', kwargs={'pk': c.id})
    resp = auth_client.post(url2)
    assert resp.data['is_active'] is False

@pytest.mark.django_db
def test_activate_course_bad_already_active(auth_client, user):
    c = Course.objects.create(title='T', owner=user, is_active=True)
    url = reverse('course-activate', kwargs={'pk': c.id})
    resp = auth_client.post(url)
    assert resp.status_code == 400


@pytest.mark.django_db
def test_course_lessons_list_good(auth_client, user):
    c = Course.objects.create(title='C', owner=user)
    Lesson.objects.create(course=c, title='L1', content='x', owner=user, order=1)
    Lesson.objects.create(course=c, title='L2', content='x', owner=user, order=2)
    url = reverse('course-lessons', kwargs={'pk': c.id})
    resp = auth_client.get(url)
    assert len(resp.data) == 2

@pytest.mark.django_db
def test_course_lessons_list_bad_course(auth_client):
    url = reverse('course-lessons', kwargs={'pk': 9999})
    resp = auth_client.get(url)
    assert resp.status_code == 404
    
# Lesson tests

@pytest.mark.django_db
def test_create_lesson_good(auth_client, user):
    c = Course.objects.create(title='C', owner=user)
    url = reverse('lesson-create')
    data = {
        'title': 'L',
        'content': 'Some lesson content',
        'course': c.id,
        'owner': user.id 
    }

    resp = auth_client.post(url, data, format='json')
    print(resp.status_code)
    print(resp.json())
    assert resp.status_code == 201
    
@pytest.mark.django_db
def test_create_lesson_bad_not_owner(auth_client_other, user):
    c = Course.objects.create(title='C', owner=user)
    url = reverse('lesson-create')
    resp = auth_client_other.post(url, {'title': 'L', 'content': 'x', 'course': c.id}, format='json')
    assert resp.status_code == 403
    
@pytest.mark.django_db
def test_move_lesson_good(auth_client, user):
    c = Course.objects.create(title='C', owner=user)
    l1 = Lesson.objects.create(course=c, title='A', content='x', owner=user, order=1)
    l2 = Lesson.objects.create(course=c, title='B', content='x', owner=user, order=2)
    url = reverse('lesson-move', kwargs={'pk': l2.id})
    resp = auth_client.put(url, {'before_lesson_id': l1.id}, format='json')
    assert resp.status_code == 200
    assert resp.data['order'] is not None
    
@pytest.mark.django_db
def test_move_lesson_bad_foreign_course(auth_client, user, other_user):
    c1 = Course.objects.create(title='C1', owner=user)
    c2 = Course.objects.create(title='C2', owner=other_user)
    l1 = Lesson.objects.create(course=c1, title='A', content='x', owner=user, order=1)
    l2 = Lesson.objects.create(course=c2, title='B', content='x', owner=other_user, order=1)
    url = reverse('lesson-move', kwargs={'pk': l1.id})
    resp = auth_client.put(url, {'before_lesson_id': l2.id}, format='json')
    assert resp.status_code == 400
    
@pytest.mark.django_db
def test_delete_lesson_good(auth_client, user):
    c = Course.objects.create(title='C', owner=user)
    l = Lesson.objects.create(course=c, title='L', content='x', owner=user, order=1)
    url = reverse('lesson-detail', kwargs={'pk': l.id})
    resp = auth_client.delete(url)
    assert resp.status_code == 204
    assert Lesson.objects.filter(id=l.id, deleted_at__isnull=False).exists()
    
@pytest.mark.django_db
def test_delete_lesson_bad_not_owner(auth_client_other, user):
    c = Course.objects.create(title='C', owner=user)
    l = Lesson.objects.create(course=c, title='L', content='x', owner=user, order=1)
    url = reverse('lesson-detail', kwargs={'pk': l.id})
    resp = auth_client_other.delete(url)
    assert resp.status_code == 403

@pytest.mark.django_db
def test_publish_unpublish_good(auth_client, user):
    c = Course.objects.create(title='C', owner=user)
    l = Lesson.objects.create(course=c, title='L', content='x', owner=user, order=1, is_published=False)
    url_pub = reverse('lesson-publish', kwargs={'pk': l.id})
    resp = auth_client.post(url_pub)
    assert resp.data['is_published'] is True

    url_un = reverse('lesson-unpublish', kwargs={'pk': l.id})
    resp = auth_client.post(url_un)
    assert resp.data['is_published'] is False

@pytest.mark.django_db
def test_publish_unpublish_bad_not_owner(auth_client_other, user):
    c = Course.objects.create(title='C', owner=user)
    l = Lesson.objects.create(course=c, title='L', content='x', owner=user, order=1, is_published=False)
    url_pub = reverse('lesson-publish', kwargs={'pk': l.id})
    resp = auth_client_other.post(url_pub)
    assert resp.status_code == 403