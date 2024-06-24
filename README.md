# Esercitazione Nephila

## Descrizione:

API Rest in Django per colloquio tecnico con Nephila con utilizzo della libreria Rest-Framework e Autenticazione basata su Token.

diagramma:
## Requisiti:
- Python: Versione 3.11.9 e oltre.
- Pip: 24.0 e oltre.

## Installazione del Virtual Enviroment:

È consigliato l'utilizzo di un Virtual Enviroment per evitare conflitti con i pacchetti e librerie installati globalmente.

Eseguire i seguenti comandi da terminale dopo essersi posizionati nella caretella root della repository:

Generazione virtual enviroment nella cartella root sotto la cartella **venv**:

    python3 -m venv .venv

Attivare il Virtual Enviroment:

- per **Linux** e **MacOs**:

        source .venv/bin/activate

- per **Windows**:
    - in **Cmd**:

           venv\Scripts\activate.bat
    - in **PowerShell**:

               venv\Scripts\Activate.ps1

**N.B.** Per disattivare il Virtual Enviroment al termine delle operazioni, usare il comando:

    deactivate

## Installazione del Virtual Enviroment:
per installare le dipendenze richieste dalla WebApi rimanere nella cartella root ed eseguire i seguenti comandi:

- Aggiornare Pip:

        pip install -U pip

- Installare le dipendenze presenti nel file **requirements.txt**:

        pip install -r ./requirements.txt

## Avviare la WebApi:
Una volta aver attivato il Virtual Enviroment, recarsi da terminale nella cartella **esercitazionenephila** ed eseguire i seguenti comandi:

generazione del **DB** SQLite e prima migration:

    python3 manage.py migrate

avvio dell' applicazione:

    python3 manage.py runserver

## Documentazione:

La **Documentazione** è presente come pagina **Swagger** nella **homepage** della WebApi una volta eseguita, utilizzando l'indirizzo locale e la porta 8000: http://127.0.0.1:8000/ , è oltretutto possibile visualizzare la versione **Redoc** nella pagina http://127.0.0.1:8000/redoc

## Unit testing

L' Api è testabile attraverso la Test Suit fornita da **Django**, o la documentazione **Swagger**, la suit non comprende tutti gli endpoint possibili, ma alcuni casi limiti di autenticazione e generazione, ricerca e modifica dei nodi root, per eseguire tutti i test è possibile usare il comando:

    python3 manage.py test

per eseguire un test specifico per utente o nodo tra quelli implementati, seguire la documentazione fornita in:
https://docs.djangoproject.com/en/5.0/topics/testing/overview/#running-tests


## Amministrazione e Superutenti

È possibile generare un superutente e controlalre i nodi e risorse generate utilizzando **Django admin** con il comando:

    python3 manage.py createsuperuser

ed inserendo lo username e password desiderati.

La gestione in amministrazione avviene attraverso la pagina: http://127.0.0.1:8000/admin permettendo di gestire le risorse del DB.

## UML database

È presente nel file **Diagramma db.png** .