import requestsData as rd
import pandas as pd
import os
import csv

columnName = ["source", "titre", "entreprise", "lieu", "contrat",
              "salaire", "date", "lien", "description"]

def createCSV(name, columnName, offer) :

    filepath = f"./output/{name}Jobs.csv"
    
    with open(filepath, "w", newline="", encoding="utf-8") as f :
        
        writer = csv.DictWriter(f, fieldnames = columnName, extrasaction = 'ignore')
        writer.writeheader()
        writer.writerows(offer)
    
    return filepath

def formater_ft(offre):
    return {
        "source":      "France Travail",
        "titre":       offre.get("intitule", ""),
        "entreprise":  offre.get("entreprise", {}).get("nom", "N/A"),  # ← extrait juste le nom
        "lieu":        offre.get("lieuTravail", {}).get("libelle", ""),
        "contrat":     offre.get("typeContratLibelle", ""),
        "salaire":     offre.get("salaire", {}).get("libelle", "Non précisé"),
        "date":        offre.get("dateCreation", "")[:10] if offre.get("dateCreation") else "",
        "lien":        offre.get("origineOffre", {}).get("urlOrigine", ""),
        "description": offre.get("description", "")[:300] if offre.get("description") else ""
    }

def formater_adzuna(offre):
    return {
        "source":      "Adzuna",
        "titre":       offre.get("title", ""),
        "entreprise":  offre.get("company", {}).get("display_name", "N/A"),
        "lieu":        offre.get("location", {}).get("display_name", ""),
        "contrat":     offre.get("contract_time", ""),
        "salaire":     f"{int(offre['salary_min'])}€ - {int(offre['salary_max'])}€" if offre.get("salary_min") else "Non précisé",
        "date":        offre.get("created", "")[:10] if offre.get("created") else "",
        "lien":        offre.get("redirect_url", ""),
        "description": offre.get("description", "")[:300] if offre.get("description") else ""
    }

def createReport(keyword, loc, codeInsee, resN) :
    
    franceTravail = rd.searchFT(rd.getToken(), keyword, codeInsee)
    wtj = rd.searchWtj(keyword, loc, resN)
    
    opport = [formater_ft(o) for o in franceTravail] + \
             [formater_adzuna(o) for o in wtj]

    opport = createCSV(keyword, columnName, opport)
    opport = pd.read_csv(opport).drop_duplicates(subset= ["titre", "entreprise", "lieu"] ,keep= 'first')
    
    return opport
