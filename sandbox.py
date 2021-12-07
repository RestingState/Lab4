from src.main import app, session
from src.database_model import engine, metadata, Major

metadata.drop_all(engine)
metadata.create_all(engine)
client = app.test_client()
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
major = Major(name='Physics')
session.add(major)
session.flush()
student_good = {
    "name": "TestSubj",
    "major": 1,
    "rating": 16,
    "marks": []
}

client.post('/user', json=user_good_1)
response = client.post('/student', json=student_good, headers=auth_good_1)
print(response.data)
