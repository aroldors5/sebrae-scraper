import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def raspar_cursos():
    url = "https://loja.sebraemg.com.br/loja/cursos"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    cursos = []
    cards = soup.select(".card-body")

    for card in cards:
        titulo = card.select_one("h5").text.strip() if card.select_one("h5") else ""
        cidade = card.select_one(".cidade").text.strip() if card.select_one(".cidade") else ""
        data = card.select_one(".data-curso").text.strip() if card.select_one(".data-curso") else ""
        link = "https://loja.sebraemg.com.br" + card.parent.get("href") if card.parent else ""
        cursos.append({
            "Título": titulo,
            "Cidade": cidade,
            "Data": data,
            "Link": link
        })

    return pd.DataFrame(cursos)

def atualizar_google_sheets(df):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Cursos Sebrae MG").sheet1
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

if __name__ == "__main__":
    df = raspar_cursos()
    atualizar_google_sheets(df)
