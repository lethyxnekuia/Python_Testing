import pytest
from .. import server
from .conftest import mock_load_clubs


class TestClubsPoints:

    @pytest.mark.usefixtures(
        "fixture_load_clubs",
        "fixture_load_competitions",
        "client"
    )
    def test_clubs_points(client):

        response = server.app.test_client().get('/clubsPoints')
        assert response.status_code == 200
        assert mock_load_clubs()[0]["name"].encode("utf-8") in response.data
