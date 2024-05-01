from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date, datetime
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
from ch_100_app.main.forms import BeanForm, NoteForm

# Import app and db from events_app package so that we can run app
from ch_100_app.extensions import app, db

main = Blueprint("main", __name__)

## ------------ Routes ------------


@main.route("/")
def homepage():
    beans = []
    if current_user == True:
        beans = Bean.query.filter_by(created_by_id=current_user.id)
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
            created_by_id=current_user.id,
        )

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
        # get selected aroma, flavor, aftertaste, acidity and mouthfeel choices from the form
        selected_aroma_names = form.aromas.data
        selected_flavor_names = form.flavors.data
        selected_aftertaste_names = form.aftertastes.data
        selected_acidity_names = form.acidities.data
        selected_mouthfeel_names = form.mouthfeels.data

        # get selected aroma, flavor, aftertaste, acidity and mouthfeel choices from db
        aromas = [Aroma(name=value) for value in selected_aroma_names]
        flavors = [Flavor(name=value) for value in selected_flavor_names]
        aftertastes = [Aftertaste(name=value) for value in selected_aftertaste_names]
        acidities = [Acidity(name=value) for value in selected_acidity_names]
        mouthfeels = [Mouthfeel(name=value) for value in selected_mouthfeel_names]

        # create note
        new_note = Note(
            bean=form.bean.data,
            order=form.order.data,
            brew_method=form.brew_method.data,
            observations=form.observations.data,
            date_recorded=form.date_recorded.data,
            created_by_id=current_user.id,
        )

        # extend with bridge table references
        new_note.aromas.extend(aromas)
        new_note.flavors.extend(flavors)
        new_note.aftertastes.extend(aftertastes)
        new_note.acidities.extend(acidities)
        new_note.mouthfeels.extend(mouthfeels)

        db.session.add(new_note)
        db.session.commit()

        flash("New note was created successfully.")
        return redirect(url_for("main.note_detail", note_id=new_note.id))

    return render_template("new_note.html", form=form)


@main.route("/bean/<bean_id>", methods=["GET", "POST"])
@login_required
def bean_detail(bean_id):
    bean = Bean.query.get(bean_id)
    form = BeanForm(obj=bean)
    # change text from submit to update
    form.submit.label.text = "Update Bean"
    # populate wash process and roast level
    # form.wash_process.label.text = bean.wash_process
    form.wash_process.value = bean.wash_process
    form.wash_process.placeholder = bean.wash_process
    print(form.wash_process)
    print(bean.wash_process)
    notes = bean.notes

    # check if valid
    if form.validate_on_submit():
        # update values
        bean.name = form.name.data
        bean.cultivar = form.cultivar.data
        bean.origin = form.origin.data
        bean.wash_process = form.wash_process.data
        bean.roast_level = form.roast_level.data

        db.session.commit()

        flash("Bean updated successfully.")
        return redirect(url_for("main.bean_detail", bean_id=bean.id))

    return render_template("bean_detail.html", bean=bean, form=form, notes=notes)


@main.route("/note/<note_id>", methods=["GET", "POST"])
@login_required
def note_detail(note_id):
    note = Note.query.get(note_id)

    return render_template("note_detail.html", note=note)


@main.route("/delete_note/<note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    bean_id = note.bean_id

    db.session.delete(note)
    db.session.commit()

    flash("Note deleted successfully", "success")
    return redirect(url_for("main.bean_detail", bean_id=bean_id))


@main.route("/coffee_context")
def coffee_context():
    return render_template("coffee_context.html")
