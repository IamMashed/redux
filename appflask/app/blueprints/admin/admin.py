from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_security.utils import hash_password
from app import db
from app.database.models.user import User, Role
from flask_babelex import gettext
from app.blueprints.admin.admin_forms import CreateForm, EditForm
from app.routing.decorators import admin_required

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def admin_index():
    users = User.query.all()
    return render_template('admin/admin_index.html',
                           users=users)


@admin.route('/create/', methods=['GET', 'POST'])
@admin_required
def admin_create():
    create_form = CreateForm()
    if create_form.validate_on_submit():
        user = User(email=create_form.email.data,
                    username=create_form.username.data,
                    role=Role.query.get(create_form.role.data),
                    password=hash_password(create_form.password.data),
                    )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.remove()
            flash(str(e))
        flash(gettext('User created'))
        return redirect('/admin/')
    return render_template('admin/admin_create.html',
                           create_form=create_form)


@admin.route('/edit/<int:id>/', methods=['GET', 'POST'])
@admin_required
def admin_edit(id):
    user = User.query.get_or_404(id)
    edit_form = EditForm(user)

    # handling delete button
    if edit_form.delete.data:
        db.session.delete(user)
        db.session.commit()
        flash(gettext('User has been deleted'))
        # if deleted was last available user
        if not User.query.count():
            return redirect(url_for('index'))
        return redirect(url_for('admin.admin_index'))

    # handling update button
    if edit_form.validate_on_submit():
        user.email = edit_form.email.data
        user.username = edit_form.username.data
        user.role = Role.query.get(edit_form.role.data)
        password = edit_form.password.data
        confirm_password = edit_form.confirm_password.data

        if password and confirm_password:
            if password != confirm_password:
                flash(gettext('Password confirmation failed'))
                return redirect(request.url)
            user.password = hash_password(password)
        db.session.commit()
        flash('User Edit Successful')
        return redirect(url_for('admin.admin_index'))
    edit_form.username.data = user.username
    edit_form.email.data = user.email
    edit_form.role.data = user.role_id
    return render_template('admin/admin_edit.html',
                           edit_form=edit_form)
