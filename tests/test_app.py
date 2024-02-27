from trycars.ext.database.database import db
from trycars.ext.database.models import User


class TestApp:
    def test_app_is_created(self, min_app):
        assert min_app.name == 'trycars.app'


    def test_config_is_loaded(self, config):
        assert config['TESTING'] is True
        assert config['DEBUG'] is False
        assert config['SQLALCHEMY_DATABASE_URI'] == "sqlite:///testing.db"
        assert config['WTF_CSRF_ENABLED'] == False


    def test_request_returns_404(self, client):
        assert client.get('/not_created_route').status_code == 404


class TestDatabase:
    def test_database_created(self, populate):
        users = db.session.execute(db.select(User)).scalars().fetchall()
        assert len(users) > 0


    def test_database_users_information(self):
        users = db.session.execute(db.select(User)).scalars().fetchall()
        assert users[0].roles.name == 'admin'
        assert users[1].roles.name == 'user'


    def test_model_return_repr(self):
        users = db.session.execute(db.select(User)).scalars().fetchall()
        assert str(users[0]) == 'User(id=1, email=lucasribeiroalves@live.com, username=lribeiro)'
        assert str(users[1]) == 'User(id=2, email=lu_ks_2009@hotmail.com, username=lucasralves)'
        assert str(users[0].roles) == 'Role(id=1, name=admin, desciption=Admin User Privileges)'
        assert str(users[1].roles) == 'Role(id=2, name=user, desciption=Simple User)'


class TestHomepage:
    def test_index_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'


class TestRegisterUser:
    def test_register_page_return_200(self, client):
        assert client.get('/auth/register').status_code == 200
    

    def test_register_get_return(self, client):
        response = client.get('/auth/register')
        for string in [b'username', b'email', b'password', b'confirm password', b'recaptcha', b'register']:
            assert string in response.data
    

    def test_register_user_ok(self, client):
        data = {
            'username': 'testUser',
            'email': 'email.teste@gmail.com',
            'password': 'Testing.01234',
            'confirm_password': 'Testing.01234',
        }
        url = '/auth/register'
        
        response = client.post(url, json=data)

        new_user = db.session.execute(db.select(User).filter_by(id=3)).scalar()

        assert response.status_code == 302
        assert new_user is not None
        assert new_user.username == 'testUser'
        assert new_user.email == 'email.teste@gmail.com'
        assert new_user.roles.name == 'user'
        