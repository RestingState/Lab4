import pytest
from src.main import app, session
from src.database_model import engine, metadata, Major, Subject, Mark, Student

user_good_1 = {
    "full_name": "Augustin Porebryk",
    "login": "augus",
    "password": "qwe123QWE",
    "email": "ag@gmail.com"
}
user_good_2 = {
    "full_name": "asda asdaf",
    "login": "lavan",
    "password": "qwe123qwe",
    "email": "aasdsg@gmail.com"
}
user_update_good = {
    "full_name": "Augustin Porebryk",
    "login": "augustin",
    "password": "qweqweqwe",
    "email": "ag@gmail.com"
}
user_update_bad_1 = {
    "full_name": "Augustin Porebryk",
    "login": "aaa",
    "password": "qweqweqwe",
    "email": "ag@gmail.com"
}
user_update_bad_2 = {
    "full_name": "Augustin Porebryk",
    "login": "lavan",
    "password": "qweqweqwe",
    "email": "ag@gmail.com"
}
user_bad = {
    "full_name": "Augustin Porebryk",
    "login": "augu",
    "password": "qwe123QWE",
    "email": "ag@gmail.com"
}
auth_good_1 = {
    "Authorization": "Basic YXVndXM6cXdlMTIzUVdF"
}
auth_good_2 = {
    "Authorization": "Basic bGF2YW46cXdlMTIzcXdl"
}
auth_bad = {
    "Authorization": "Basic bGF2YW46cXdlMsIzcXdl"
}
student_good = {
    "name": "TestSubj",
    "major": {"name": "Physics"},
    "rating": 16,
    "marks": [{"subject": {"name": "Applied Programming"}, "grade": 15}]
}
student_bad = {
    "name": "TestSubj",
    "major": {"name": "Math"},
    "rating": 16,
    "marks": []
}
student_bad_2 = {
    "name": "TestSubj",
    "rating": 16,
    "marks": []
}
student_bad_3 = {
    "name": "TestSubj",
    "major": {"name": "Physics"},
    "rating": 16,
    "marks": [{"subject": {"name": "test"}, "grade": 15}]
}
student_update_good = {
    "name": "Updated",
    "major": {"name": "Physics"},
    "rating": 25,
    "marks": [{"subject": {"name": "Applied Programming"}, "grade": 15}]
}
student_update_bad_1 = {
    "name": "Updated",
    "major": {"name": "Math"},
    "rating": 25,
    "marks": [{"subject": {"name": "Applied Programming"}, "grade": 15}]
}
student_update_bad_2 = {
    "name": "Updated",
    "major": {"name": "Math"},
    "rating": 25,
    "marks": [{"subject": {"name": "Test"}, "grade": 15}]
}
student_update_bad_3 = {
    "name": "Updated",
    "major": 0,
    "rating": 25,
    "marks": [{"subject": {"name": "Test"}, "grade": 15}]
}


@pytest.fixture
def client():
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield app.test_client()
    session.close()


@pytest.fixture
def client_with_user_1(client):
    client.post('/user', json=user_good_1)
    return client


@pytest.fixture
def client_with_both_users(client):
    client.post('/user', json=user_good_1)
    client.post('/user', json=user_good_2)
    return client


@pytest.fixture
def full_set_client(client):
    client.post('/user', json=user_good_1)
    client.post('/user', json=user_good_2)

    major = Major(name='Physics')
    session.add(major)
    session.flush()

    subject1 = Subject(name='Applied Programming')
    subject2 = Subject(name='Quantum Physics')
    session.add(subject1)
    session.add(subject2)
    session.flush()

    student1 = Student(name='Yurii Stebelskij', major_id=major.id, rating=100)
    student2 = Student(name='Alex', major_id=major.id, rating=4)
    session.add(student1)
    session.add(student2)
    session.flush()

    mark1 = Mark(student_id=student1.id, subject_id=subject2.id, grade=42)
    mark2 = Mark(student_id=student2.id, subject_id=subject2.id, grade=64)
    mark3 = Mark(student_id=student2.id, subject_id=subject1.id, grade=2)
    session.add(mark1)
    session.add(mark2)
    session.add(mark3)
    session.flush()

    return client


def test_root(client):
    response = client.get('/')
    assert response.status_code == 404


def test_user_creation_valid(client):
    response = client.post('/user', json=user_good_1)
    assert response.status_code == 200


def test_user_creation_invalid(client):
    # Check validation error
    response = client.post('/user', json=user_bad)
    assert response.status_code == 400
    # Check integrity error
    client.post('/user', json=user_good_1)
    response = client.post('/user', json=user_good_1)
    assert response.status_code == 403


def test_user_login_valid(client_with_user_1):
    response = client_with_user_1.get('/user/login', headers=auth_good_1)
    assert response.status_code == 200


def test_user_login_invalid(client_with_user_1):
    response = client_with_user_1.get('/user/login', headers=auth_good_2)
    assert response.status_code == 401


def test_get_user_info_valid(client_with_user_1):
    lg = user_good_1['login']
    response = client_with_user_1.get(
        f'/user/{lg}', headers=auth_good_1)
    assert response.status_code == 200
    assert response.data == b'\n      full_name = Augustin Porebryk; \n      login = augus; \n      email = ag@gmail.com; \n      '


