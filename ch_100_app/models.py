"""Create database models to represent tables."""
from ch_100_app import db
from flask_login import UserMixin
from sqlalchemy_utils import URLType
from ch_100_app.utils import FormEnum
from datetime import datetime


class RoastLevel(FormEnum):
    """Roast Levels."""

    LIGHT_ROAST = "Light Roast"
    MEDIUM_ROAST = "Medium Roast"
    MEDIUM_DARK_ROAST = "Medium-Dark Roast"
    DARK_ROAST = "Dark Roast"
    VERY_DARK_ROAST = "Very Dark Roast"
    OTHER = "Other"


class ProcessMethod(FormEnum):
    """Process Methods."""

    WASHED = "Washed"
    NATURAL = "Natural"
    ANAEROBIC = "Anaerobic"
    HONEY = "Honey"
    BLACK_HONEY = "Black Honey"
    RED_HONEY = "Red Honey"
    OTHER = "Other"


class OrderCategory(FormEnum):
    """Order Categories."""

    SINGLE_ORIGIN = "Single Origin"
    BLEND = "Blend"


class BrewMethod(FormEnum):
    """Brew Methods."""

    DRIP = "Drip"
    ESPRESSO = "Espresso"
    FRENCH_PRESS = "French Press"
    AERO_PRESS = "Aero Press"
    SIPHON = "Siphon"
    WATER_DRIP = "Water Drip"
    OTHER = "Other"


class AromaChoices(FormEnum):
    """Aroma Choices."""

    SWEET = "Sweet"
    BRIGHT = "Bright"
    PERFUME = "Perfume"
    SUBTLE = "Subtle"
    INTENSE = "Intense"
    EARTHY = "Earthy"
    NUTTY = "Nutty"
    SHARP = "Sharp"
    FRUITY = "Fruity"
    FERMENT = "Ferment"
    PEPPERY = "Peppery"
    SPICE = "Spice"


class FlavorChoices(FormEnum):
    """Flavor Choices."""

    RED_FRUIT = "Red Fruit"
    WARM_CITRUS = "Warm Citrus"
    CHOCOLATE = "Chocolate"
    TROPICAL = "Tropical"
    LEMON_LIME = "Lemon Lime"
    FLORAL = "Floral"
    CANDY = "Candy"
    STONE_FRUIT = "Stone Fruit"
    NUTS = "Nuts"
    TEA_LIKE = "Tea-like"
    WINE = "Wine"
    NOUGAT = "Nougat"


class AftertasteChoices(FormEnum):
    """Aftertaste Choices."""

    CLEAN = "Clean"
    FLORAL = "Floral"
    LINGERING = "Lingering"
    DEEP = "Deep"
    SHARP = "Sharp"
    BUTTERY = "Buttery"
    SWEET = "Sweet"
    FRUITY = "Fruity"
    SHORT = "Short"
    LIGHT = "Light"
    WARM = "Warm"
    SMOKY = "Smoky"


class AcidityChoices(FormEnum):
    """Acidity Choices."""

    VIBRANT = "Vibrant"
    SWEET = "Sweet"
    TANGY = "Tangy"
    TART = "Tart"
    SOFT = "Soft"
    STRONG = "Strong"
    DELICATE = "Delicate"
    SOUR = "Sour"
    LEMONY = "Lemony"
    MILD = "Mild"
    WINEY = "Winey"
    COMPLEX = "Complex"


class MouthfeelChoices(FormEnum):
    """Mouthfeel Choices."""

    JUICY = "Juicy"
    CREAMY = "Creamy"
    SMOOTH = "Smooth"
    RICH = "Rich"
    VELVETY = "Velvety"
    THICK = "Thick"
    BUTTERY = "Buttery"
    BOUNCY = "Bouncy"
    SOFT = "Soft"
    THIN = "Thin"
    LIQUOR_LIKE = "Liquor-like"
    REFRESHING = "Refreshing"


class Bean(db.Model):
    """Bean model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    # Arabica, Robusta, Typica, Bourbon, Caturra, Catuai, Geisha
    cultivar = db.Column(db.String(60))

    # Ethiopia, Colombia, Brazil, Costa Rica, Guatemala, Kenya, Panama
    origin = db.Column(db.String(100), nullable=False)

    # ALMA PINEDA, LUZ DARY BURBANO, HUILA COMMUNITY SMALLHOLDERS, VIDES FAMILY
    producer = db.Column(db.String(100))

    # Washed, Natural, Black Honey, etc.
    process = db.Column(db.Enum(ProcessMethod), default=ProcessMethod.OTHER)

    # Individual (such as Hara), or roaster (such as Metric)
    roasted_by = db.Column(db.String(100))

    # Light roast, Medium roast, etc.
    category = db.Column(db.Enum(RoastLevel), default=RoastLevel.OTHER)


class Note(db.Model):
    """Note model."""

    id = db.Column(db.Integer, primary_key=True)
    # FK User
    # FK Bean

    # Single Origin / Blend
    order = db.Column(db.Enum(OrderCategory), default=OrderCategory.SINGLE_ORIGIN)

    # Drip, Espresso, French Roast, etc.
    brew_method = db.Column(db.Enum(BrewMethod), default=BrewMethod.DRIP)

    # Sweet, Bright, Perfume, etc.
    aroma = db.Column(db.Enum(AromaChoices))

    # Red fruit, Chocolate, Floral, etc.
    flavor = db.Column(db.Enum(FlavorChoices))

    # Clean, Fruity, Buttery, etc.
    aftertaste = db.Column(db.Enum(AftertasteChoices))

    # Sweet, Tangy, Tart, etc.
    acidity = db.Column(db.Enum(AcidityChoices))

    # Creamy, Bouncy, Juicy, etc.
    mouthfeel = db.Column(db.Enum(MouthfeelChoices))

    general_notes = db.Column(db.Text, nullable=False)

    date_time = db.Column(db.DateTime, default=datetime.utcnow)


class Cafe(db.Model):
    """Cafe model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(100), nullable=False)


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
