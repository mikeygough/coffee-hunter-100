from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date, datetime
from ch_100_app.models import User, Bean, Note
from ch_100_app.main.forms import BeanForm, NoteForm

# Import app and db from events_app package so that we can run app
from ch_100_app.extensions import app, db

main = Blueprint("main", __name__)

## ------------ Routes ------------


@main.route("/")
def homepage():
    beans = Bean.query.all()
    return render_template("home.html", beans=beans)


@main.route("/new_bean", methods=["GET", "POST"])
@login_required
def new_bean():
    # form
    form = BeanForm()

    # if form was submitted with no errors
    if form.validate_on_submit():
        new_bean = Bean(
            name=form.name.data,
            cultivar=form.cultivar.data,
            origin=form.origin.data,
            wash_process=form.wash_process.data,
            roast_level=form.roast_level.data,
        )
        # added this ⬇️
        # new_bean = db.session.merge(new_bean)
        # added this ⬆️
        db.session.add(new_bean)
        db.session.commit()

        flash("New bean was created successfully.")
        return redirect(url_for("main.bean_detail", bean_id=new_bean.id))

    return render_template("new_bean.html", form=form)


@main.route("/new_note", methods=["GET", "POST"])
@login_required
def new_note():
    # form
    form = NoteForm()

    # if form was submitted with no errors
    if form.validate_on_submit():
        new_note = Note(
            bean=form.bean.data,
            order=form.order.data,
            brew_method=form.brew_method.data,
            aroma=form.aromas.data,
            flavor=form.flavors.data,
            aftertaste=form.aftertastes.data,
            acidity=form.acidities.data,
            mouthfeel=form.mouthfeels.data,
            observations=form.observations.data,
            date_recorded=form.date_recorded.data,
        )
        # added this ⬇️
        # new_note = db.session.merge(new_note)
        # added this ⬆️
        db.session.add(new_note)
        db.session.commit()

        flash("New note was created successfully.")
        return redirect(url_for("main.homepage"))

    return render_template("new_note.html", form=form)


@main.route("/bean/<bean_id>", methods=["GET", "POST"])
@login_required
def bean_detail(bean_id):
    bean = Bean.query.get(bean_id)

    return render_template("bean_detail.html", bean=bean)
