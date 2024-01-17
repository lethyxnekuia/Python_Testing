import pytest 
from ..server import app

test_dict = {
    "name": "Face Lift",
    "email": "john@simplylift.co",
    "points": "50",
    "competition": "Spring Festival",
    "date": "2024-03-27 10:00:00",
    "numberOfPlaces": "25",
    "bookedPlaces": "2"
}


class TestPurchasePlaces:
    @pytest.mark.usefixtures("fixture_load_clubs", "fixture_load_competitions", "client")
    def test_success_purchase_places(client):

        response = app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places=test_dict["bookedPlaces"]))
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        remaining_clubs_points = int(test_dict["points"]) - int(test_dict["bookedPlaces"])
        remaining_clubs_points = "Points available: " + str(remaining_clubs_points)
        print(response.data)
        assert remaining_clubs_points.encode("utf-8") in response.data
        remaining_competition_places = int(test_dict["numberOfPlaces"]) - int(test_dict["bookedPlaces"])
        remaining_competition_places = "Number of Places: " + str(remaining_competition_places)
        assert remaining_competition_places.encode("utf-8") in response.data


    def test_failure_purchase_more_places_than_points(client):

        response = app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places="100"))
        message = "You have not enough points."
        assert message.encode("utf-8") in response.data

    def test_failure_purchase_more_than_twelves_places(client):
        response = app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places="13"))
        message = "You can not book more than 12 places"
        assert message.encode("utf-8") in response.data

    def test_failure_purchase_old_event(client):
        response = app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition="Fall Classic",
                                                           places="1"))
        message = "This event has passed"
        assert message.encode("utf-8") in response.data

