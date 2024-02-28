from trycars.ext.database.database import db
from trycars.ext.database.models import User

import pytest


class TestRegisterUser:
    url = '/auth/register'

    def test_register_page_return_200(self, client):
        assert client.get(self.url).status_code == 200


    def test_register_get_return(self, client):
        response = client.get(self.url)
        for string in [b'username', b'email', b'password', b'confirm password', b'recaptcha', b'register']:
            assert string in response.data


    def test_register_user_ok(self, client):
        data = {
            'username': 'testUser',
            'email': 'email.teste@gmail.com',
            'password': 'Testing.01234',
            'confirm_password': 'Testing.01234',
        }
        
        response = client.post(self.url, json=data)

        users = db.session.execute(db.select(User)).scalars().fetchall()
        new_user = users[-1:][0]
        print(users)
        print(new_user)

        assert response.status_code == 302
        assert len(users) == 3
        assert new_user is not None
        assert new_user.username == 'testUser'
        assert new_user.email == 'email.teste@gmail.com'
        assert new_user.roles.name == 'user'

    
    @pytest.mark.parametrize(
            ('username', 'email', 'type', 'tag'),
            (
                ('testUser', 'email.teste.novo@gmail.com', b'Username', b'testUser'),
                ('testU', 'email.teste@gmail.com', b'Email', b'email.teste@gmail.com'),
            )
    )
    def test_exclusive_username_and_email(self, client, username, email, type, tag):
        data = {
            'username': username,
            'email': email,
            'password': 'Testing.01234',
            'confirm_password': 'Testing.01234',
        }
        response = client.post(self.url, json=data)

        assert response.status_code == 200
        for string in [type, tag, b'has already been taken']:
            assert string in response.data


    @pytest.mark.parametrize(
            ('pw', 'c_pw', 'error'),
            (
                ('1234567', '1234567', b'Password must have between 8 and 30 characters.'),
                ('01234567890123456789012345678901234567890123456789', '01234567890123456789012345678901234567890123456789', b'Password must have between 8 and 30 characters.'),
                ('abcdefgh', 'abcdefgh', b'Password must have at least 1 digit.'),
                ('1abcdefgh', '1abcdefgh', b'Password must have at least one uppercase letter'),
                ('1ABCDEFGH', '1ABCDEFGH', b'Password must have at least one lowercase letter'),
                ('1ABCDEFGh', '1ABCDEFGh', b'Password must have at least one symbol'),
                ('1ABCDEf@', '1ABCDEf@', b'Password is to weak.'),
                ('QLDpoisDf@123.GDFfg', 'QLDpoisDf@123.GDFfgError', b'Password and confirmation must match'),
            )
    )
    def test_password_validation(self, client, pw, c_pw, error):
        data = {
            'username': 'tester',
            'email': 'tester@gmail.com',
            'password': pw,
            'confirm_password': c_pw,
        }
        response = client.post(self.url, json=data)

        assert error in response.data
    

    @pytest.mark.parametrize(
            ('username', 'email', 'pw', 'c_pw'),
            (
                ('', 'test@gmail.com', 'Testing@1234', 'Testing@1234'),
                ('TestUser', '', 'Testing@1234', 'Testing@1234'),
                ('TestUser', 'test@gmail.com', '', 'Testing@1234'),
            )
    )
    def test_required_fields(self, client, username, email, pw, c_pw):
        data = {
            'username': username,
            'email': email,
            'password': pw,
            'confirm_password': c_pw,
        }

        response = client.post(self.url, json=data)

        assert response.status_code == 200
        assert b'This field is required.' in response.data
        assert 1==0


    def test_mail_deliverability(self, client):
        data = {
            'username': 'New User',
            'email': 'test@test.test',
            'password': 'Testing@1234',
            'confirm_password': 'Testing@1234',
        }

        response = client.post(self.url, json=data)

        assert response.status_code == 200
        assert b'Not a valid e-mail address.' in response.data