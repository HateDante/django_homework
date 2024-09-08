import datetime
import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student

COURSE_URL = '/api/v1/courses/'


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture()
def student():
    return Student.objects.create(name='Ivanov', birth_date=datetime.date(1995, 1, 1))


@pytest.fixture()
def course(student):
    course = student.course_set.create(name='course 1')
    return course


@pytest.mark.django_db
def test_create_course(client, student):
    count = Course.objects.count()
    new_data = {
        'name': 'course 1',
        'students': [student.id, ]
    }
    response = client.post(COURSE_URL, data=new_data)
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course):
    new_data = {
        'name': 'course 2',
    }
    response = client.patch(f'{COURSE_URL}{course.id}/', data=new_data)
    assert response.status_code == 200
    data = Course.objects.get(id=course.id)
    assert data.name == new_data['name']


@pytest.mark.django_db
def test_delete_course(client, course):
    new_data = {
        'id': course.id,
    }
    response = client.delete(f'{COURSE_URL}{course.id}/', data=new_data)
    assert response.status_code == 204
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get(COURSE_URL, data={'id': courses[0].id})
    assert response.status_code == 200
    data = response.json()
    assert courses[0].name == data[0]['name']


@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(COURSE_URL)
    assert response.status_code == 200
    data = response.json()
    for i, current_course in enumerate(data):
        assert courses[i].name == current_course['name']


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = 5
    response = client.get(COURSE_URL, data={'id': courses[course_id].id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert courses[course_id].id == data[0]['id']


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = 3
    response = client.get(COURSE_URL, data={'name': courses[course_id].name})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert courses[course_id].name == data[0]['name']
