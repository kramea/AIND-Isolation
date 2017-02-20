
# Isolation Game-playing Agent

## Synopsis

In this project, an adversarial search agent is developed to play the game "Isolation". Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around), however, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

These rules are implemented in the `isolation.Board` class provided in the repository. The `Board` class exposes an API including `is_winner()`, `is_loser()`, `get_legal_moves()`, and other methods available for your agent to use.

### Heuristics used for evaluation

Three evaluations functions were explored to analyze the quick heuristics for end-game scenarios.

- First heuristic is the difference between the number of moves of the player and the number of overlapping squares of the two players. The idea is as the game comes to an end, the overlaps have to be reduced so that the agent successfully blocks the opponent, while increasing its number of moves.

- Second heuristic utilizes the distance between the two players. The idea is, as distance between them reduces, it is an indication to the end-game. An inverse of distance is used to score. This is not always true, as the players might start out close.

- Third heuristic captures the issue with the second heuristic. It includes the number of blank spaces in its function. It takes the inverse of (1 + distance + number of blank spaces) along with maximizing the number of moves of the agent, and minimizing the number of moves of the opponent. This turns out to be best heuristic of all.

The exploratory results of these three heuristics are included in heuristics_evaluation.pdf file.

### Tournament

The `tournament.py` script is used to evaluate the effectiveness of your custom_score heuristic.  The script measures relative performance of your agent (called "Student") in a round-robin tournament against several other pre-defined agents.  The Student agent uses time-limited Iterative Deepening and the custom_score heuristic developed.

The performance of time-limited iterative deepening search is hardware dependent (faster hardware is expected to search deeper than slower hardware in the same amount of time).  The script controls for these effects by also measuring the baseline performance of an agent called "ID_Improved" that uses Iterative Deepening and the improved_score heuristic from `sample_players.py`.  

The tournament opponents are listed below. (See also: sample heuristics and players defined in sample_players.py)

- Random: An agent that randomly chooses a move each turn.
- MM_Null: CustomPlayer agent using fixed-depth minimax search and the null_score heuristic
- MM_Open: CustomPlayer agent using fixed-depth minimax search and the open_move_score heuristic
- MM_Improved: CustomPlayer agent using fixed-depth minimax search and the improved_score heuristic
- AB_Null: CustomPlayer agent using fixed-depth alpha-beta search and the null_score heuristic
- AB_Open: CustomPlayer agent using fixed-depth alpha-beta search and the open_move_score heuristic
- AB_Improved: CustomPlayer agent using fixed-depth alpha-beta search and the improved_score heuristic



