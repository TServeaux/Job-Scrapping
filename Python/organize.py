import requestsData as rd
import pandas as pd
import csv

columnName = ["source", "titre", "entreprise", "lieu", "contrat",
              "salaire", "date", "lien", "description"]

def createCSV(name, columnName, offer) :
    
    with open(f'{name}.csv', "w", newline="", encoding="utf-8") as f :
        
        writer = csv.DictWriter(f, fieldnames= columnName)
        writer.writeheader()
        writer.writerows(offer)
    
    return writer

def createReport(keyword, loc, codeInsee, resN) :
    
    franceTravail = rd.searchFT(rd.getToken, keyword, codeInsee)
    wtj = rd.searchWtj(keyword, loc, resN)
    
    opport = franceTravail + wtj
    opport = createCSV("Job for " + keyword, columnName, opport)
    
    return pd.read_csv(opport)
    
def removeDuplicates(file) :
    
    return file.drop_dupplicates(None,'first')