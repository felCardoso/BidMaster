from player import Player
from deck import Deck, RAT_ID, DONKEY_ID
from actions import Auction, Clash, GameEnd

# from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
	QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QLabel,
    QInputDialog,
    QListWidget,
    QGridLayout,
    QMessageBox,
)


MIN_PLAYERS = 2


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Leilão")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QGridLayout()
        self.init_ui()

        self.count_donkeys = 0
        self.count_rats = 0

    def init_ui(self) -> None:
        """Inicializa a interface do usuário."""

        self.create_buttons()
        self.create_labels()
        self.create_lists()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def create_buttons(self) -> None:
        """Cria e configura os botões da interface."""

        self.start_button = QPushButton("Iniciar Jogo", self)
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button, 0, 0, 1, 2)

        self.take_card_btn = QPushButton("Puxar Carta", self)
        self.take_card_btn.clicked.connect(self.take_card)
        self.take_card_btn.setEnabled(False)
        self.layout.addWidget(self.take_card_btn, 1, 0, 1, 1)

        self.card_clash_btn = QPushButton("Desafio de Cartas", self)
        self.card_clash_btn.clicked.connect(self.card_clash)
        self.card_clash_btn.setEnabled(False)
        self.layout.addWidget(self.card_clash_btn, 1, 1, 1, 1)

    def create_labels(self) -> None:
        """Cria e configura os rótulos da interface."""

        self.card_label = QLabel("", self)
        self.layout.addWidget(self.card_label, 2, 0, 1, 2)

        self.info_label = QLabel("Informações do Jogo", self)
        self.layout.addWidget(self.info_label, 5, 0, 1, 2)

    def create_lists(self) -> None:
        """Cria e configura as listas da interface."""

        self.players_list = QListWidget(self)
        self.layout.addWidget(self.players_list, 3, 0, 1, 2)

        self.player_coins = QListWidget(self)
        self.layout.addWidget(self.player_coins, 4, 0, 1, 2)

    def start_game(self) -> None:
        """Configura os jogadores e o baralho para o início do jogo."""

        self.players = []

        num_players, ok = QInputDialog.getInt(
            self, "Número de Jogadores", "Quantos jogadores irão jogar?"
        )

        if ok:
            if num_players < MIN_PLAYERS:
                QMessageBox.warning(
                    self, "Erro", "Você deve adicionar pelo menos 2 jogadores."
                )
                return

            for i in range(num_players):
                name, ok = QInputDialog.getText(
                    self, "Nome do Jogador", f"Digite o nome do jogador {i+1}:"
                )

                if ok:
                    player = Player(name=name)
                    self.players.append(player)
                    self.update()
                else:
                    player = Player(name=f"Jogador {i+1}")
                    self.players.append(player)
                    self.update()

            self.info_label.setText(
                f"{num_players} jogadores adicionados. Pronto para começar!"
            )

            self.deck = Deck()
            self.turn = 0

            self.take_card_btn.setEnabled(True)

            self.layout.removeWidget(self.start_button)
            self.start_button.deleteLater()

    def take_card(self) -> None:
        """Tira uma carta do baralho e inicia um leilão."""

        player = self.players[self.turn]
        card = self.deck.draw_card()

        self.card_label.setText(
            f"[{len(self.deck.deck)}] {player.name} - Carta: {card}"
        )

        if card.id == RAT_ID:  # ID do Rato
            self.handle_rat(player, card)
        else:
            self.handle_cards(player, card)

        self.update()
        self.turn = (self.turn + 1) % len(self.players)
        self.info_label.setText(f"Vez de {self.players[self.turn].name}")

        if self.can_clash(self.players[self.turn], self.players):
            self.card_clash_btn.setEnabled(True)
        else:
            self.card_clash_btn.setEnabled(False)

        if len(self.deck.deck) == 0:  # Remove the Take Card button when out of Cards
            self.del_take_card_btn()

    def card_clash(self) -> None:
        """Inicia um desafio de cartas entre jogadores."""

        player1 = self.players[self.turn]
        player_options = self.get_player_options(player1)

        if player_options:
            nemesis, ok = QInputDialog.getItem(
                self,
                "Batalhar Carta",
                "Escolha o jogador que irá batalhar com você:",
                player_options,
                0,
                False,
            )

            if not ok:
                return

            player2 = self.get_player_by_name(nemesis)

            if not player2:
                QMessageBox.warning(self, "Erro", "Jogador não encontrado.")
                return

            card_options = self.get_card_options(player1, player2)

            card2, ok = QInputDialog.getItem(
                self,
                "Escolha a Carta",
                f"Escolha a carta do {nemesis} para batalhar:",
                card_options,
                0,
                False,
            )

            if not ok:
                return

            battled_card = next(c for c in player1.deck if c.name == card2)
            clash = Clash(
                player1=player1,
                player2=player2,
                card=battled_card,
            )

            clash.start_clash()

            self.update()

            self.turn = (self.turn + 1) % len(self.players)
            self.info_label.setText(f"Vez de {self.players[self.turn].name}")
            self.card_clash_btn.setEnabled(
                self.can_clash(self.players[self.turn], self.players)
            )

        if len(self.deck.deck) == 0:
            game = GameEnd(players=self.players)
            game.end_game()

    def handle_rat(self, player, card) -> None:
        """Lida com a carta de rato."""

        player.add_deck(card)

        self.count_rats += 1

        if self.count_rats < 4:
            QMessageBox.information(
                None, "Rato", f"O {self.count_rats}º rato foi sorteado! "
            )
        else:
            QMessageBox.information(None, "Rato", "O último rato foi sorteado! ")

        self.update()

    def handle_cards(self, player, card) -> None:
        """Lida com outras cartas."""

        if card.id == DONKEY_ID:
            self.donkey()

        auction = Auction(owner=player, card=card, players=self.players)
        auction.start_auction()

    def donkey(self) -> None:
        """Distribui moedas aos jogadores quando um burro é sorteado."""

        coins_list = [{5: 1}, {10: 1}, {20: 1}, {50: 1}]

        QMessageBox.information(
            None,
            "Burro",
            f"Um burro foi sorteado! Os jogadores ganham {list(coins_list[self.count_donkeys].keys())[0]}c.",
        )

        for player in self.players:
            player.add_coins(coins_list[self.count_donkeys])

        self.count_donkeys += 1
        self.update()

        return

    def del_take_card_btn(self) -> None:
        """Remove o botão de puxar carta quando o baralho está vazio."""
        self.layout.removeWidget(self.take_card_btn)
        self.take_card_btn.deleteLater()
        self.layout.removeWidget(self.card_clash_btn)
        self.layout.addWidget(self.card_clash_btn, 1, 0, 1, 2)

    def can_clash(self, player, players) -> bool:
        """Verifica se o jogador pode iniciar um desafio de cartas."""

        other_players = [p for p in players if p != player]

        for card in player.deck:

            for p in other_players:

                if p != player and any(c.id == card.id for c in p.deck):
                    return True

        return False

    def get_player_options(self, player1) -> list:
        """Obtém a lista de jogadores que podem ser desafiados."""

        return [
            p.name
            for p in self.players
            if p != player1
            and any(c.id in [card.id for card in player1.deck] for c in p.deck)
        ]

    def get_player_by_name(self, name) -> object:
        """Obtém um jogador pelo nome."""

        return next((p for p in self.players if p.name == name), None)

    def get_card_options(self, player1, player2) -> list:
        """Obtém a lista de cartas que podem ser desafiadas."""

        return [
            c.name
            for c in player2.deck
            if any(c.id == card.id for card in player1.deck)
        ]

    def get_card_by_name(self, player, name) -> object:
        """Obtém uma carta pelo nome."""

        return next(c for c in player.deck if c.name == name)

    def update(self) -> None:
        """Atualiza a interface do usuário com o estado atual do jogo."""

        self.players_list.clear()
        self.player_coins.clear()

        for player in self.players:

            self.players_list.addItem(f"{player.name} - Deck: {player.show_deck()}")
            self.player_coins.addItem(
                f"{player.name} - Coins: {player.show_coins()} - Total: {player.total_coins()}"
            )


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
