import requestsData as rd
import pandas as pd
import os
import csv

columnName = ["source", "titre", "entreprise", "lieu", "contrat",
              "salaire", "date", "lien", "description"]

def createCSV(name, columnName, offer) :

    """
    Creates a CSV file in the ./output directory with the given offers.

    Args:
        - name (str)         : Name of the file.
        - columnName (list)  : List of column names to include in the CSV.
        - offer (list)       : List of dicts representing job offers.

    Returns:
        - filepath (str) : Path to the created CSV file.
    """

    filepath = f"./output/{name}Jobs.csv"
    
    with open(filepath, "w", newline="", encoding="utf-8") as f :
        
        writer = csv.DictWriter(f, fieldnames = columnName, extrasaction = 'ignore')
        writer.writeheader()
        writer.writerows(offer)
    
    return filepath

def formatFt(offer):
    """
    Formats a raw France Travail job offer into a standardized dict.

    Args:
        offer (dict) : Raw job offer returned by the France Travail API.

    Returns:
        dict : Formatted job offer with keys matching columnName.
    """

    return {
        "source":      "France Travail",
        "titre":       offer.get("intitule", ""),
        "entreprise":  offer.get("entreprise", {}).get("nom", "N/A"),  # ← extrait juste le nom
        "lieu":        offer.get("lieuTravail", {}).get("libelle", ""),
        "contrat":     offer.get("typeContratLibelle", ""),
        "salaire":     offer.get("salaire", {}).get("libelle", "Non précisé"),
        "date":        offer.get("dateCreation", "")[:10] if offer.get("dateCreation") else "",
        "lien":        offer.get("origineOffre", {}).get("urlOrigine", ""),
        "description": offer.get("description", "")[:300] if offer.get("description") else ""
    }

def formatAdzuna(offer):
    """
    Formats a raw Adzuna job offer into a standardized dict.

    Args:
        offer (dict) : Raw job offer returned by the Adzuna API.

    Returns:
        dict : Formatted job offer with keys matching columnName.
    """
    return {
        "source":      "Adzuna",
        "titre":       offer.get("title", ""),
        "entreprise":  offer.get("company", {}).get("display_name", "N/A"),
        "lieu":        offer.get("location", {}).get("display_name", ""),
        "contrat":     offer.get("contract_time", ""),
        "salaire":     f"{int(offer['salary_min'])}€ - {int(offer['salary_max'])}€" if offer.get("salary_min") else "Non précisé",
        "date":        offer.get("created", "")[:10] if offer.get("created") else "",
        "lien":        offer.get("redirect_url", ""),
        "description": offer.get("description", "")[:300] if offer.get("description") else ""
    }

def createReport(keyword, loc, codeInsee, resN) :
    """
    Fetches job offers from France Travail and Adzuna, merges them,
    removes duplicates and saves the result as a CSV file.

    Args:
        keyword (str)  : Job title or keyword to search for.
        loc (str)      : City or region name for Adzuna (e.g. 'Lyon').
        codeInsee (str): Department code for France Travail (e.g. '69').
        resN (int)     : Number of results to fetch from Adzuna.

    Returns:
        DataFrame : Cleaned and deduplicated job offers.
    """
    
    franceTravail = rd.searchFT(rd.getToken(), keyword, codeInsee)
    wtj = rd.searchWtj(keyword, loc, resN)
    
    opport = [formatFt(i) for i in franceTravail] + \
             [formatAdzuna(i) for i in wtj]

    opport = createCSV(keyword, columnName, opport)
    opport = pd.read_csv(opport).drop_duplicates(subset= ["titre", "entreprise", "lieu"] ,keep= 'first')
    
    return opport
