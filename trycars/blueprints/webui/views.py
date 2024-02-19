from trycars.ext.database.database import db
from trycars.ext.database.models import *

def register_views(bp):
    @bp.route('/')
    def index():
        return 'Hello, World!'
    
    @bp.route('/database')
    def database():
        return {
            'users':[str(user) for user in db.session.execute(db.select(User)).scalars()],
            'roles':[str(role) for role in db.session.execute(db.select(Role)).scalars()],
        }