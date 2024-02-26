

def test_app_is_created(min_app):
    assert min_app.name == 'trycars.app'


def test_config_is_loaded(config):
    assert config['DEBUG'] is False


def test_request_returns_404(client):
    response = client.get('/not_created_route')
    assert response.status_code == 404