import pytest

from PS3838._utils.errors import RetrieveMatchError
from PS3838._utils.tools_code import verify_prediction

MATCH = {'id': 1593707406, 'starts': '2024-07-15T00:00:00Z', 'home': 'Argentina', 'away': 'Colombia', 'rotNum': '30805', 'liveStatus': 2, 'status': 'O', 'parlayRestriction': 2, 'altTeaser': False, 'resultingUnit': 'Regular', 'betAcceptanceType': 0, 'version': 538876225}


def test_verify_prediction_team1_wins():
    assert verify_prediction(MATCH, "Argentina", "Colombia", 1) == 1

def test_verify_prediction_team2_wins():
    assert verify_prediction(MATCH, "Argentina", "Colombia", 2) == 2

def test_verify_prediction_draw():
    assert verify_prediction(MATCH, "Argentina", "Colombia", 0) == 0

def test_verify_prediction_team1_wins_with_prediction_2():
    assert verify_prediction(MATCH, "Colombia", "Argentina", 2) == 1

def test_verify_prediction_team2_wins_with_prediction_1():
    assert verify_prediction(MATCH, "Colombia", "Argentina", 1) == 2

def test_verify_prediction_no_prediction():
    assert verify_prediction(MATCH, "Argentina", "Colombia", None) is None

def test_verify_prediction_invalid_prediction():
    with pytest.raises(RetrieveMatchError):
        verify_prediction(MATCH, "Argentina", "Colombia", 3)

def test_verify_prediction_case_insensitive():
    assert verify_prediction(MATCH, "argentina", "colombia", 1) == 1

def test_verify_prediction_with_spaces():
    assert verify_prediction(MATCH, "Argen tina", "Col ombia", 1) == 1

def test_verify_prediction_with_punctuation():
    assert verify_prediction(MATCH, "Argentina!", "Colombia!", 1) == 1

def test_verify_prediction_partial_name():
    assert verify_prediction(MATCH, "Arg", "Colom", 1) == 1

def test_verify_prediction_mismatched_team_names():
    match =  {'id': 1593707406, 'starts': '2024-07-15T00:00:00Z', 'home': 'Brazil', 'away': 'Chile', 'rotNum': '30805', 'liveStatus': 2, 'status': 'O', 'parlayRestriction': 2, 'altTeaser': False, 'resultingUnit': 'Regular', 'betAcceptanceType': 0, 'version': 538876225}
    with pytest.raises(RetrieveMatchError):
        verify_prediction(match, "Argentina", "Colombia", 1)