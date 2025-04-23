from deck import CARD_AMT, RAT_ID
from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
)


class BidDialog(QDialog):

    def __init__(self, player, card, parent=None) -> None:
        super().__init__(parent)

        self.player = player
        self.card = card

        self.setWindowTitle("Lance")
        self.layout = QVBoxLayout()

        self.info_label = QLabel(
            f"[{self.card.name}] - {self.card.value}\n{self.player.name}, insira suas moedas.\n{self.player.show_coins()}"
        )
        self.layout.addWidget(self.info_label)

        self.coin_inputs = {}

        for coin in self.player.coin.keys():
            h_layout = QHBoxLayout()
            label = QLabel(f"{coin}c:")

            spin_box = QSpinBox()
            spin_box.setRange(0, self.player.coin[coin])

            h_layout.addWidget(label)
            h_layout.addWidget(spin_box)

            self.layout.addLayout(h_layout)
            self.coin_inputs[coin] = spin_box

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

        self.setLayout(self.layout)

    def get_bid(self) -> tuple:
        coins_dict = {
            coin: spin_box.value() for coin, spin_box in self.coin_inputs.items()
        }

        bid = sum(coin * amount for coin, amount in coins_dict.items())

        return bid, coins_dict


class Auction:

    def __init__(self, owner, card, players) -> None:
        self.owner = owner
        self.card = card
        self.players = players

    def start_auction(self) -> None:

        winner_bid = 0
        winner = None

        bidding = True

        desist_cont = 0
        desist_lock = True

        players_order = (
            self.players[self.players.index(self.owner) + 1 :]
            + self.players[: self.players.index(self.owner)]
        )

        while bidding:

            for player in players_order:

                if not bidding:
                    break

                total_funds = player.total_coins()
                valid_bid = False

                while not valid_bid:

                    bid, ok = QInputDialog.getInt(
                        None,
                        "Lance",
                        f"[{self.card.name}] - {self.card.value}\n{player.name}, insira seu lance.\n{player.show_coins()}\nSaldo disponível: {total_funds}",
                    )

                    if bid > total_funds:
                        QMessageBox.warning(
                            None,
                            "Lance Inválido",
                            "Você não possui fundos suficientes para este lance.",
                        )
                        break

                    if ok:
                        if bid == 0:

                            QMessageBox.warning(
                                None,
                                "Lance",
                                f"{player.name} desistiu do lance.",
                            )
                            desist_cont += 1

                            if (
                                desist_cont
                                >= (len(self.players) - 1) & desist_lock
                                == False
                            ):
                                bidding = False
                                break
                            elif (
                                desist_cont
                                >= (len(players_order) - 1) & desist_lock
                                == True
                            ):
                                desist_lock = False
                                break
                            else:
                                continue
                            
                        if bid > winner_bid:
                            winner_bid = bid
                            winner = player
                            valid_bid = True
                            desist_lock = False
                            QMessageBox.information(
                                None,
                                "Lance",
                                f"{player.name} deu um lance de {bid}!",
                            )
                        else:
                            QMessageBox.warning(
                                None,
                                "Lance Inválido",
                                "O lance deve ser maior que o anterior.",
                            )
                            break
                    else:
                        QMessageBox.warning(
                            None, "Lance", f"{player.name} desistiu do lance."
                        )
                        desist_cont += 1

                        if (
                            desist_cont
                            >= (len(self.players) - 2) & desist_lock
                            == False
                        ):
                            bidding = False
                            break
                        elif (
                            desist_cont >= (len(self.players) - 2) & desist_lock == True
                        ):
                            desist_lock = False
                            break

        if not bidding:
            if winner is None:
                QMessageBox.information(
                    None,
                    "Leilão Concluído",
                    f"{self.owner.name} venceu o leilão sem lances!",
                )
                self.owner.add_deck(self.card)
            else:
                QMessageBox.information(
                    None,
                    "Leilão Concluído",
                    f"{winner.name} venceu o leilão com um lance de {winner_bid}!",
                )
                deduced_coins = winner.deduct_coins(winner_bid)
                winner.add_deck(self.card)
                self.owner.add_coins(deduced_coins)
                winner.del_coins(deduced_coins)
        else:
            QMessageBox.information(
                None,
                "Leilão Concluído",
                f"{self.owner.name} venceu o leilão sem lances!",
            )
            self.owner.add_deck(self.card)

    def has_coins(self, player, bid) -> bool:

        total_funds = sum(value * count for value, count in player.coin.items())

        return total_funds >= bid


