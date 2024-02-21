from flask import request, redirect, url_for
from flask_mail import Message

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from trycars.ext.mail_client.mail_client import mail

def register_views(bp):
    
    @bp.route('/database')
    def database():
        return {
            'users':[str(user) for user in db.session.execute(db.select(User)).scalars()],
            'roles':[str(role) for role in db.session.execute(db.select(Role)).scalars()],
        }
    
    @bp.route('/email', methods=['GET', 'POST'])
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