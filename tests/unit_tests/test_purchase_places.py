from ...server import app
from ..fixtures import fixture_load_clubs, fixture_load_competitions, test_dict


class TestPurchasePlaces:
    def test_success_purchase_places(self,
                                  fixture_load_clubs,
                                  fixture_load_competitions):

        response = app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places=test_dict["bookedPlaces"]))
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data


    def test_failure_purchase_places_2(self,
                                  fixture_load_clubs,
                                  fixture_load_competitions):

        response = app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places="100"))
        message = "You don't have enough points."
        assert message.encode("utf-8") in response.data

