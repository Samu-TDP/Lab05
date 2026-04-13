from database.corso_DAO import CorsoDAO
from database.studente_DAO import StudenteDAO


class Model:
    def __init__(self):
        # Questo Model non ha bisogno di mantenere uno "stato" (variabili interne persistenti)
        # tra un click e l'altro, quindi il costruttore è vuoto.
        pass

    # --- ESERCIZIO 1: Popolare il menu a tendina ---
    def get_tutti_corsi(self):
        """
        Recupera tutti i corsi dal DAO.
        Qui non applichiamo ordinamenti perché abbiamo già usato "ORDER BY nome ASC" nella query SQL.
        """
        return CorsoDAO.get_tutti_corsi()

    # --- ESERCIZIO 2: Cerca iscritti a un corso ---
    def get_iscritti_corso(self, codins):
        """
        Dato il codice di un corso, restituisce la lista degli studenti iscritti.
        Applica una logica di business: ordina gli studenti in ordine alfabetico (Cognome, Nome).
        """
        # 1. Chiediamo i dati al DAO (ci restituisce una lista di oggetti Studente)
        studenti = StudenteDAO.get_studenti_by_corso(codins)

        # 2. Logica di Business: Ordinamento Alfabetico
        # Usiamo una tupla nella lambda per ordinare PRIMA per cognome, e POI per nome a parità di cognome
        studenti.sort(key=lambda s: (s.cognome, s.nome))

        # 3. Restituiamo la lista ordinata al Controller
        return studenti

    # --- ESERCIZIO 3: Cerca studente per matricola ---
    def get_studente(self, matricola):
        """
        Cerca se uno studente esiste.
        Restituisce l'oggetto Studente se esiste, altrimenti None.
        Questa funzione serve come "controllo" per gli Esercizi 3, 4 e 5.
        """
        return StudenteDAO.get_studente_by_matricola(matricola)

    # --- ESERCIZIO 4: Cerca corsi a cui è iscritto uno studente ---
    def get_corsi_studente(self, matricola):
        """
        Data una matricola, restituisce i corsi a cui è iscritto.
        """
        # Anche qui, potremmo ordinare alfabeticamente per nome del corso
        corsi = CorsoDAO.get_corsi_by_studente(matricola)
        corsi.sort(key=lambda c: c.nome)
        return corsi

    # --- ESERCIZIO 5 (Opzionale): Iscrivi studente ---
    def iscrivi_studente(self, matricola, codins):
        """
        Tenta di iscrivere uno studente a un corso.
        Prima di disturbare il database con una INSERT, il Model fa dei controlli logici (Validazione).
        Restituisce un messaggio di testo con l'esito dell'operazione.
        """

        # CONTROLLO 1: Lo studente esiste nel database?
        studente_esiste = self.get_studente(matricola)
        if studente_esiste is None:
            return "Errore: Nessuno studente trovato con questa matricola."

        # CONTROLLO 2: Lo studente è GIÀ iscritto a questo corso?
        # Chiediamo i corsi di questo studente
        corsi_studente = self.get_corsi_studente(matricola)

        # Iteriamo sui corsi. Usiamo l'attributo .codins per il confronto.
        for corso in corsi_studente:
            if corso.codins == codins:
                return "Attenzione: Lo studente risulta già iscritto a questo corso."

        # Se passa i controlli, deleghiamo la scrittura al DAO
        successo = StudenteDAO.iscrivi_studente(matricola, codins)

        if successo:
            return "Iscrizione avvenuta con successo!"
        else:
            return "Errore imprevisto durante l'inserimento nel database."