def test_get_user_info_invalid(client_with_user_1):
    # URL validation error (login can't exist)
    response = client_with_user_1.get('/user/a', headers=auth_good_1)
    assert response.status_code == 400
    # Auth fail
    lg = user_good_1['login']
    response = client_with_user_1.get(
        f'/user/{lg}', headers=auth_good_2)
    assert response.status_code == 401
    # No user
    lg = 'not_existing'
    response = client_with_user_1.get(
        f'/user/{lg}', headers=auth_good_1)
    assert response.status_code == 404


def test_put_user_valid(client_with_user_1):
    lg = user_good_1['login']
    response = client_with_user_1.put(
        f'/user/{lg}', json=user_update_good, headers=auth_good_1)
    assert response.status_code == 200


def test_put_user_invalid(client_with_both_users):
    lg = user_good_1['login']
    # Bad auth
    response = client_with_both_users.put(
        f'/user/{lg}', json=user_update_good, headers=auth_bad)
    assert response.status_code == 401
    # Bad update #1
    response = client_with_both_users.put(
        f'/user/{lg}', json=user_update_bad_1, headers=auth_good_1)
    assert response.status_code == 400
    # Bad update #2
    response = client_with_both_users.put(
        f'/user/{lg}', json=user_update_bad_2, headers=auth_good_1)
    assert response.status_code == 403
    # Different user
    response = client_with_both_users.put(
        f'/user/{lg}', json=user_update_good, headers=auth_good_2)
    assert response.status_code == 400


def test_delete_user_valid(client_with_user_1):
    lg = user_good_1['login']
    response = client_with_user_1.delete(f'/user/{lg}', headers=auth_good_1)
    assert response.status_code == 200


def test_delete_user_invalid(client_with_both_users):
    lg = user_good_1['login']
    # Failed auth
    response = client_with_both_users.delete(f'/user/{lg}', headers=auth_bad)
    assert response.status_code == 401
    # Different user access
    response = client_with_both_users.delete(
        f'/user/{lg}', headers=auth_good_2)
    assert response.status_code == 400
    # Validate login fail
    response = client_with_both_users.delete(
        f'/user/aa', headers=auth_good_1)
    assert response.status_code == 400


def test_student_add_valid(full_set_client):
    response = full_set_client.post(
        '/student', json=student_good, headers=auth_good_1)
    assert response.status_code == 200


def test_student_add_invalid(full_set_client):
    # Server error - bad request
    response = full_set_client.post(
        '/student', headers=auth_good_1)
    assert response.status_code == 500
    # Bad auth
    response = full_set_client.post(
        '/student', json=student_good, headers=auth_bad)
    assert response.status_code == 401
    # Bad data
    response = full_set_client.post(
        '/student', json=student_bad, headers=auth_good_1)
    assert response.status_code == 500
    # Bad data x2
    response = full_set_client.post(
        '/student', json=student_bad_2, headers=auth_good_1)
    assert response.status_code == 400
    # Bad data x3
    response = full_set_client.post(
        '/student', json=student_bad_3, headers=auth_good_1)
    assert response.status_code == 500


def test_student_get_info_valid(full_set_client):
    response = full_set_client.get('/student/1', headers=auth_good_1)
    assert response.status_code == 200


def test_student_get_info_invalid(full_set_client):
    # Bad auth
    response = full_set_client.get('/student/1', headers=auth_bad)
    assert response.status_code == 401
    # Bad url
    response = full_set_client.get('/student/dzuske', headers=auth_good_1)
    assert response.status_code == 400
    # Student don't exist
    response = full_set_client.get('/student/15', headers=auth_good_1)
    assert response.status_code == 404


def test_student_put_valid(full_set_client):
    response = full_set_client.put(
        '/student/1', json=student_update_good, headers=auth_good_1)
    assert response.status_code == 200


def test_student_put_invalid(full_set_client):
    # Bad auth
    response = full_set_client.put(
        '/student/1', json=student_update_good, headers=auth_bad)
    assert response.status_code == 401
    # Bad data x1
    response = full_set_client.put(
        '/student/1', json=student_update_bad_1, headers=auth_good_1)
    assert response.status_code == 404
    # Bad data x2
    response = full_set_client.put(
        '/student/1', json=student_update_bad_2, headers=auth_good_1)
    assert response.status_code == 404
    # Bad data x3
    response = full_set_client.put(
        '/student/1', json=student_update_bad_3, headers=auth_good_1)
    assert response.status_code == 400
    # No student
    response = full_set_client.put(
        '/student/15', json=student_update_good, headers=auth_good_1)
    assert response.status_code == 404


def test_delete_student_valid(full_set_client):
    response = full_set_client.delete(f'/student/1', headers=auth_good_1)
    assert response.status_code == 200


def test_delete_student_invalid(full_set_client):
    # Failed auth
    response = full_set_client.delete(f'/student/1', headers=auth_bad)
    assert response.status_code == 401
    # Bad url
    response = full_set_client.delete('/student/dzuske', headers=auth_good_1)
    assert response.status_code == 400
    # Bad url x2
    response = full_set_client.delete('/student/4', headers=auth_good_1)
    assert response.status_code == 404


def test_uni_top_valid(full_set_client):
    # Normal ammount of students
    response = full_set_client.get('/university/2')
    assert response.status_code == 200
    # Too many students
    response = full_set_client.get('/university/3')
    assert response.status_code == 200


def test_uni_top_invalid(full_set_client):
    # Bad url value
    response = full_set_client.get('/university/dzuske')
    assert response.status_code == 404
    response = full_set_client.get('/university/0')
    assert response.status_code == 400
