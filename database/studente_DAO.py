from database.DB_connect import get_connection
from model.studente import Studente  # Importiamo il "contenitore" Studente


class StudenteDAO:

    # PDF Esercizio 2: Dato un corso, trova gli iscritti
    @staticmethod
    def get_studenti_by_corso(codins):
        """Restituisce la lista di studenti iscritti a uno specifico corso."""

        cnx = get_connection()
        if cnx is None:
            return []

        cursor = cnx.cursor(dictionary=True)

        # JOIN tra studente e iscrizione.
        query = """
            SELECT s.*
            FROM studente s, iscrizione i
            WHERE s.matricola = i.matricola AND i.codins = %s
        """

        # Sostituisco il %s con il parametro codins passato dalla funzione
        cursor.execute(query, (codins,))

        result = []
        for row in cursor:
            # Ogni riga (row) è un dizionario {"matricola": 123, "nome": "Mario", ...}
            # **row lo scompatta in Studente(matricola=123, nome="Mario", ...)
            result.append(Studente(**row))

        cursor.close()
        cnx.close()

        return result

    # PDF Esercizio 3: Cercare uno studente per matricola (esiste o no?)
    @staticmethod
    def get_studente_by_matricola(matricola):
        """Cerca uno studente specifico data la sua matricola.
        Restituisce un OGGETTO Studente se lo trova, oppure None se non esiste."""

        cnx = get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)

        # Cerco la matricola nella tabella studente
        query = "SELECT * FROM studente WHERE matricola = %s"
        cursor.execute(query, (matricola,))

        studente_trovato = None
        # Siccome la matricola è chiave primaria, la query restituirà al massimo UNA riga
        for row in cursor:
            studente_trovato = Studente(**row)

        cursor.close()
        cnx.close()

        # Restituisco l'oggetto Python (oppure None se il ciclo for non è mai partito)
        return studente_trovato

    # PDF Esercizio 5 (Opzionale): Iscrivere uno studente a un corso
    @staticmethod
    def iscrivi_studente(matricola, codins):
        """Inserisce una nuova riga nella tabella 'iscrizione'.
        Ritorna True se l'inserimento ha successo, False in caso di errori (es. era già iscritto)."""

        cnx = get_connection()
        if cnx is None:
            return False

        cursor = cnx.cursor()  # Qui dictionary=True non serve, perché non dobbiamo "leggere" dati

        # Query di INSERIMENTO.
        # IGNORARE i duplicati in modo elegante: se provi a iscrivere uno studente che
        # è già iscritto, MySQL andrebbe in crash (Primary Key Violata).
        # Usando INSERT IGNORE, MySQL non dà errore, ma semplicemente non inserisce la riga doppia.
        query = "INSERT IGNORE INTO iscrizione (matricola, codins) VALUES (%s, %s)"

        try:
            # Qui abbiamo DUE %s, quindi la tupla deve avere due valori in quest'ordine esatto!
            cursor.execute(query, (matricola, codins))

            # FONDAMENTALE QUANDO SI SCRIVE SUL DATABASE:
            # cnx.commit() salva in via definitiva le modifiche sul disco del server.
            # Senza questa riga, la query viene eseguita ma annullata appena chiudi la connessione!
            cnx.commit()

            # cursor.rowcount ci dice quante righe sono state aggiunte effettivamente.
            # Se è 0, significa che era già iscritto (grazie a IGNORE).
            if cursor.rowcount > 0:
                successo = True
            else:
                successo = False

        except Exception as e:
            print(f"Errore durante l'inserimento: {e}")
            successo = False

        finally:
            # Blocco finally si esegue SEMPRE, sia che il try vada a buon fine, sia che ci sia un except
            cursor.close()
            cnx.close()

        return successo
