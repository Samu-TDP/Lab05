from dataclasses import dataclass
@dataclass
class Corso:
    codins: str
    crediti: int
    nome: str
    pd: int

    def __eq__(self, other):
        # Due corsi sono uguali se hanno lo stesso codice insegnamento
        return self.codins == other.codins

    def __hash__(self):
        # Permette l'inserimento in set() e come chiave di dizionari
        return hash(self.codins)

    def __str__(self):
        # Come apparirà il corso nella ListView di Flet
        return f"{self.nome} ({self.codins})"