class Clash:

    def __init__(self, player1, player2, card) -> None:
        self.player1 = player1
        self.player2 = player2
        self.card = card

    def set_coins(self, player) -> tuple:

        total_funds = sum(value * count for value, count in player.coin.items())
        bid_dialog = BidDialog(player, self.card)

        if bid_dialog.exec_() == QDialog.Accepted:
            bid, coins_dict = bid_dialog.get_bid()

            if bid > total_funds:
                QMessageBox.warning(
                    None,
                    "Lance Inválido",
                    "Você não possui fundos suficientes para este lance.",
                )

                return None, None

            return bid, coins_dict

        return None, None

    def start_clash(self) -> None:

        winner = None
        loser = None
        tie = False

        bid1, coins1 = self.set_coins(self.player1)

        if bid1 is None:
            return

        QMessageBox.information(
            None,
            "Lance do Jogador 1",
            f"{self.player1.name} deu: {sum(coins1.values())} moeda(s)",
        )

        bid2, coins2 = self.set_coins(self.player2)

        if bid2 is None:
            return

        if bid1 == bid2:
            tie = True
        elif bid1 > bid2:
            winner = self.player1
            loser = self.player2
            winner_coins = coins1
            loser_coins = coins2
        else:
            winner = self.player2
            loser = self.player1
            winner_coins = coins2
            loser_coins = coins1

        if tie:
            QMessageBox.information(
                None,
                "Resultado do Confronto",
                "O confronto terminou em empate!",
            )
        else:
            QMessageBox.information(
                None,
                "Resultado do Confronto",
                f"{winner.name} venceu o confronto com um lance de {max(bid1, bid2)}!",
            )

        if tie:
            return
        else:
            winner_coins = winner.deduct_coins(max(bid1, bid2))
            loser_coins = loser.deduct_coins(min(bid1, bid2))

            winner.add_coins(loser_coins)
            winner.del_coins(winner_coins)
            loser.add_coins(winner_coins)
            loser.del_coins(loser_coins)

            if self.card.id == 11:  # If the card is a rat the winner loses it
                winner.del_deck(self.card)
                loser.add_deck(self.card)
            else:  # If the card is any other the winner takes it
                winner.add_deck(self.card)
                loser.del_deck(self.card)


class GameEnd:

    def __init__(self, players) -> None:
        self.players = players

    def score(self, player) -> int:

        card_counts = {}
        groups = 0
        values = 0
        rat = False

        for card in player.deck:

            if card.id in card_counts:
                card_counts[card.id] += 1
            else:
                card_counts[card.id] = 1

        for card_id, count in card_counts.items():

            if count == CARD_AMT:

                if card_id == RAT_ID:  # Assuming 11 is the ID for rats
                    rat = True

                else:
                    groups += 1

                    card_value = next(
                        card.value for card in player.deck if card.id == card_id
                    )

                    values += card_value

        if rat:
            min_value = min(card.value for card in player.deck if card.id != 11)
            values -= min_value
            groups -= 1

        score = groups * values

        return score

    def end_game(self) -> None:

        scores = {player.name: self.score(player) for player in self.players}
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        winner = sorted_scores[0][0]
        winner_score = sorted_scores[0][1]

        result_message = "Pontuações Finais:\n"

        for player, score in sorted_scores:

            result_message += f"{player}: {score} pontos\n"

        result_message += f"\nVencedor: {winner} com {winner_score} pontos!"

        QMessageBox.information(None, "Fim do Jogo", result_message)

        # Create a table to show the ranking
        table = QTableWidget()
        table.setRowCount(len(sorted_scores))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Jogador", "Pontuação"])

        for row, (player, score) in enumerate(sorted_scores):

            table.setItem(row, 0, QTableWidgetItem(player))
            table.setItem(row, 1, QTableWidgetItem(str(score)))

        table.resizeColumnsToContents()
        table.setWindowTitle("Ranking Final")
        table.show()
