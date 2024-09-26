from datetime import datetime
from typing import Any, Dict, List, Optional

import Levenshtein

from PS3838._PS3838Retrieve import Retrieve
from PS3838._telegram.telegram_bot import CustomLogger
from PS3838._utils.constants import ID_SOCCER
from PS3838._utils.errors import RetrieveMatchError
from PS3838._utils.leagues_correspondency import CORRESPONDENCY_DICT_LEAGUES

    ##############################################
    #     Retrieve Odds For Specific Matches     #
    ##############################################

    # UNUSED FOR THE MOMENT

    # def retrieving(self, list_matches : List[Dict[str, Any]] = None) -> List[List[Dict[str, Any]]]:
    #     """
    #     This function retrieves the odds for a given list of matches. Several functions are used to find each match and their corresponding odds.
            
    #     Returns:
    #         List[List[Dict[str, Any]]]: A list of matches with their corresponding odds.
    #             Example: [({'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'rotNum': '3121', 'liveStatus': 2, 'status': 'O', 'parlayRestriction': 2, 'altTeaser': False, 'resultingUnit': 'Regular', 'betAcceptanceType': 0, 'version': 545200449, 'league': 2036, 'prediction': 1, 'amount': 5, 'odd_min': 1.05, 'line_id': 2650184231}, {'team1_odds': 1.309, 'draw_odds': 6.14, 'team2_odds': 8.47}), ...]
    #     """

    #     # Retrieve the matches
    #     matches = retrieve_specific_matches(list_matches, self.retrieve, self.logger)

    #     # Retrieve the odds for each match
    #     match_odds = []
    #     for match in matches:
    #         try:
    #             team1_odds, match["line_id"] = get_team_odds(self.retrieve, match, "Team1")
    #             team2_odds, _ = get_team_odds(self.retrieve, match, "Team2")
    #             draw_odds, _ = get_team_odds(self.retrieve, match, "Draw")
                
    #             # Append the match and odds to the list "match_odds"
    #             match_odds.append((match, 
    #                 {
    #                     "team1_odds": team1_odds,
    #                     "draw_odds": draw_odds,
    #                     "team2_odds": team2_odds,
    #                 }
    #             ))
                
    #         except Exception as e:
    #             if self.logger:
    #                 self.logger.error(f"Error retrieving odds for match {match['event_id']}: {e}")
        
    #     if self.logger:
    #         self.logger.info(f"Retrieved odds for {len(match_odds)} match(es)" if len(match_odds) > 0 else "No matches found")
    #     return match_odds


def retrieve_specific_matches(
    list_matches : List[Dict[str, Any]],
    api_retrieve : Retrieve,
    logger : Optional[CustomLogger] = None,
    *args, 
    **kwargs
) -> List[Dict[str, Any]]:
    """
    This function retrieves the matches from the list of matches provided. It retrieves the matches one by one and appends them to a list of matches found.
    
    Parameters:
        list_matches : List[Dict[str, Any]] : List of matches to retrieve.
        api_retrieve : Retrieve : API object to retrieve the matches
        logger : Optional[CustomLogger] : Logger to log the results
 
    Returns:
        matches_found : List[Dict[str, Any]] : List of matches found
    """

    # Retrieve the matches
    matches_found = []
    for match in list_matches:
        
        try : 
            # Try to find the match that corresponds to the parameters
            match_found= retrieve_match(api_retrieve, league=match["league"], name_team1=match["team1"], name_team2=match["team2"], date=match["date"] if "date" in match.keys() else None, prediction=match["prediction"] if "prediction" in match.keys() else None, amount=match["amount"] if "amount" in match.keys() else None, odd_min=match["odd_min"] if "odd_min" in match.keys() else None, logger=logger)


            # Append the match to the list of matches found
            matches_found.append(match_found)
            if logger:
                logger.info(f"Match found for {match_found['home']} - {match_found['away']}")

        except Exception as e:
            if logger:
                logger.error(f"Error retrieving match for {match['team1']} - {match['team2']} : {e}")
            continue

    return matches_found

