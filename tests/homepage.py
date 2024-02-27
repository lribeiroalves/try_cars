class TestHomepage:
    def test_index_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'