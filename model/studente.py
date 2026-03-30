from dataclasses import dataclass
@dataclass
class Studente:
    matricola: int
    cognome: str
    nome: str
    CDS: str

    def __eq__(self, other):
        # Due studenti sono uguali se hanno la stessa matricola
        return self.matricola == other.matricola

    def __hash__(self):
        return hash(self.matricola)

    def __str__(self):
        # Come apparirà lo studente nella ListView di Flet
        return f"{self.cognome}, {self.nome} ({self.matricola})"