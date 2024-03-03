import os
import unittest
import app

from datetime import date
from ch_100_app.extensions import app, db, bcrypt
from ch_100_app.models import (
    User,
    Bean,
    Note,
    Aroma,
    Flavor,
    Aftertaste,
    Acidity,
    Mouthfeel,
)

from ch_100_app.models import (
    WashProcess,
    RoastLevel,
    OrderCategory,
    BrewMethod,
    AromaChoices,
    FlavorChoices,
    AftertasteChoices,
    AcidityChoices,
    MouthfeelChoices,
)

#################################################
# Setup
#################################################


def login(client, username, password):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def create_beans():
    bean = Bean(
        name="Santa Rita",
        origin="Colombia",
        cultivar="Caturra",
        wash_process=WashProcess.WASHED,
        roast_level=RoastLevel.LIGHT_ROAST,
    )

    db.session.add(bean)
    db.session.commit()


def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="me1", password=password_hash)
    db.session.add(user)
    db.session.commit()


class MainTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        print(app.app_context())
        with app.app_context():  # Ensure that we're operating within the application context
            db.create_all()
        # db.drop_all()
        # db.create_all()

    def test_homepage_logged_out(self):
        """Test that the beans show up on the homepage."""
        # Set up
        create_beans()
        create_user()

        # Make a GET request
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # # Check that page contains all of the things we expect
        # response_text = response.get_data(as_text=True)
        # self.assertIn("To Kill a Mockingbird", response_text)
        # self.assertIn("The Bell Jar", response_text)
        # self.assertIn("me1", response_text)
        # self.assertIn("Log In", response_text)
        # self.assertIn("Sign Up", response_text)

        # # Check that the page doesn't contain things we don't expect
        # # (these should be shown only to logged in users)
        # self.assertNotIn("Create Book", response_text)
        # self.assertNotIn("Create Author", response_text)
        # self.assertNotIn("Create Genre", response_text)


#################################################
# Tests
#################################################
