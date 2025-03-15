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

option = 0

while True:
    try:
        option = int(input("Escolha uma opção: \n"
        "1. Ver as taxas de câmbio em Euro \n"
        "2. Escolher um valor em EUR e converter para a moeda escolhida \n"
        "3. Mostra o arquivo XML original formatado \n"
        "4. Exportar as taxas de câmbio para CSV \n"
        "5. Fechar o menu \n"))
    except ValueError:
        print("Escolha um número inteiro entre 1 e 5. \n")
        continue

    if option == 1:
        # Mostra o DataFrame
        print(dataframe, end="\n\n")
    elif option == 2:
        # Conversor de EURO para moeda escolhida
        chosen_value = float(input("Digite o valor em EUR a ser convertido: \n"))
        chosen_tax = input("Escolha a taxa de câmbio que será convertida (ex: USD, EUR): \n").upper()

        # Verifica se a moeda escolhida está entre as opções
        if chosen_tax in currency:
            index = currency.index(chosen_tax)
            tax_rate = float(rate[index])
            converted_value = round(chosen_value * tax_rate, 2)

            print(f"{chosen_value} EUR equivale a {converted_value} {chosen_tax}", end="\n\n")
        else: 
            print("Moeda não encontrada. Verifique as taxas de câmbio disponíveis e tente novamente.", end="\n\n")
    elif option == 3:
        # XML formatado:
        print(soup.prettify(), end="\n\n")
    elif option == 4:
        # Exporta o DataFrame para CSV
        dataframe.to_csv(f"euro_conversion_{date}.csv", index=False, sep=';')
        print("Exportado com sucesso.", end="\n\n")
    elif option == 5:
        break
    elif option < 0 or option > 5:
        print("Escolha uma opção válida.", end="\n\n")










