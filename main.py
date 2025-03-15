import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

APIurl = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

response = requests.get(APIurl)
soup = BeautifulSoup(response.content, "lxml-xml")

cube = soup.find_all("Cube", {'currency': True, 'rate': True})

original_date = soup.find("Cube", {'time': True})["time"] # Armazena a data original
date_obj = datetime.strptime(original_date, "%Y-%m-%d") # Converte para um objeto datetime
date = date_obj.strftime("%d-%m-%Y") # Transforma de 'yyyy-mm-dd' para 'dd-mm-yyyy'

currency = [] # Lista de moedas
rate = [] # Lista de taxas
rate_to_brl = [] # Lista de taxas convertidas para BRL
brl_rate = None

# Armazena os dados nas listas 'currency' e 'rate'
for moedas in cube:
    if moedas['currency'] == 'BRL':
        brl_rate = float(moedas['rate']) # Armazena o rate de BRL em euro (1 EUR = 'x' BRL)
    
    currency.append(moedas['currency'])
    rate.append(f'{float(moedas["rate"]):.2f}')

# Converte as taxas de câmbio para BRL
if brl_rate:
    for tax in rate:
        rate_to_brl.append(round(brl_rate / float(tax), 2))

# Cria o DataFrame
dataframe = pd.DataFrame({'Data de conversão de Euro': date, 'Moedas': currency, 'Taxa (Euro)': rate, 'Convertido para BRL': rate_to_brl})
print(dataframe)

# XML formatado:
print(soup.prettify())

# Exportar para CSV
dataframe.to_csv(f"euro_conversion_{date}.csv", index=False, sep=';')
