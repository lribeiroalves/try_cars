from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import SystemRandom

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from .forms import RegisterForm

def register_views(bp):
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            # generate unique fs_uniquifier
            while True:
                fs = str(SystemRandom().getrandbits(64))[0:15]
                if db.session.execute(db.select(User).filter_by(fs_uniquifier=fs)).scalar() is None:
                    break

            user_role = db.session.execute(db.select(Role).filter_by(name='user')).scalar()
            new_user = User(email=form.email.data, username=form.username.data, active=False, fs_uniquifier=fs, password=generate_password_hash(form.password.data), roles=user_role)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('development.database'))

        return render_template('auth/register.html', form=form)