def retrieve_match(
    api_retrieve : Retrieve,
    league : int, 
    name_team1 : str, 
    name_team2 : str, 
    date : Optional[datetime] = None, 
    prediction : Optional[int] = None,
    amount : Optional[int] = None,
    odd_min : Optional[float] = None,
    logger : Optional[CustomLogger] = None,
    *args, 
    **kwargs
) -> Dict[str, Any]:
    """
    This function retrieves a match from the API based on the parameters provided. It retrieves the leagues, the matches in the league, and then finds the match that corresponds to the parameters.
    
    Parameters:
        api_retrieve : Retrieve : API object to retrieve the matches
        league : int : ID of the league
        name_team1 : str : Name of the first team
        name_team2 : str : Name of the second team
        date : Optional[datetime] : Date of the match
        prediction : Optional[int] : prediction of the match (1 = team1 win, 2 = team2 win, 0 = draw)
        amount : Optional[int] : Amount to bet on the match
        odd_min : Optional[float] : Minimum odds to bet on the match
        logger : Optional[CustomLogger] : Logger to log the results
        
    Returns:
        match : Dict[str, Any] : Match found
    """

    # Find the ID of the league
    league_id = find_league_id_PS3838(league, logger)

    # Find the matches in the league
    fixtures = api_retrieve.get_fixtures_v3(sport_id=ID_SOCCER, league_ids=[league_id])

    # Keep only the elements where 'statut' = 'O' which means the match is open
    fixtures = [match for match in fixtures["league"][0]["events"] if match["status"] == "O"]

    print(fixtures)

    # Find the match
    match = find_match(fixtures, name_team1, name_team2, date, logger)

    # Verify if the parameter prediction is correct
    prediction = verify_prediction(match, name_team1, name_team2, prediction, logger)

    # Add the league ID to the match, the prediction, the amount and the minimum odds that are fundamentals parameters if we want to bet afterwards
    match["league"] = league_id
    match["prediction"] = prediction
    match["amount"] = amount
    match["odd_min"] = odd_min

    return match

def normalize_name(name : str) -> str:
    """
    This function normalizes a name by removing all special characters and converting it to lowercase.
    """
    return ''.join(e for e in name.lower() if e.isalnum())


def find_best_match(name: str, candidates: list[str], cutoff : float = 0.5) -> str:
    """
    This function finds the best match for a name in a list of candidates. It uses the Levenshtein distance to calculate the similarity between the name and the candidates. It is useful when the name of sport_api is not exactly the same as the name on PS3838. The cutoff parameter is used to filter the candidates that are too different from the name.
    """
    normalized_name = normalize_name(name)
    normalized_candidates = [normalize_name(candidate) for candidate in candidates]

    best_match = None
    highest_similarity = -1

    for candidate in normalized_candidates:
        similarity = Levenshtein.ratio(normalized_name, candidate)
        if similarity > highest_similarity and similarity >= cutoff:
            highest_similarity = similarity
            best_match = candidate

    if best_match:
        best_match_index = normalized_candidates.index(best_match)
        return candidates[best_match_index]

    return None

def find_match(
    fixtures : list[Dict[str, Any]], 
    name_team1 : str, 
    name_team2 : str, 
    date : datetime = None, 
    logger : CustomLogger = None
) -> Dict[str, Any]:
    """
    This function finds the match that corresponds to the team names and the date provided. It first tries to have the perfect match between team1 and team2 and the date, and then tries a lighter version without the date.
    
    Parameters:
        fixtures : list[Dict[str, Any]] : List of available matches returned by PS3838.
        name_team1 : str : Name of the first team
        name_team2 : str : Name of the second team
        date : datetime : Date of the match
        logger : CustomLogger : Logger to log the predictions
        
    Returns:
        match : Dict[str, Any] : Match found
    """
    # Find the candidates for the team names
    candidates_home = []
    candidates_away = []
    for match in fixtures:
        candidates_home.append(match["home"])
        candidates_away.append(match["away"])

    match = None
    # Find the match
    for fixture in fixtures:
        if (find_best_match(name_team1, candidates_home) == fixture["home"] and find_best_match(name_team2, candidates_away) == fixture["away"]) or (find_best_match(name_team1, candidates_away) == fixture["away"] and find_best_match(name_team2, candidates_home) == fixture["home"]) and datetime.fromisoformat(fixture["starts"].replace('Z','')) == date:
            match = fixture
            break
        elif (find_best_match(name_team1, candidates_home) == fixture["home"] and find_best_match(name_team2, candidates_away) == fixture["away"]) or (find_best_match(name_team1, candidates_away) == fixture["away"] and find_best_match(name_team2, candidates_home) == fixture["home"]):
            match = fixture
            break
        
    if not match:
        if logger:
            logger.error(f"Match not found for {name_team1} - {name_team2}")
        raise RetrieveMatchError("Match not found")
    
    return match


