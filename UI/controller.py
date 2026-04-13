import flet as ft


class Controller:
    def __init__(self, view, model):
        # 1. Il Controller si salva in tasca i riferimenti a View e Model
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # --- ESERCIZIO 1: Popolare i Corsi all'avvio ---
    def riempi_dd_corsi(self):
        """Metodo chiamato dalla View appena si accende il programma."""
        # Chiediamo al Model tutti i corsi
        corsi = self._model.get_tutti_corsi()

        # Per ogni corso, creiamo un'opzione nel menu a tendina
        for c in corsi:
            # Usiamo il trucco del "Cavallo di Troia": mostriamo il nome del corso,
            # ma nascondiamo l'intero oggetto Corso dentro l'attributo 'data'
            self._view.dd_corso.options.append(ft.dropdown.Option(
                key=c.codins,  # Quello che il programma userà come ID univoco
                text=c.nome,  # Quello che l'utente VEDE scritto nella tendina
                data=c  # Il carico nascosto (L'intero oggetto Python!)
            ))

        # Non serve update_page() qui, perché la View lo fa già alla fine di load_interface

    # --- ESERCIZIO 2: Cerca iscritti a un corso ---
    def handle_cerca_iscritti(self, e):
        # 1. Pulizia lavagna
        self._view.txt_result.controls.clear()

        # 2. Lettura input
        codins = self._view.dd_corso.value

        # 3. Validazione
        if codins is None:
            self._view.create_alert("Attenzione: devi prima selezionare un corso dal menu a tendina!")
            return

        # 4. Chiamata al Model
        studenti = self._model.get_iscritti_corso(codins)

        # 5. Stampa dei risultati
        if len(studenti) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuno studente iscritto a questo corso."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Trovati {len(studenti)} iscritti:"))
            for s in studenti:
                # Stampiamo l'oggetto Studente (che invocherà il suo metodo __str__)
                self._view.txt_result.controls.append(ft.Text(f"{s}"))

        # 6. Aggiornamento interfaccia
        self._view.update_page()

    # --- ESERCIZIO 3: Cerca studente ---
    def handle_cerca_studente(self, e):
        self._view.txt_result.controls.clear()

        # 1. Leggiamo la matricola inserita dall'utente (ATTENZIONE: è una Stringa!)
        matricola_str = self._view.txt_matricola.value

        if matricola_str == "":
            self._view.create_alert("Inserisci una matricola!")
            return

        # 2. Conversione Sicura (Try-Except)
        # Il DB vuole un numero (int), l'interfaccia ci dà un testo (str).
        # Se l'utente ha scritto "ciao", int("ciao") farebbe crashare l'app.
        try:
            matricola_int = int(matricola_str)
        except ValueError:
            self._view.create_alert("Errore: La matricola deve contenere solo numeri!")
            return

        # 3. Chiamata al Model
        studente = self._model.get_studente(matricola_int)

        # 4. Gestione risultato e Riempimento campi "Read Only"
        if studente is None:
            self._view.create_alert("Nessuno studente trovato con questa matricola.")
            # Svuotiamo i campi nome/cognome per sicurezza
            self._view.txt_nome.value = ""
            self._view.txt_cognome.value = ""
        else:
            # MAGIA: Riempiamo automaticamente le caselle di testo della View!
            self._view.txt_nome.value = studente.nome
            self._view.txt_cognome.value = studente.cognome
            self._view.txt_result.controls.append(ft.Text(f"Studente trovato: {studente.nome} {studente.cognome}"))

        self._view.update_page()

    # --- ESERCIZIO 4: Cerca corsi studente ---
    def handle_cerca_corsi_studente(self, e):
        self._view.txt_result.controls.clear()

        matricola_str = self._view.txt_matricola.value
        if matricola_str == "":
            self._view.create_alert("Inserisci una matricola!")
            return

        try:
            matricola_int = int(matricola_str)
        except ValueError:
            self._view.create_alert("La matricola deve essere un numero!")
            return

        # Per fare un bel lavoro, controlliamo prima se lo studente esiste
        studente = self._model.get_studente(matricola_int)
        if studente is None:
            self._view.create_alert("Studente non trovato nel database.")
            return

        # Ora cerchiamo i corsi
        corsi = self._model.get_corsi_studente(matricola_int)

        if len(corsi) == 0:
            self._view.txt_result.controls.append(ft.Text("Questo studente non è iscritto a nessun corso."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Lo studente è iscritto a {len(corsi)} corsi:"))
            for c in corsi:
                self._view.txt_result.controls.append(ft.Text(f"{c}"))

        self._view.update_page()

    # --- ESERCIZIO 5: Iscrivi studente ---
    def handle_iscrivi(self, e):
        self._view.txt_result.controls.clear()

        # Per iscrivere ci servono DUE informazioni: la tendina (corso) e il testo (matricola)
        codins = self._view.dd_corso.value
        matricola_str = self._view.txt_matricola.value

        if codins is None or matricola_str == "":
            self._view.create_alert("Per iscrivere uno studente devi inserire la matricola E selezionare un corso.")
            return

        try:
            matricola_int = int(matricola_str)
        except ValueError:
            self._view.create_alert("La matricola deve essere un numero!")
            return

        # Ti ricordi il Model? Restituisce direttamente una stringa di testo pronta da stampare!
        messaggio_esito = self._model.iscrivi_studente(matricola_int, codins)

        self._view.txt_result.controls.append(ft.Text(messaggio_esito))
        self._view.update_page()
