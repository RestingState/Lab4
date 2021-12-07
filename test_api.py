from unittest.mock import ANY

from flask import url_for
from flask_testing import TestCase

from src.models import metadata, engine
from src.db_actions import session
from src.main import app, bcrypt

class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.create_tables()

        self.user1_data = {
            "username": "whatever",
            "first_name": "testing",
            "last_name": "laaast!",
            "email": "whatever@gmail.com",
            "password": "123456",
            "phone": "0663578412"
        }

        self.user2_data = {
            "username": "sowhat",
            "first_name": "testing",
            "last_name": "laaast!",
            "email": "whatever@gmail.com",
            "password": "123456",
            "phone": "0663578412"
        }

        self.user1_authorization = {
            "Authorization": "Basic d2hhdGV2ZXI6MTIzNDU2"
        }

        self.user2_authorization = {
            "Authorization": "Basic D2hhdGV2ZXI6MTIzNDU2"
        }

        self.ticket1 = {
            "title": "art museum",
            "start_date": "2021-06-05",
            "place": "arena lviv",
            "line": 5,
            "sit_place": 28,
            "price": 100,
            "status": "active",
            "username": "whatever"
        }

        self.ticket2 = {
            "title": "art museum",
            "start_date": "2021-06-05",
            "place": "arena lviv",
            "line": 5,
            "sit_place": 28,
            "price": 100,
            "status": "active",
            "username": "never"
        }

        self.booking1 = {
            "ticket": self.ticket1,
            "expires": "2021-01-30"
        }

        self.booking2 = {
            "ticket": self.ticket2,
            "expires": "2021-01-30"
        }

    def create_user(self, data):
        resp = self.client.post(url_for("userRoot"), json=data)
        return resp

    def login_user(self, data):
        resp = self.client.get(url_for("userLogin"), headers=data)
        return resp

    def book(self, data, token):
        resp = self.client.post(url_for("bookingRoot"), json=data, headers={"x-access-token": token["token"]})
        return resp

    def buy(self, data, token):
        resp = self.client.post(url_for("buyingRoot"), json=data, headers={"x-access-token": token["token"]})
        return resp

    def create_tables(self):
        metadata.drop_all(engine)
        metadata.create_all(engine)

    def tearDown(self):
        session.close()

    def create_app(self):
        return app


class test_User(BaseTestCase):
    def test_post_user(self):
        resp = self.create_user(self.user1_data)
        self.assert_200(resp)

    def test_post_user_invalid(self):
        resp = self.create_user(self.booking1)
        self.assert_400(resp)
        resp = self.create_user({
            "username": "whatever",
            "first_name": "testing",
            "last_name": "laaast!",
            "email": "whatever",
            "password": "123456",
            "phone": "0663578412"
        })
        self.assert_400

    def test_login(self):
        self.create_user(self.user1_data)
        resp = self.login_user(self.user1_authorization)
        self.assertEqual(resp.json, {"token": ANY})

    def test_login_fail(self):
        self.create_user(self.user1_data)
        resp = self.login_user(self.user2_authorization)
        self.assert_403(resp)

    def test_login_invalid(self):
        self.create_user(self.user1_data)
        resp = self.login_user(self.ticket1)
        self.assert_(resp)
        resp = self.login_user({"username": 1, "password": 1})
        self.assert_500(resp)

    def test_post_user_fail(self):
        self.create_user(self.user1_data)
        resp = self.create_user(self.user1_data)
        self.assert_500(resp)

    def test_logout(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.get(url_for("userLogout"), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_get_user(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.get(url_for("userHandling", username="whatever"), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_put_user(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.put(url_for(
            "userHandling", username="whatever"),
            headers={"x-access-token": token["token"]},
            json={
                "username": "whatever",
                "first_name": "testing",
                "last_name": "last_real",
                "email": "whatever@gmail.com",
                "password": "123456",
                "phone": "0663578412"
            }
        )
        self.assert_200(resp)

    def test_put_user_invalid(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.put(url_for(
            "userHandling", username="whatever"),
            headers={"x-access-token": token["token"]},
            json={
                "username": "",
                "first_name": "testing",
                "last_name": "last_real",
                "email": "whatever",
                "password": "123456",
                "phone": "0663578412"
            }
        )
        self.assert_400(resp)

    def test_delete_user(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.delete(url_for("userHandling", username="whatever"), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_handling_fail(self):
        self.create_user(self.user1_data)
        self.create_user(self.user2_data)
        token = self.login_user(self.user1_authorization).json

        resp = self.client.delete(url_for("userHandling", username="sowhat"), headers={"x-access-token": token["token"]})
        self.assert_404(resp)
        resp = self.client.delete(url_for("userHandling", username=""), headers={"x-access-token": token["token"]})
        self.assert_404(resp)


class test_Booking(BaseTestCase):
    def test_post_booking(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.book(self.booking1, token)
        self.assert_200(resp)

    def test_post_booking_invalid(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.buy(self.ticket1, token)
        resp = self.book(self.booking1, token)
        self.assert_400(resp)

    def test_post_booking_unauth(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.book(self.booking1, {"token": None})
        self.assert_401(resp)

    def test_post_booking_nouser(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.book(self.booking2, token)
        self.assert_401(resp)

    def test_get_booking(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.book(self.booking1, token)
        resp = self.client.get(url_for("bookingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_get_booking_fail(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.book(self.booking1, token)
        resp = self.client.get(url_for("bookingHandling", id=2), headers={"x-access-token": token["token"]})
        self.assert_500(resp)
        resp = self.client.get(url_for("bookingHandling", id="lasagna"), headers={"x-access-token": token["token"]})
        self.assert_400(resp)


    def test_delete_booking(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.book(self.booking1, token)
        resp = self.client.delete(url_for("bookingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_delete_booking_notexist(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.delete(url_for("buyingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_500(resp)

    def test_get_all(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.book(self.booking1, token)
        resp = self.client.get(url_for("bookingMyTickets"), headers={"x-access-token": token["token"]})
        self.assert_200(resp)


class test_Buying(BaseTestCase):
    def test_post_ticket(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.buy(self.ticket1, token)
        self.assert_200(resp)

    def test_post_ticket_invalid(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.buy(self.booking1, token)
        self.assert_400(resp)
        resp = self.buy({
            "title": "art museum",
            "start_date": "no-date",
            "place": "arena lviv",
            "line": 5,
            "sit_place": 28,
            "price": 100,
            "status": "active",
            "username": "whatever"
        }, token)
        self.assert_400(resp)

        self.buy(self.ticket1, token)
        resp = self.buy(self.ticket1, token)
        self.assert_400(resp)

    def test_get_ticket(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.buy(self.ticket1, token)
        resp = self.client.get(url_for("buyingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_get_ticket_invalid(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.get(url_for("buyingHandling", id="LASAGNA"), headers={"x-access-token": token["token"]})
        self.assert_400(resp)
        resp = self.client.get(url_for("buyingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_500(resp)

    def test_delete_ticket(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.buy(self.ticket1, token)
        resp = self.client.delete(url_for("buyingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

    def test_delete_ticket_invalid(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        resp = self.client.delete(url_for("buyingHandling", id=1), headers={"x-access-token": token["token"]})
        self.assert_500(resp)

    def test_get_all(self):
        self.create_user(self.user1_data)
        token = self.login_user(self.user1_authorization).json
        self.buy(self.ticket1, token)
        resp = self.client.get(url_for("buyingMyTickets"), headers={"x-access-token": token["token"]})
        self.assert_200(resp)

