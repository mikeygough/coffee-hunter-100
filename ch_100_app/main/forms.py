from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SelectField,
    SubmitField,
    TextAreaField,
    SelectMultipleField,
    widgets,
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

# from wtforms.fields.html5 import URLField
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from ch_100_app.models import User, Bean, Note


class BeanForm(FlaskForm):
    """Form for adding/updating a Bean."""

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(
                max=60,
                message="Your bean needs a name! (Keep it 60 characters or less).",
            ),
        ],
    )

    cultivar = StringField(
        "Cultivar",
        validators=[
            Length(
                max=60,
                message="Your bean needs a cultivar value (keep it 60 characters or less).",
            ),
        ],
    )

    origin = StringField(
        "Origin",
        validators=[
            DataRequired(),
            Length(
                max=100,
                message="Your bean needs an origin! (Keep it 100 characters or less).",
            ),
        ],
    )

    producer = StringField(
        "Producer",
        validators=[
            Length(
                max=100,
                message="Your bean needs a producer value (keep it 100 characters or less).",
            )
        ],
    )

    wash_process = SelectField("Wash Process", choices=WashProcess.choices())

    roasted_by = StringField(
        "Roaster",
        validators=[
            Length(
                max=100,
                message="Your bean needs a roasted_by value (keep it 60 characters or less).",
            )
        ],
    )

    roast_level = SelectField("Roast Level", choices=RoastLevel.choices())

    submit = SubmitField("Save Bean")


class NoteForm(FlaskForm):
    """Form for adding/updating a Note."""

    order = SelectField("Order", choices=OrderCategory.choices())

    brew_method = SelectField("Brew Method", choices=BrewMethod.choices())

    # multi selects start
    aromas = SelectMultipleField(
        "Aroma Choices",
        choices=[(choice.name, choice.value) for choice in AromaChoices],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    flavors = SelectMultipleField(
        "Flavor Choices",
        choices=[(choice.name, choice.value) for choice in FlavorChoices],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    aftertastes = SelectMultipleField(
        "Aftertaste Choices",
        choices=[(choice.name, choice.value) for choice in AftertasteChoices],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    acidities = SelectMultipleField(
        "Acidity Choices",
        choices=[(choice.name, choice.value) for choice in AcidityChoices],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    mouthfeels = SelectMultipleField(
        "Mouthfeel Choices",
        choices=[(choice.name, choice.value) for choice in MouthfeelChoices],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
    )

    # multi selects end

    general_notes = TextAreaField(
        "General Notes",
        validators=[
            DataRequired(),
        ],
    )

    date_time = DateField("Date")

    submit = SubmitField("Save Note")
