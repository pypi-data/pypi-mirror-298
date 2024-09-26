# BET PS3838

## Introduction

**BET PS3838** This project aims to bet automatically on different odds available on PS3838. It is part of a bigger secret project, but can be used by anyone who wants to place some bets, or retrieve some football odds (indeed, only football for the moment).


## Package functionalities

There are two classes in the package called "PS3838RetrieveOdds" and "PS3838AutomatedBets"

- **PS3838RetrieveOdds** :
    This class is used to retrieve the odds for a list of matches or to place bets on the PS3838 API. It also uses a CustomLogger to log the information.
    
        Parameters:
            - credentials (Dict[str, str]): The credentials to connect to the PS3838 API. 
                Example: {"username": "my_username", "password": "my_password"}
            - list_matches (List[Dict[str, Any]]): A list of matches to retrieve the odds for or to place the bets for.
                Example: [{"league" : 2036, "team1" : "Montpellier", "team2" : "Paris Saint-Germain", "date" : datetime(2024, 8, 17, 17, 0, 0), "prediction" : 2, "amount" : 5, "odd_min" : 1.05}, ...]. Note that the parameters "prediction", "amount" and "odd_min" are optional and only used when placing bets.
            - logger_active (bool): A boolean to activate the logger. Default is True.
            - to_bet (bool): A boolean to know if we want to retrieve the odds or place the bets. Default is False.

- **PS3838RetrieveOdds** :
    This class is used to retrieve the odds from the PS3838 API. It uses the Retrieve class to connect to the API and retrieve the odds for each match. It also uses a CustomLogger to log the information.
        
        Parameters:
            config (Dict[str, str]): The config to connect to the PS3838 API.
                Example: {"username": "my_username", "password": "my_password"}
            logger_active (bool): A boolean to activate the logger. Default is True.
            logger_name (str): The name of the log file. Default is "PS3838.log".

    The main function in this class is "retrieving()". This function retrieves the odds for all the matches until a given date and for a given list of leagues.

        Parameters:
            until_date (datetime): The date until which we want to retrieve the matches. Default is None, it retrieves everything in the specified leagues.
            leagues (List[int]): A list of leagues for which we want to retrieve the matches. Default is None, it retrieves every league until the date specified.

        Returns:
            List[List[Dict[str, Any]]]: A list of matches with their corresponding odds.
                Example: [{'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'league': 2036, 'line_id': 2650184231, 'odds': {'home': 1.309, 'draw': 6.14, 'away': 8.47}}, ...]
    

- **PS3838AutomatedBets** : 
    This class is used to place bets on the PS3838 API. It uses the Bet classes to connect to the API and place the bets. It also uses a CustomLogger to log the information.
        
        Parameters:
            config (Dict[str, str]): The config to connect to the PS3838 API. 
                Example: {"username": "my_username", "password": "my_password"}
            list_matches (List[Dict[str, Any]]): A list of matches to bet on.
                Example: 
                    [{'id': 1596465583, 'starts': '2024-09-04T17:45:00Z', 'home': 'Resende FC', 'away': 'Artsul', 'league': 216059, 'line_id': 2673459336, 'odds': {'Team1': 2.05, 'Team2': 3.1, 'Draw': 3.25}, 'prediction': 1, 'amount': 5},
                    {'id': 1596465586, 'starts': '2024-09-04T17:45:00Z', 'home': 'Fluminense', 'away': 'AF Perolas Negras', 'league': 216059, 'line_id': 2673462355, 'odds': {'Team1': 1.159, 'Team2': 11.83, 'Draw': 5.83}, 'prediction': 0, 'amount': 5}, ...].
            logger_active (bool): A boolean to activate the logger. Default is True.
            to_bet (bool): A boolean to know if we really want to bets. Default is False, useful for testing the code.

    The main function in this class is "betting()". This function places bets on the PS3838 API for a given list of matches, if the bets are not already placed and if the maintenance is not in progress.
 
        Returns:
            List[List[Dict[str, Any]]] | None: A list of matches with their corresponding odds if the bets were placed, None otherwise.
                Example: [{'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'league': 2036, 'line_id': 2650184231, 'odds': {'home': 1.309, 'draw': 6.14, 'away': 8.47}}, ...]


## How to use the package

Here is an example of code to use the package

```python
import PS3838

# CREDENTIALS PART
config = {'username': 'gagou', 'telegram': {'token': 'YOUR_TELEGRAM_TOKEN', 'chat_id': 'YOUR_TELEGRAM_CHAT_ID'}, 'ps3838': {'username': 'YOUR_USERNAME_PS3838', 'password': 'YOUR_PASSWORD_ps3838'}, 'db': {'db_bets': {'root_password': 'ROOT_PASSWORD', 'host': 'localhost', 'name': 'bet_db', 'user': 'user', 'password': 'PASSWORD'}, 'db_preds': {'host': 'IP_ADDRESS', 'port': '5432', 'name': 'football', 'user': 'postgres', 'password': 'PASSWORD'}}, 'strategy': {'leagues': [2036, 4867], 'criterion': 'kelly', 'min_amount': 5}}


# MATCHES PART
match1 = {
    'id': 1596236279, 
    'starts': '2024-09-14T19:00:00Z',
    'home': 'Paris Saint-Germain', 
    'away': 'Brest', 
    'league': 2036, 
    'line_id': 2673340912, 
    'odds': {'home': 1.296, 'away': 8.56, 'draw': 5.91},
    'prediction': 1,
    'amount': 5,
}
match2 = {
    #league = 61
    "league" : 61,
    "team1" : "Marseille",
    "team2" : "Nice",
    "prediction" : 1,
    "amount" : 5,
}


matches = [match1]


# BETTING PART
betting_object = PS3838.PS3838AutomatedBets(config, list_matches=matches, logger_active=True, to_bet=False)
matches_status = betting_object.betting()
print(matches_status)

# RETRIEVE PART
retrieve_object = PS3838.PS3838RetrieveOdds(config, logger_active=True)
matches_odds = retrieve_object.retrieving(leagues=[2036])
print(matches_odds)

# BANKROLL PART
bankroll_object = PS3838.PS3838RetrieveBankroll(config, logger_active=True)
bankroll = bankroll_object.retrieve_bankroll()
print(bankroll)
```


## Logger

You can activate or desactivate the logger with the parameter "logger_active" when instantiating.
- If the logger is active and a telegram token and chat id are provided in the config dict, then you will receive the logs on your telegram chatbot and on a PS3838.log file. (On telegram there are only the logs up to "INFO", not "DEBUG".)
- If the logger is active and the telegram parameters are missing, then you will receive the logs only on a PS3838.log file.
- If the logger is not active then you will not receive anything.

Here is an example of what the logger can display on Telegram : 

![Example of telegram logs](PS3838/_images/image_telegram.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

