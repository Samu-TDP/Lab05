from database.DB_connect import get_connection
from model.corso import Corso  # Importiamo il "contenitore" Corso


class CorsoDAO:

    # PDF Esercizio 1: Popolare il Dropdown iniziale
    @staticmethod
    def get_tutti_corsi():
        """Recupera tutti i corsi per popolare il menu a tendina iniziale."""

        # 1. Ottengo la connessione (usando la funzione fornita nel file DB_connect)
        cnx = get_connection()
        if cnx is None:
            return []  # Se la connessione fallisce (es. password errata), ritorno lista vuota

        # 2. Creo il cursore con dictionary=True per avere i nomi delle colonne
        cursor = cnx.cursor(dictionary=True)

        # 3. Scrivo la query SQL (non servono %s perché prendo tutto)
        query = "SELECT * FROM corso ORDER BY nome ASC"

        # 4. Eseguo la query
        cursor.execute(query)

        # 5. Inizializzo la lista dei risultati
        result = []

        # 6. Ciclo sui risultati e uso lo spacchettamento **row per istanziare l'oggetto Corso
        for row in cursor:
            result.append(Corso(**row))

        # 7. Pulizia: chiudo cursore e connessione
        cursor.close()
        cnx.close()

        return result

    # PDF Esercizio 4: Dato uno studente (matricola), trovare i corsi a cui è iscritto
    @staticmethod
    def get_corsi_by_studente(matricola):
        """Restituisce la lista di oggetti Corso a cui una determinata matricola è iscritta."""

        cnx = get_connection()
        if cnx is None:
            return []

        cursor = cnx.cursor(dictionary=True)

        # JOIN: Prendo i dati dalla tabella 'corso' collegandola alla tabella 'iscrizione'
        # Voglio solo i corsi in cui l'iscrizione ha la matricola passata come parametro.
        query = """
            SELECT c.*
            FROM corso c, iscrizione i
            WHERE c.codins = i.codins AND i.matricola = %s
        """

        # Passo la variabile 'matricola' come Tupla di un elemento (%s)
        cursor.execute(query, (matricola,))

        result = []
        for row in cursor:
            result.append(Corso(**row))

        cursor.close()
        cnx.close()

        return result