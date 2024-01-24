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


class TestIntegration:
    @pytest.mark.usefixtures(
        "fixture_load_clubs",
        "fixture_load_competitions",
        "client"
    )
    def test_integration(client):
        # Try to connect with an unknown email
        response = app.test_client()
        assert response.post(
            '/showSummary',
            data=dict(email="unknown@address.com")
        ).status_code == 404

        # Try to connect with a good email
        email = "john@simplylift.co"
        response = app.test_client().post(
            '/showSummary',
            data=dict(email=email)
        )
        assert response.status_code == 200
        assert f"Welcome, {email}".encode("utf-8") in response.data

        # Try to get 2 tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club=test_dict["name"],
                competition=test_dict["competition"],
                places=test_dict["bookedPlaces"]
            )
        )
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        clubs_points = int(
            test_dict["points"]) - int(test_dict["bookedPlaces"])
        clubs_points = "Points available: " + str(clubs_points)
        assert clubs_points.encode("utf-8") in response.data
        competition_places = int(
            test_dict["numberOfPlaces"]) - int(test_dict["bookedPlaces"])
        competition_places = "Number of Places: " + str(competition_places)
        assert competition_places.encode("utf-8") in response.data

        # Try to get 100 tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club=test_dict["name"],
                competition=test_dict["competition"],
                places="100"
            )
        )
        message = "You have not enough points."
        assert message.encode("utf-8") in response.data

        # try to get more than 12 tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club=test_dict["name"],
                competition=test_dict["competition"],
                places="13"
                )
            )
        message = "You can not book more than 12 places"
        assert message.encode("utf-8") in response.data

        # try to get tickets for an old event
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club=test_dict["name"],
                competition="Fall Classic",
                places="1"
                )
            )
        message = "This event has passed"
        assert message.encode("utf-8") in response.data

        # another person try to connect
        email = "admin@irontemple.com"
        response = app.test_client().post(
            '/showSummary',
            data=dict(email=email)
        )
        assert response.status_code == 200
        assert f"Welcome, {email}".encode("utf-8") in response.data

        # Try to get 5 tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club="Iron Temple",
                competition=test_dict["competition"],
                places="5"
            )
        )
        message = "You have not enough points."
        assert message.encode("utf-8") in response.data

        # Try to get 2 tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club="Iron Temple",
                competition=test_dict["competition"],
                places=test_dict["bookedPlaces"]
            )
        )
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        clubs_points = 4 - int(test_dict["bookedPlaces"])
        clubs_points = "Points available: " + str(clubs_points)
        assert clubs_points.encode("utf-8") in response.data
        competition_places = int(
            test_dict["numberOfPlaces"]) - int(test_dict["bookedPlaces"]) - 2
        competition_places = "Number of Places: " + str(competition_places)
        assert competition_places.encode("utf-8") in response.data

        # Try to get 3 more tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club="Iron Temple",
                competition=test_dict["competition"],
                places="5"
            )
        )
        message = "You have not enough points."
        assert message.encode("utf-8") in response.data

        # Try to get 2 tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club="Iron Temple",
                competition=test_dict["competition"],
                places=test_dict["bookedPlaces"]
            )
        )
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        clubs_points = 0
        clubs_points = "Points available: " + str(clubs_points)
        assert clubs_points.encode("utf-8") in response.data
        competition_places = int(
            test_dict["numberOfPlaces"]) - int(test_dict["bookedPlaces"]) - 4
        competition_places = "Number of Places: " + str(competition_places)
        assert competition_places.encode("utf-8") in response.data

        # the first User try to get 2 more tickets
        response = app.test_client().post(
            '/purchasePlaces',
            data=dict(
                club=test_dict["name"],
                competition=test_dict["competition"],
                places=test_dict["bookedPlaces"]
            )
        )
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        clubs_points = int(
            test_dict["points"]) - int(test_dict["bookedPlaces"]) - 2
        clubs_points = "Points available: " + str(clubs_points)
        assert clubs_points.encode("utf-8") in response.data
        competition_places = int(
            test_dict["numberOfPlaces"]) - int(test_dict["bookedPlaces"]) - 6
        competition_places = "Number of Places: " + str(competition_places)
        assert competition_places.encode("utf-8") in response.data
