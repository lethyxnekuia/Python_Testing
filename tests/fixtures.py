import pytest

def mock_load_clubs():
    list_of_clubs = [
        {
            "name": "Face Lift",
            "email": "johnsteed@hotmail.com",
            "points": "50"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
    return list_of_clubs


@pytest.fixture
def fixture_load_clubs(monkeypatch):
    monkeypatch.setattr('Python_Testing.server.clubs', mock_load_clubs())


def mock_load_competitions():
    list_of_competitions = [
        {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
    return list_of_competitions


@pytest.fixture
def fixture_load_competitions(monkeypatch):
    monkeypatch.setattr('Python_Testing.server.competitions', mock_load_competitions())