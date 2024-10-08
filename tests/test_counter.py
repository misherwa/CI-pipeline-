import pytest
from src.counter import app, create_counter
from src import status

@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:

    def test_duplicate_a_counter(self, client): #
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT
    def test_create_a_counter(self, client): #sn
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_to_counter(self, client):
        re = client.post('/counters/i')
        assert re.status_code == status.HTTP_201_CREATED
        a = client.get('/counters/i')
        assert a.status_code == status.HTTP_200_OK
        base = a.get_json().get("i")
        result = client.put('/counters/i')
        assert result.status_code == status.HTTP_200_OK
        x = client.get('/counters/i')
        assert x.status_code == status.HTTP_200_OK
        update = x.get_json().get("i")
        assert update == base + 1
        
    def test_to_no_counter(self, client):
        re = client.get('/counters/missed')
        assert re.status_code == status.HTTP_404_NOT_FOUND
    def test_next_misscount(self, client):
        re = client.put('/counters/missed')
        assert re.status_code == status.HTTP_404_NOT_FOUND

    def test_to_next_counter(self, client):
        re = client.post('/counters/ex')
        assert re.status_code == status.HTTP_201_CREATED
        NextRe = client.get('/counters/ex')
        assert NextRe.status_code == status.HTTP_200_OK
        va = NextRe.get_json().get("ex")
        assert va == 0

    def test_to_delete_counter(self, client):
        re = client.post('/counters/test')
        assert re.status_code == status.HTTP_201_CREATED
        counter_delete = client.delete('/counters/test')
        assert counter_delete.status_code == status.HTTP_204_NO_CONTENT
        
    def test_delete_nonexistent_counter(self, client):
        response = client.delete('/counters/nonexistent')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    
