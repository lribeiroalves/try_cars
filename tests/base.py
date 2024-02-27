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