import unittest
import app
from unittest import TestCase

from datetime import date

from ch_100_app.extensions import app, db, bcrypt
from ch_100_app.models import User

#################################################
# Setup
#################################################


def create_user():
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="mikey", password=password_hash)
    db.session.add(user)
    db.session.commit()


#################################################
# Tests
#################################################


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        # make post request to signup
        post_data = {"username": "mikey", "password": "password"}
        response = self.app.post("/signup", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        created_user = User.query.filter_by(username="mikey").one()
        self.assertIsNotNone(create_user)
        self.assertEqual(created_user.username, "mikey")

    def test_signup_existing_user(self):
        # setup
        create_user()

        # make post request to signup
        post_data = {"username": "mikey", "password": "password"}
        response = self.app.post("/signup", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("<legend>Enter your credentials</legend>", response_text)
        self.assertIn(
            "That username is taken. Please choose a different one.", response_text
        )

    def test_login_correct_password(self):
        # setup
        create_user()

        # make post request to signup
        post_data = {"username": "mikey", "password": "password"}
        response = self.app.post("/login", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("You are logged in as mikey", response_text)

    def test_login_nonexistent_user(self):
        # make post request to signup
        post_data = {"username": "mikey", "password": "password"}
        response = self.app.post("/login", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("<legend>Enter your credentials</legend>", response_text)
        self.assertIn("No user with that username. Please try again.", response_text)

    def test_login_incorrect_password(self):
        # setup
        create_user()

        # make post request to signup
        post_data = {"username": "mikey", "password": "incorrectpassword"}
        response = self.app.post("/login", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("<legend>Enter your credentials</legend>", response_text)
        self.assertIn("Password doesn&#39;t match. Please try again.", response_text)

    def test_logout(self):
        # setup
        create_user()

        # make post request to signup
        post_data = {"username": "mikey", "password": "password"}
        response = self.app.post("/login", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("You are logged in as mikey", response_text)

        response = self.app.get("/logout", follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn("Log In", response_text)
