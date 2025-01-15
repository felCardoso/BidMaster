class Player:

    def __init__(self, name) -> None:
        self.name = name
        self.deck = []
        self.coin = {0: 0, 1: 0, 2: 0, 5: 0, 10: 0, 20: 0, 50: 0}
        self.card = []
        self.initialize_coins()

    def initialize_coins(self) -> None:
        """Inicializa as moedas do jogador."""
        self.coin = {0: 2, 1: 3, 2: 1, 5: 1, 10: 0, 20: 0, 50: 0}

    def add_deck(self, card) -> None:
        """Adiciona uma carta ao deck do jogador."""
        self.deck.append(card)

    def del_deck(self, card) -> None:
        """Remove uma carta do deck do jogador."""
        self.deck.remove(card)

    def add_coins(self, coins_dict: dict) -> None:
        """Adiciona moedas ao jogador"""

        for coin, amount in coins_dict.items():

            if coin in self.coin:
                self.coin[coin] += amount
            else:
                raise ValueError(f"Valor de moeda inválido: {coin}")

    def del_coins(self, coins_dict) -> None:
        """Remove moedas do jogador"""

        for coin, amount in coins_dict.items():

            if coin in self.coin:
                if self.coin[coin] >= amount:
                    self.coin[coin] -= amount
                else:
                    raise ValueError(
                        f"Não há moedas de valor {coin} suficientes para remover"
                    )
            else:
                raise ValueError(f"Valor de moeda inválido: {coin}")

    def show_deck(self) -> str:
        """Mostra o deck do jogador em uma string"""

        if not self.deck:
            return "[Vazio]"

        deck_count = {}

        for card in self.deck:

            if card.id in deck_count:
                deck_count[card.id] += 1
            else:
                deck_count[card.id] = 1

        sorted_deck = sorted(deck_count.items())

        result = []

        for card_id, count in sorted_deck:

            for card in self.deck:

                if card.id == card_id:

                    if card.name == "Rato":
                        result.append(f"{count}x [Rato]")
                    else:
                        result.append(f"{count}x [{card.name}] {card.value}")
                    break

        return ", ".join(result)

    def show_coins(self) -> str:
        """Mostra as moedas do jogador em uma string"""

        return " / ".join(
            f"{coin}c: {amount}x" for coin, amount in self.coin.items() if amount > 0
        )

    def deduct_coins(self, amount) -> dict:
        """Deduz uma quantidade de moedas de acordo com um valor"""

        keys = sorted([key for key in self.coin.keys() if key != 0], reverse=True)
        deduced_coins = self.coin.copy()
        coins_used = {}

        for value in keys:

            while amount >= value and deduced_coins[value] > 0:

                amount -= value
                deduced_coins[value] -= 1

                if value in coins_used:
                    coins_used[value] += 1
                else:
                    coins_used[value] = 1

        if amount > 0:
            raise ValueError(
                "Não foi possível deduzir o valor total do lance com as moedas disponíveis."
            )

        return coins_used

    def total_coins(self) -> int:
        """Faz a soma total das moedas do jogador."""
        return sum(value * count for value, count in self.coin.items())
