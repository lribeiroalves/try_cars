from flask import request, redirect, url_for, render_template
from flask_mail import Message
from werkzeug.utils import secure_filename
import os
from flask_login import login_required

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from trycars.ext.mail_client.mail_client import mail

from .forms import MyFirstForm, PhotoForm, CaptchaForm

def register_views(bp, app):
    
    @bp.route('/database')
    def database():
        return {
            'users':[str(user) for user in db.session.execute(db.select(User)).scalars()],
            'roles':[str(role) for role in db.session.execute(db.select(Role)).scalars()],
            'relations': [f'User: {str(user.username)} --> Role: {str(user.roles.name)}' for user in db.session.execute(db.select(User)).scalars()],
        }
    
    @bp.route('/email', methods=['GET', 'POST'])
    @login_required
    def email():
        if request.method == 'POST':
            msg = Message(
                subject='Testing Email',
                recipients=['lucasribeiroalves@live.com'],
                body='Email sent from my Flask Aplication using Python.'
            )
            mail.send(msg)
            return 'Email Sent'
        else:
            return """
                <p><strong> Testing... </strong></p>
                <form method="post">
                    <button>Send Email</button>
                </form>
            """
    
    @bp.route('/home')
    def home():
        return redirect(url_for('homepage.index'))
    
    @bp.route('/form', methods=['GET', 'POST'])
    def form():
        form = MyFirstForm()
        if form.validate_on_submit():
            return 'OK'
        return render_template('development/first_form.html', form=form)
    
    @bp.route('/photo-form', methods=['GET', 'POST'])
    def photo_form():
        form = PhotoForm()

        if form.validate_on_submit():
            print('teste')
            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                app.instance_path, 'photos', filename
            ))
            return 'File Uploaded'
        
        return render_template('development/upload.html', form=form)
    
    @bp.route('/captcha', methods=['GET', 'POST'])
    def captcha():
        form = CaptchaForm()


        if form.validate_on_submit():
            user = db.session.execute(db.select(User).filter_by(username=form.user.data)).scalar()
            return str(user)
        
        return render_template('development/captcha.html', form=form)
