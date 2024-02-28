from flask import render_template, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import SystemRandom
from flask_mail import Message

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from trycars.ext.mail_client.mail_client import mail
from .forms import RegisterForm
from .token import generate_confirmation_token, confirm_token

def register_views(bp, app):
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

            token = generate_confirmation_token(app, form.email.data)

            confirmation_message = Message(
                subject='TryCars - Email Confirmation',
                recipients=[form.email.data,],
                html = render_template_string(
                    '<a href="localhost:5000/auth/confirm/{{token}}">Click here to confirm your login.</a>', token=token
                )
            )
            
            mail.send(message=confirmation_message)

            return redirect(url_for('development.database'))

        return render_template('auth/register.html', form=form)


    @bp.route('/confirm/<token>')
    def confirmation(token):
        email = confirm_token(app, token)

        if email is None:
            return 'Not Confirmed'
        else:
            user = db.session.execute(db.select(User).filter_by(email=email)).scalar()
            if user is None:
                return 'Not Confirmed'
            else:
                user.active = True
                db.session.commit()
                return 'Confirmed'
