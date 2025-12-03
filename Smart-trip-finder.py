from openai import OpenAI
from dotenv import load_dotenv
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import (
    By,
)  # Importa il metodo By per selezionare elementi
from selenium.webdriver.common.keys import (
    Keys,
)  # Importa Keys per simulare la pressione dei tasti
import time as t  # Importa il modulo time e lo rinomina come t

# importiamo un nuovo mreotod per ritardare con un tempo per unb determinato
# obbiettivo un'azione, come in questo caso aspettare che appare il tasto accetta dei cookie e accetttarlo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from enum import Enum

# OPENAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

###########################################################


def cerca_voli(luogo_p, data_p, data_r, passeggeri):

    URL = f"https://it.trip.com/flights/explore?dcity={luogo_p}&ddate={data_p}&rdate={data_r}&triptype=rt&class=y&quantity={passeggeri}&searchboxarg=t&nonstoponly=off&locale=it-IT&curr=EUR"
   
    # options = Options()
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome()
    driver.get(URL)
    t.sleep(2)
    

    cookie_button = driver.find_element(By.ID, "ibu-cookie-banner-btn-decline")
    cookie_button.click()
    t.sleep(2)

    voli_dict = {}

    lista_voli = driver.find_elements(By.CLASS_NAME, "top-list-flight")
    lista_voli = lista_voli[:5]

    for index, voli in enumerate(lista_voli):
        prezzo = voli.find_element(By.CLASS_NAME, "price").text
        luogo_destinazione = voli.find_element(
            By.CLASS_NAME, "top-list-flight__infoCity"
        ).text
        data_partenza_arrivo = voli.find_element(By.CLASS_NAME, "date").text

        voli_dict[index] = {
            "destinazione": luogo_destinazione,
            "data arrivo e partenza": data_partenza_arrivo,
            "passeggeri": passeggeri,
            "prezzo": prezzo,
        }

    t.sleep(2)

    print(voli_dict)
    ############################################################################

    voli_json = json.dumps(voli_dict, ensure_ascii=False)

    prompt_valutazione = f"Questi sono i voli trovati dal sito:\n{voli_json}\nScegli i migliori 5 voli con il prezzo più basso. Rispondi SOLO con una lista JSON di 5 elementi, ordinati dal più economico al più costoso."

    response = client.responses.create(model="gpt-4.1-nano", input=prompt_valutazione)

    print("Classifica voli migliori:")
    print(response.output_text)


####################################################################

risposta_finale = "STOP"
risposta = ""

history = [
    {
        "role": "system",
        "content": (
            "Aiutami a cercare un volo con queste istruzioni: "
            "fammi delle domande per una scelta ottimale che includa solo date e partenza, senza andare troppo nei dettagli, ma consigliandomi."
            "Questa è una lista di sigle delle città che il sito interpreta: "
            "Partenze"
            "Non scrivere più di una domanda alla volta."
            "Appena arrivi ad una soluzione, rispondi SOLO con un dizionario con chiavi: luogo_p, data_p, data_r, passeggeri(senza premesse o altro nella risposta)."
            "Se non conosci la risposta, vado fuori dall'argomento e parlo di qualcosa di non inerente alla scelta , rispondi con 'Non posso rispondere'"
        ),
    }
]


class Partenze(Enum):
    VENEZIA = "VCE"
    CATANIA = "CTA"
    TORINO = "TRN"
    NAPOLI = "NAP"
    BARI = "BRI"
    PALERMO = "PMO"
    GENOVA = "GOA"
    ALGHERO = "AHO"
    ROMA = "ROM"
    MILANO = "MIL"
    ANCONA = "AOI"
    BERGAMO = "BGY"
    BRINDISI = "BDS"
    CAGLIARI = "CAG"
    CUNEO = "CUF"
    FIRENZE = "FLR"
    LAMEZIA = "SUF"
    OLBIA = "OLB"
    PISA = "PSA"
    REGGIO_CALABRIA = "REG"
    RIMINI = "RMI"
    TRAPANI = "TPS"
    TREVISO = "TSF"
    TRIESTE = "TRS"
    VERONA = "VRN"
    BOLOGNA = "BLQ"


print(Partenze.BOLOGNA)
print(Partenze.BOLOGNA.value)


while True:
    response = client.responses.create(model="gpt-4.1-nano", input=history)
    output = response.output_text.strip()

    print("------------------------")
    print(f"Assistant: {output}")
    print("------------------------")

    try:
        dati_finali = json.loads(output)
        print("Dati finali trovati!")
        break
    except:
        pass

    risposta = input("Rispondi: ")
    history.append({"role": "user", "content": risposta})
    history.append({"role": "assistant", "content": output})


# SELENIUM

cerca_voli(
    dati_finali["luogo_p"],
    dati_finali["data_p"],
    dati_finali["data_r"],
    dati_finali["passeggeri"],
)
