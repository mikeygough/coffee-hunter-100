import unittest
import app

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
    santa_rita = Bean(
        name="Santa Rita",
        origin="Colombia",
        cultivar="Caturra",
        wash_process=WashProcess.WASHED,
        roast_level=RoastLevel.LIGHT_ROAST,
        created_by_id=1,
    )

    don_angel = Bean(
        name="Don Angel",
        origin="Guatemala",
        cultivar="Caturra",
        wash_process=WashProcess.WASHED,
        roast_level=RoastLevel.LIGHT_ROAST,
        created_by_id=1,
    )

    santa_rita_note = Note(
        bean_id=1,
        created_by_id=1,
        order=OrderCategory.SINGLE_ORIGIN,
        brew_method=BrewMethod.DRIP,
        observations="delicious!",
    )

    db.session.add(santa_rita)
    db.session.add(don_angel)
    db.session.add(santa_rita_note)

    db.session.commit()


def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="mikey", password=password_hash)
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
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the beans show up on the homepage."""
        # Set up
        create_beans()
        create_user()

        # Make a GET request
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Coffee Hunter 100", response_text)
        self.assertIn("Santa Rita", response_text)
        self.assertIn("Don Angel", response_text)
        self.assertIn("Log In", response_text)
        self.assertIn("Signup", response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn("New Note", response_text)
        self.assertNotIn("New Bean", response_text)
        self.assertNotIn("Log Out", response_text)

    def test_homepage_logged_in(self):
        """Test that the beans show up on the homepage."""
        # Set up
        create_beans()
        create_user()
        login(self.app, "mikey", "password")

        # Make a GET request
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Coffee Hunter 100", response_text)
        self.assertIn("Santa Rita", response_text)
        self.assertIn("Don Angel", response_text)
        self.assertIn("New Bean", response_text)
        self.assertIn("New Note", response_text)
        self.assertIn("Log Out", response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn("Log In", response_text)
        self.assertNotIn("Signup", response_text)

    def test_bean_detail_logged_out(self):
        """
        Test that the user is redirected when trying to access the bean detail
        route if not logged in.
        """
        create_beans()

        response = self.app.get("/bean/1")

        # Make sure that the user was redirecte to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login?next=%2Fbean%2F1", response.location)

    def test_bean_detail_logged_in(self):
        """Test that the bean appears on its detail page."""
        # Set up
        create_beans()
        create_user()
        login(self.app, "mikey", "password")

        response = self.app.get("/bean/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("You are logged in as mikey", response_text)
        self.assertIn("<p><strong>Origin:</strong> Colombia</p>", response_text)
        self.assertIn("<p><strong>Cultivar:</strong> Caturra</p>", response_text)
        self.assertIn("<p><strong>Wash Process:</strong> Washed</p>", response_text)
        self.assertIn("<p><strong>Roast Level:</strong> Light Roast</p>", response_text)
        self.assertIn("Notes", response_text)
        self.assertIn("<p><strong>Observations:</strong> delicious!</p>", response_text)

    def test_new_bean(self):
        """Test creating a bean."""
        # Set up
        create_user()
        login(self.app, "mikey", "password")

        # Make POST request with data
        post_data = {
            "name": "Alma Pineda SL-28",
            "origin": "Honduras",
            "cultivar": "SL-28",
            "wash_process": "NATURAL",
            "roast_level": "LIGHT_ROAST",
        }

        self.app.post("/new_bean", data=post_data)
        bean = Bean.query.filter_by(name="Alma Pineda SL-28").one()
        self.assertIsNotNone(bean)
        self.assertEqual(bean.origin, "Honduras")
        self.assertEqual(bean.cultivar, "SL-28")

    def test_note_detail_logged_out(self):
        """
        Test that the user is redirected when trying to access the note detail
        route if not logged in.
        """
        create_beans()

        response = self.app.get("/note/1")

        # Make sure that the user was redirecte to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login?next=%2Fnote%2F1", response.location)

    def test_new_note(self):
        """Test creating a note."""
        # Set up
        create_beans()
        create_user()
        login(self.app, "mikey", "password")

        # Make POST request with data
        post_data = {
            "bean": "1",
            "order": "SINGLE_ORIGIN",
            "brew_method": "DRIP",
            "date_recorded": "2024-03-05",
            "observations": "Fruity!",
        }

        self.app.post("/new_note", data=post_data)
        note = Note.query.get(2)
        self.assertIsNotNone(note)
        self.assertEqual(note.bean.id, 1)
        self.assertEqual(note.observations, "Fruity!")
