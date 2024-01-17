from ... import server
from ..fixtures import mock_load_clubs, fixture_load_clubs

class TestClubsPoints:
    def test_clubs_points(self, fixture_load_clubs):

        response = server.app.test_client().get('/clubsPoints')
        assert response.status_code == 200
        assert mock_load_clubs()[0]["name"].encode("utf-8") in response.data