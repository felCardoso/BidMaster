# Leilão de Animais

Este é um jogo de cartas de leilão e blefe onde os jogadores tentam coletar conjuntos de quatro cartas de animais iguais.

> **Aviso:** Este jogo está em fase de teste. Feedbacks e sugestões são bem-vindos.

## Estrutura do Projeto

### Arquivos

- `actions.py`: Contém as classes e funções relacionadas às ações do jogo, como leilões e confrontos.
- `deck.py`: Define as classes `Card` e `Deck`, que representam as cartas e o baralho do jogo.
- `main.py`: Ponto de entrada do jogo.
- `player.py`: Define a classe `Player`, que representa os jogadores do jogo.

## Requisitos

- Python 3.12
- PyQt5

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/felCardoso/leilao.git
   ```
2. Navegue até o diretório do projeto:
   ```sh
   cd leilao
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Como Abrir o Jogo

1. Execute o arquivo `Leilao/main.py` para iniciar o jogo:
   ```sh
   python leilao/main.py
   ```
2. Siga as instruções na interface gráfica para participar dos leilões e trocas.

## Como Jogar

- Objetivo do Jogo: Colete o maior número de conjuntos de quatro animais iguais para ganhar pontos. O jogador com mais pontos no final vence.

- Cartas: O jogo inclui cartas de animais, cartas de pedigree e cartas de rato. As cartas de animais têm diferentes valores.

- Leilões: Os jogadores leiloam cartas de animais. O jogador que oferece o maior lance ganha a carta. Você pode usar dinheiro ou outras cartas de animais para fazer lances.

- Trocas: Além dos leilões, os jogadores podem trocar cartas entre si. As trocas envolvem negociação e blefe para obter as melhores cartas.

- Fim do Jogo: O jogo termina quando todas as cartas de animais foram leiloadas e trocadas. Os jogadores então somam os pontos dos seus conjuntos de animais para determinar o vencedor.

## Pontuação

- A pontuação é calculada com base nos grupos de cartas adquiridas e seus valores, a cada grupo de cartas, adiciona 1x ao multiplicador de pontos.
  Ex.: 4x Cavalo (1000) e 4x Burro (500) = (1.000 + 500) x 2 = 3.000

- O conjunto de rato elimina o grupo de cartas de menor valor.
  Ex.: 4x Burro (500), 4x Cachorro (160) 4x Rato = 500 x 1 (O grupo de cachorros perdeu o valor pelo rato)

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Caso queira ajudar o projeto com alguma ideia, sinta-se à vontade para fazer um pull request ou entre em contato pelo e-mail [fel.cardoso@outlook.com](mailto:fel.cardoso@outlook.com).
