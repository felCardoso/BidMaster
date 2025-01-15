import random

ANIMALS = [
    "Cavalo",
    "Vaca",
    "Porco",
    "Burro",
    "Bode",
    "Ovelha",
    "Cachorro",
    "Gato",
    "Pato",
    "Galo",
    "Rato",
]
VALUE = [1000, 800, 650, 500, 350, 250, 160, 90, 40, 10, 0]
CARD_AMT = 4
RAT_ID = 11
DONKEY_ID = 4


class Card:

    def __init__(self, id: int, name: str, value: int) -> None:
        self.id = id
        self.name = name
        self.value = value
        # self.image_path = image_path

    def __repr__(self) -> str:
        if self.id != RAT_ID:
            return f"[{self.name}] - {self.value}"
        else:
            return f"[{self.name}]"


class Deck:

    def __init__(self) -> None:
        self.deck: list[Card] = []
        self.set_deck()

    def draw_card(self) -> Card:
        """Tira uma carta do baralho."""
        return self.deck.pop()

    def set_deck(self) -> None:
        """Cria o deck inicial"""

        base_deck = [
            Card(id=i + 1, name=ANIMALS[i], value=VALUE[i]) for i in range(11)
        ]  # image_path=f"images/{ANIMAL[i]}.png"

        for card in base_deck:
            self.deck.extend([card] * CARD_AMT)

        random.shuffle(self.deck)
