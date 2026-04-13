import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # --- Impostazioni base della Pagina ---
        self._page = page
        self._page.title = "Lab 05 - Segreteria Studenti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        # --- Riferimento al Controller ---
        self._controller = None

        # --- Pre-dichiarazione degli elementi grafici (Componenti UI) ---
        self._title = None

        # Riga 1: Dati studente
        self.txt_matricola = None
        self.txt_nome = None
        self.txt_cognome = None

        # Riga 2: Menu a tendina per i corsi
        self.dd_corso = None

        # Riga 3: Bottoni delle azioni
        self.btn_cerca_studente = None
        self.btn_cerca_corsi = None
        self.btn_iscrivi = None

        # Riga 4: Area dei risultati
        self.txt_result = None

    def load_interface(self):
        """Costruisce fisicamente i pezzi grafici e li aggiunge alla pagina."""

        # --- TITOLO ---
        self._title = ft.Text("App Gestione Studenti", color="blue", size=24, weight="bold")
        self._page.controls.append(self._title)

        # --- MENU A TENDINA (Corsi) ---
        # Creiamo la tendina vuota e chiederemo al Controller di riempirla (come nel Lab04)
        self.dd_corso = ft.Dropdown(
            label="Seleziona un Corso",
            width=500,
            hint_text="Scegli il corso per cui vuoi vedere gli iscritti"
        )
        # Chiamata al Controller per popolare le opzioni del Dropdown (Esercizio 1)
        self._controller.riempi_dd_corsi()

        # Aggiungiamo un bottone di fianco alla tendina per cercare gli iscritti al corso (Esercizio 2)
        self.btn_iscritti_corso = ft.ElevatedButton(
            text="Cerca Iscritti",
            on_click=self._controller.handle_cerca_iscritti
        )

        # Uniamo tendina e bottone nella prima riga
        row_corsi = ft.Row([self.dd_corso, self.btn_iscritti_corso], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row_corsi)

        # --- CAMPI DI TESTO (Dati Studente) ---
        # Creiamo le tre caselle di testo. Nome e Cognome le mettiamo in 'read_only'
        # perché le riempiremo noi in automatico quando cerchiamo la matricola.
        self.txt_matricola = ft.TextField(label="Matricola", width=150)
        self.txt_nome = ft.TextField(label="Nome", width=200, read_only=True)
        self.txt_cognome = ft.TextField(label="Cognome", width=200, read_only=True)

        row_studente = ft.Row([self.txt_matricola, self.txt_nome, self.txt_cognome],
                              alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row_studente)

        # --- BOTTONI DELLE AZIONI ---
        # Creiamo i tre bottoni richiesti e li colleghiamo ai futuri metodi del Controller
        self.btn_cerca_studente = ft.ElevatedButton(
            text="Cerca studente",
            on_click=self._controller.handle_cerca_studente
        )
        self.btn_cerca_corsi = ft.ElevatedButton(
            text="Cerca corsi",
            on_click=self._controller.handle_cerca_corsi_studente
        )
        self.btn_iscrivi = ft.ElevatedButton(
            text="Iscrivi",
            on_click=self._controller.handle_iscrivi
        )

        row_bottoni = ft.Row([self.btn_cerca_studente, self.btn_cerca_corsi, self.btn_iscrivi],
                             alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row_bottoni)

        # --- AREA RISULTATI ---
        # Creiamo la ListView scrollabile dove il Controller stamperà i testi
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        # Renderizziamo il tutto a schermo
        self._page.update()

    # --- METODI GETTER E SETTER ---
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    # --- METODI DI UTILITÀ PER IL CONTROLLER ---
    def create_alert(self, message):
        """Apre un popup di errore se l'utente sbaglia qualcosa."""
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        """Aggiorna lo schermo. Usato dal Controller dopo aver stampato i risultati."""
        self._page.update()
