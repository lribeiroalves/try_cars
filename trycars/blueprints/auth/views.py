from flask import render_template, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import SystemRandom
from flask_mail import Message
import datetime

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from trycars.ext.mail_client.mail_client import mail
from .forms import RegisterForm, EmailConfirmationForm
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
            if user_role is None:
                user_role = Role(name = 'user', description='Simple User')
            new_user = User(email=form.email.data, username=form.username.data, active=False, fs_uniquifier=fs, password=generate_password_hash(form.password.data), roles=user_role)
            db.session.add(new_user)
            db.session.commit()

            # email confirmation
            token = generate_confirmation_token(app, form.email.data)
            confirmation_message = Message(
                subject='TryCars - Email Confirmation',
                recipients=[form.email.data,],
                html = f"""
                <p>
                    You have registered your TryCars account succesfully.
                </p>
                <p>
                    Copy the link
                    <p><strong>localhost:5000/auth/confirm/{token}</strong></p>
                    and paste it into your browser to confirm your email and have access to all functionallity of the website.
                </p>
                <p>
                    Thank You.
                </p>
                """
            )
            mail.send(message=confirmation_message)

            return redirect(url_for('homepage.index'))

        return render_template('auth/register.html', form=form)


    @bp.route('/confirm/<token>')
    def confirmation(token):
        form = EmailConfirmationForm()
        email = confirm_token(app, token)

        if email is None:
            return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)
        else:
            user = db.session.execute(db.select(User).filter_by(email=email)).scalar()
            if user is None:
                return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)
            else:
                if user.active:
                    return render_template('auth/email_confirmation.html', confirmed = 'a', form=form)
                else:
                    user.active = True
                    user.confirmed_at = datetime.datetime.now()
                    db.session.commit()
                    return render_template('auth/email_confirmation.html', confirmed = 'y', form=form)


    @bp.route('/confirmation/send', methods=['GET', 'POST'])
    def send_new_confirmation_link():
        form = EmailConfirmationForm()

        if form.validate_on_submit():
            # email confirmation
            token = generate_confirmation_token(app, form.email.data)
            confirmation_message = Message(
                subject='TryCars - Email Confirmation',
                recipients=[form.email.data,],
                html = f"""
                <p>
                    This is a new confirmation code for your TryCars account.
                </p>
                <p>
                    Copy the link
                    <p><strong>localhost:5000/auth/confirm/{token}</strong></p>
                    and paste it into your browser to confirm your email and have access to all functionallity of the website.
                </p>
                <p>
                    Thank You.
                </p>
                """
            )
            mail.send(message=confirmation_message)

            return redirect(url_for('homepage.index'))
        
        else:
            return render_template('auth/email_confirmation.html', confirmed = 'n', form=form)
