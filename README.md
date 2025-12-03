# Smart Trip Finder

Questo progetto Python automatizza la ricerca dei voli tramite
**Trip.com**, utilizzando **Selenium** per la navigazione web e l'API di
**OpenAI** per classificare i risultati.

## 🚀 Funzionalità

-   Apertura automatica del browser tramite Selenium
-   Rifiuto automatico dei cookie
-   Estrazione dei primi 5 voli trovati
-   Valutazione dei voli tramite modello OpenAI (`gpt-4.1-nano`)
-   Conversazione guidata con l'utente per ottenere:
    -   Luogo di partenza
    -   Data di partenza
    -   Data di ritorno
    -   Numero di passeggeri

## 📦 Requisiti

-   Python 3.10+
-   Librerie Python:
    -   selenium
    -   python-dotenv
    -   openai
-   Chrome WebDriver installato e compatibile con la tua versione di
    Chrome

## 🔧 Configurazione

1.  Crea un file `.env` con la tua API key:

        OPENAI_API_KEY=your_api_key

2.  Installa le dipendenze:

    ``` bash
    pip install selenium python-dotenv openai
    ```

3.  Assicurati che **ChromeDriver** sia nel PATH.

## ▶️ Esecuzione

Lancia il programma con:

``` bash
python Smart-trip-finder.py
```

Segui le domande poste dal chatbot fino alla generazione dei parametri
finali.

Il sistema cercherà automaticamente i voli, li classificherà e mostrerà
i 5 migliori.

## 📁 Struttura del progetto

-   `Smart-trip-finder.py` -- Script principale
-   `.env` -- Variabili ambiente (non incluso)
-   `README.md` -- Questo file

## 📜 Note

-   Lo script utilizza Selenium in modalità non--headless per mostrare
    la pagina di ricerca.
-   Puoi modificare la parte relativa alle opzioni Chrome se desideri
    eseguirlo in headless mode.
