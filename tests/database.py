from trycars.ext.database.database import db
from trycars.ext.database.models import User

class TestDatabase:
    def test_database_created(self):
        users = db.session.execute(db.select(User)).scalars().fetchall()
        assert len(users) > 0


    def test_database_users_information(self):
        users = db.session.execute(db.select(User)).scalars().fetchall()
        assert users[0].roles.name == 'admin'


    def test_model_return_repr(self):
        users = db.session.execute(db.select(User)).scalars().fetchall()
        assert str(users[0]) == 'User(id=1, email=lucasribeiroalves@live.com, username=lribeiro)'
        assert str(users[0].roles) == 'Role(id=1, name=admin, desciption=Admin User Privileges)'