def verify_prediction(
    match : Dict[str, Any],
    name_team1 : str, 
    name_team2 : str, 
    prediction : int, 
    logger : CustomLogger = None
) -> int:
    """
    This function verifies if the prediction corresponds to the home team or the away team, and changes it if necessary.
    For example if we entered Marseille - Lens with prediction 1 and the actual match is Lens - Marseille, the function will return 2.
    
    Parameters:
        match : Dict[str, Any] : Match found
        name_team1 : str : Name of the first team
        name_team2 : str : Name of the second team
        prediction : int : prediction of the match (1 = team1 win, 2 = team2 win, 0 = draw)
        logger : CustomLogger : Logger to log the results
        
    Returns:
        int : 1 if the prediction corresponds to the home team, 2 if the prediction corresponds to the away team, 0 if the prediction corresponds to a draw
    """
    if prediction is not None:
        if prediction == 1:
            if (find_best_match(match["home"], [name_team1, name_team2]) == name_team1) and (find_best_match(match["away"], [name_team1, name_team2]) == name_team2):
                return 1
            elif (find_best_match(match["away"], [name_team1, name_team2]) == name_team1) and (find_best_match(match["home"], [name_team1, name_team2]) == name_team2):
                return 2
            elif (find_best_match(match["home"], [name_team1, name_team2]) == name_team1) or (find_best_match(match["away"], [name_team1, name_team2]) == name_team2):
                return 1
            elif (find_best_match(match["away"], [name_team1, name_team2]) == name_team1) or (find_best_match(match["home"], [name_team1, name_team2]) == name_team2):
                return 2
            else:
                if logger:
                    logger.error(f"Error while verifying if the prediction 1 corresponds to the home team")
                raise RetrieveMatchError("Error while verifying if the prediction 1 corresponds to the home team")
        elif prediction == 2:
            if (find_best_match(match["home"], [name_team1, name_team2]) == name_team1) and (find_best_match(match["away"], [name_team1, name_team2]) == name_team2):
                return 2
            elif (find_best_match(match["away"], [name_team1, name_team2]) == name_team1) and (find_best_match(match["home"], [name_team1, name_team2]) == name_team2):
                return 1
            elif (find_best_match(match["home"], [name_team1, name_team2]) == name_team1) or (find_best_match(match["away"], [name_team1, name_team2]) == name_team2):
                return 2
            elif (find_best_match(match["away"], [name_team1, name_team2]) == name_team1) or (find_best_match(match["home"], [name_team1, name_team2]) == name_team2):
                return 1
            else:
                if logger:
                    logger.error(f"Error while verifying if the prediction 2 corresponds to the home team")
                raise RetrieveMatchError("Error while verifying if the prediction 2 corresponds to the home team")
        else:
            return 0
    else:
        return None
    
def find_league_id_PS3838(league_id_sport_api : int, logger : CustomLogger = None) -> int:
    """
    This function finds the league ID of PS3838 from the league ID of the sport API. It is useful to find the correct league to place the bets.
    
    Parameters:
        league_id_sport_api : int : League ID of the sport API
        logger : CustomLogger : Logger to log the results
        
    Returns:
        int : League ID of PS3838
    """
    for _, associations in CORRESPONDENCY_DICT_LEAGUES.items():
        for association_sport_api, association_ps3838 in associations.items():
            if association_sport_api[1] == league_id_sport_api:
                return association_ps3838[1]
    if logger:
        logger.error(f"League correspondency not found")
    raise RetrieveMatchError("League correspondency not found")