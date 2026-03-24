import requests 
import json

def getKey(data):

    with open(data,'r',encoding='utf-8') as d:
        data = json.load(d)
    
    return data


def getToken():

    client = getKey("./data/user.json")

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

def searchJob(token, keyWord, codeInsee, distance) :
    
    response = requests.get("https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search",
                            
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

    print("URL appelée:", response.url)
    print("Status offres:", response.status_code)
    print("Détail:", response.text)
    response.raise_for_status()

    return response.json().get("resultats", [])

print(searchJob(getToken(),"python","69",30))