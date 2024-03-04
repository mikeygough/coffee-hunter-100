"""Create database models to represent tables."""
from ch_100_app.extensions import db

# from ch_100_app import db
from ch_100_app.utils import FormEnum
from flask_login import UserMixin
from datetime import datetime


## ------------ ENUMS ------------
class RoastLevel(FormEnum):
    """Roast Levels."""

    LIGHT_ROAST = "Light Roast"
    MEDIUM_ROAST = "Medium Roast"
    MEDIUM_DARK_ROAST = "Medium-Dark Roast"
    DARK_ROAST = "Dark Roast"
    VERY_DARK_ROAST = "Very Dark Roast"
    OTHER = "Other"


class WashProcess(FormEnum):
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


## ------------ BRIDGE TABLES ------------
note_aroma = db.Table(
    "note_aroma",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
    db.Column("aroma_id", db.Integer, db.ForeignKey("aroma.id"), primary_key=True),
)

note_flavor = db.Table(
    "note_flavor",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
    db.Column("flavor_id", db.Integer, db.ForeignKey("flavor.id"), primary_key=True),
)

note_aftertaste = db.Table(
    "note_aftertaste",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
    db.Column(
        "aftertaste_id", db.Integer, db.ForeignKey("aftertaste.id"), primary_key=True
    ),
)

note_acidity = db.Table(
    "note_acidity",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
    db.Column("acidity_id", db.Integer, db.ForeignKey("acidity.id"), primary_key=True),
)

note_mouthfeel = db.Table(
    "note_mouthfeel",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
    db.Column(
        "mouthfeel_id", db.Integer, db.ForeignKey("mouthfeel.id"), primary_key=True
    ),
)


## ------------ MODELS ------------
class Bean(db.Model):
    """Bean model."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    # Ethiopia, Colombia, Brazil, Costa Rica, Guatemala, Kenya, Panama
    origin = db.Column(db.String(100), nullable=False)
    # Arabica, Robusta, Typica, Bourbon, Caturra, Catuai, Geisha
    cultivar = db.Column(db.String(60))
    # Washed, Natural, Black Honey, etc.
    wash_process = db.Column(db.Enum(WashProcess), nullable=False)
    # Light roast, Medium roast, etc.
    roast_level = db.Column(db.Enum(RoastLevel), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    ## ------------ Relationships ------------
    notes = db.relationship("Note", back_populates="bean")
    created_by = db.relationship("User")

    ## ------------ Methods ------------
    def __str__(self):
        return f"<Bean: {self.name} from {self.origin}>"

    def __repr__(self):
        return f"<Bean: {self.name} from {self.origin}>"


class Note(db.Model):
    """Note model."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    bean_id = db.Column(db.Integer, db.ForeignKey("bean.id"), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Single Origin / Blend
    order = db.Column(db.Enum(OrderCategory), default=OrderCategory.SINGLE_ORIGIN)
    # Drip, Espresso, French Roast, etc.
    brew_method = db.Column(db.Enum(BrewMethod), default=BrewMethod.DRIP)
    # mm/dd/yyyy
    date_recorded = db.Column(db.Date, default=datetime.utcnow)
    observations = db.Column(db.Text, nullable=False)

    ## ------------ Relationships ------------
    bean = db.relationship("Bean", back_populates="notes")
    created_by = db.relationship("User")

    aromas = db.relationship(
        "Aroma", secondary=note_aroma, backref=db.backref("notes", lazy="dynamic")
    )

    flavors = db.relationship(
        "Flavor", secondary=note_flavor, backref=db.backref("notes", lazy="dynamic")
    )

    aftertastes = db.relationship(
        "Aftertaste",
        secondary=note_aftertaste,
        backref=db.backref("notes", lazy="dynamic"),
    )

    acidities = db.relationship(
        "Acidity", secondary=note_acidity, backref=db.backref("notes", lazy="dynamic")
    )

    mouthfeels = db.relationship(
        "Mouthfeel",
        secondary=note_mouthfeel,
        backref=db.backref("notes", lazy="dynamic"),
    )

    ## ------------ Methods ------------
    def __str__(self):
        return f"<Note: {self.bean.name} note created by {self.created_by.username} on {self.date_recorded}>"

    def __repr__(self):
        return f"<Note: {self.bean.name} note created by {self.created_by.username} on {self.date_recorded}>"


class Aroma(db.Model):
    """Aroma Model. For example: Sweet, Bright, Perfume, etc."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(AromaChoices), nullable=False)

    ## ------------ Methods ------------
    def __repr__(self):
        return f"<Aroma {self.name}>"


class Flavor(db.Model):
    """Flavor Model. For example: Red fruit, Chocolate, Floral, etc."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(FlavorChoices), nullable=False)

    ## ------------ Methods ------------
    def __repr__(self):
        return f"<Flavor {self.name}>"


class Aftertaste(db.Model):
    """Aftertaste Model. For example: Clean, Fruity, Buttery, etc."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(AftertasteChoices), nullable=False)

    ## ------------ Methods ------------
    def __repr__(self):
        return f"<Aftertaste {self.name}>"


class Acidity(db.Model):
    """Acidity model. For example: Sweet, Tangy, Tart, etc."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(AcidityChoices), nullable=False)

    ## ------------ Methods ------------
    def __repr__(self):
        return f"<Acidity {self.name}>"


class Mouthfeel(db.Model):
    """Mouthfeel model. For example: Creamy, Bouncy, Juicy, etc."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(MouthfeelChoices), nullable=False)

    ## ------------ Methods ------------
    def __repr__(self):
        return f"<Mouthfeel {self.name}>"


class User(UserMixin, db.Model):
    """User model."""

    ## ------------ Attributes ------------
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    ## ------------ Methods ------------
    def __str__(self):
        return f"<Username: {self.username}>"

    def __repr__(self):
        return f"<Username: {self.username}>"
