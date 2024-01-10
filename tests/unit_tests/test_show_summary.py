from ...server import app
from ..fixtures import fixture_load_clubs, fixture_load_competitions


class TestShowSummary:
    def test_success_show_summary(self,
                                  fixture_load_clubs,
                                  fixture_load_competitions):
        email = "john@simplylift.co"
        response = app.test_client().post('/showSummary',
                                                 data=dict(email=email))
        assert response.status_code == 200
        assert f"Welcome, {email}".encode("utf-8") in response.data

    def test_failure_show_summary(self):
        response = app.test_client()
        assert response.post('/showSummary',
                             data=dict(email="unknown@address.com")).status_code == 404