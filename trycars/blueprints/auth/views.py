from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from .forms import RegisterForm

def register_views(bp):
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            user_role = db.session.execute(db.select(Role).filter_by(name='user')).scalar()
            new_user = User(email=form.email.data, username=form.username.data, active=False, fs_uniquifier='987987654312', password=generate_password_hash(form.password.data), roles=user_role)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('development.database'))

        return render_template('auth/register.html', form=form)
