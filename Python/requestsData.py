import requests 
import json

def getKey(path):
    """
    Loads and returns the content of a JSON file.

    Args:
        path (str) : Path to the JSON file.

    Returns:
        dict : Parsed content of the JSON file.
    """

    with open(path,'r',encoding='utf-8') as d:
        data = json.load(d)
    
    return data


def getToken():

    """
    Authenticates to the France Travail API using OAuth2 client credentials
    and returns an access token.

    Returns:
        str : Bearer access token valid for 30 minutes.

    Raises:
        HTTPError : If the authentication request fails.
    """

    client = getKey("./data/user.json") #Change here and put ./data/userKeys.json

    response = requests.post(

        "https://entreprise.francetravail.fr/connexion/oauth2/access_token",

        params={
            "realm": "/partenaire"  
        },

        headers={
            "Content-Type": "application/x-www-form-urlencoded"  
        },

        data={                             
            "grant_type":    "client_credentials",
            "client_id":     client['franceTravail']['userId'],
            "client_secret": client['franceTravail']['userAcces'],
            "scope":         "api_offresdemploiv2 o2dsoffre"
        }
    )

    response.raise_for_status()

    return response.json()["access_token"]

def searchFT(token, keyWord, codeInsee) :

    """
    Searches for job offers on the France Travail API.

    Args:
        token (str)     : Bearer access token obtained from getToken().
        keyWord (str)   : Job title or keyword to search for.
        codeInsee (str) : French department code to filter by location (e.g. '69').

    Returns:
        list : List of raw job offer dicts returned by the API.

    Raises:
        HTTPError : If the API request fails.
    """
    
    response = requests.get(
        
        "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search",
                            
        headers={
            "Authorization": f"Bearer {token}",
            "Accept":        "application/json"
        },

        params={
            "motsCles": keyWord,
            "departement":  codeInsee,
            "range":    "0-9"
        }
    )

    response.raise_for_status()

    return response.json().get("resultats", [])

def searchWtj(keyWord, loc, resN):

    """
    Searches for job offers on the Adzuna API.

    Args:
        keyWord (str) : Job title or keyword to search for.
        loc (str)     : City or region name to filter by location (e.g. 'Lyon').
        resN (int)    : Number of results to return per page.

    Returns:
        list : List of raw job offer dicts returned by the API.

    Raises:
        HTTPError : If the API request fails.
    """

    client = getKey("./data/user.json")

    response = requests.get(

        "https://api.adzuna.com/v1/api/jobs/fr/search/1",

        params={
            "app_id":           client['wtj']['userId'],
            "app_key":          client['wtj']['userAcces'],
            "what":             keyWord,
            "where":            loc,
            "results_per_page": resN,
            "sort_by":          "date"
        }
    )

    response.raise_for_status()

    return response.json().get("results", [])