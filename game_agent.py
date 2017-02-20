"""This program works in conjunction with isolation.py and tournament.py to generate player 
moves and evaluation functions"""

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

## The following function is created to calculate "Manhattan distance" between
## the player locations. This value is used in two of the evaluation functions
def manhattan_distance(move1, move2):
    return(abs(move1[0]-move2[0])+abs(move1[1]-move2[1]))



def custom_score(game, player):

    """Three heuristic functions are evaluated as part of this exercise. The best 
    of the three is chosen after performing game simulations. 

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).


    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    player1_moves = (game.get_legal_moves(player))
    player2_moves = (game.get_legal_moves(game.get_opponent(player)))
 

    p1_location = game.get_player_location(player)
    p2_location = game.get_player_location(game.get_opponent(player))

    dist = manhattan_distance(p1_location, p2_location) ## Gets the manhattan distance between the two player locations
    blank = game.get_blank_spaces() ## Gets the left over blank spaces in the board

    overlap = list(set(player1_moves).intersection(player2_moves)) ## Gets the number of overlapping spaces between the two players

    #score = (len(player1_moves) -   len(player2_moves)) ## Heuristic used in the lecture
    #score =  len(player1_moves) - len(overlap) #Evaluation Function I
    #score = (len(player1_moves) - (len(player2_moves))) / (1 + dist )  # Evaluation Function II 
    score = (len(player1_moves) - len(player2_moves)) / (1 + dist + len(blank)) # Evaluation Function III (best)


    return(float(score))


class CustomPlayer:
    """
    This class specifies a few methods (minimax and minimax with alpha-beta pruning) that 
    helps the player to choose the next best move in the game.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout



    def minimax(self, game, depth, maximizing_player=True):
        """This function implements the minimax method

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        """
        ## When the time left is smaller than the threshold to run the method, this fetches a quick move
        ## for the player from the get_move subroutine
        if self.time_left() < self.TIMER_THRESHOLD:
            return(self.score(game, self), game.get_move(game, game.get_legal_moves(self), self.TIMER_THRESHOLD))


        ## Minimax is implemented using two helper functions (min_value and max_value) 
        ## This algorithm is implemented based on the pseudocode specified in Russell & Norvig (2010)

        ## The main 'function' uses recursive sub-functions to minimize / maximize the values obtained
        ## at each depth of the game tree. If the player is a maximizing player, then they are directed
        ## to the minimizing function, where they get the values at that depth (or further). 


        def min_value(game, n_game, n_depth, max_depth, maximizing_player):

            ## This is the terminal test. If the search reaches the maximum depth specified or if any 
            ## of the players wins / loses, then it returns the values at that node without 
            ## further recursing.
            if n_depth == max_depth or n_game.is_winner(self) == True or n_game.is_loser(self) == True:
                return(float(self.score(n_game, self)))
            
            ## Here the decision is made based on whether the original player is maximizing / not.
            ## If the original player is maximizing, then at this minimizing node, it is the opponent's moves
            ## that needs to be considered (their scores have to be minimized)
            if maximizing_player:
                n_moves = n_game.get_legal_moves(game.get_opponent(self))
            else:
                n_moves = n_game.get_legal_moves(self)
            
            ## Highest possible value is assigned as the best score before comparing them to the lower node values
            best_score = float('Inf') 

            ## Before recursing the depth value is increased, so that it is checked at the next level whether 
            ## the program has explored the maximum depth or not
            n_depth = n_depth + 1 
            for m in n_moves:
                next_game = n_game.forecast_move(m) ## A deep copy of the next move
                best_score = min(best_score, max_value(game, next_game, n_depth, max_depth, maximizing_player)) 

            return(best_score)

        def max_value(game, n_game, n_depth, max_depth, maximizing_player):
            ## This is the terminal test. If the search reaches the maximum depth specified or if any 
            ## of the players wins / loses, then it returns the values at that node without 
            ## further recursing.
            if n_depth == max_depth or n_game.is_winner(self) == True or n_game.is_loser(self) == True:
                return(float(self.score(n_game, self)))

            ## Here the decision is made based on whether the original player is maximizing / not.
            ## If the original player is maximizing, then at this maximizing node, it has to be the same person.
            if maximizing_player:
                n_moves = n_game.get_legal_moves(self)
            else:
                n_moves = n_game.get_legal_moves(game.get_opponent(self))

            ## Lowest possible value is assigned as the best score before comparing them to the lower node values
            best_score = float('-Inf')

            ## Before recursing the depth value is increased, so that it is checked at the next level whether 
            ## the program has explored the maximum depth or not
            n_depth = n_depth + 1
            for m in n_moves:
                next_game = n_game.forecast_move(m) ## A deep copy of the next move
                best_score = max(best_score, min_value(game, next_game, n_depth, max_depth, maximizing_player))

            return(best_score)

        try:

            num_legal_moves = game.get_legal_moves(game.active_player)

            ## This is given as the 'best move' and if no further moves are found suitable,
            ## the program returns this.
            best_move = (-1, -1) 
            if maximizing_player:
                best_score = float('-Inf') ## Lowest possible value
            else:
                best_score = float('Inf') ## Highest possible value

            ## The program searches for all the possible moves
            for m in num_legal_moves:
                next_game = game.forecast_move(m) ## Deep copy of the next move

                ## If the player is at the maximizing node, then the next level is opponent's turn
                ## so the program has to look at the minimizing subroutine
                if maximizing_player:
                    score = min_value(game, next_game, 1, depth, maximizing_player)
                    if score > best_score:
                        best_move = m
                        best_score = score   
                else:
                    score = max_value(game, next_game, 1, depth, maximizing_player)
                    if score < best_score:
                        best_score = score
                        best_move = m
                        

            return(best_score, best_move)

        except TimeoutError:

            return(best_score, best_move)

    

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """This function implements the alpha-beta pruning for the above minimax algorithm.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """

        ## When the time left is smaller than the threshold to run the method, this fetches a quick move
        ## for the player from the get_move subroutine
        if self.time_left() < self.TIMER_THRESHOLD:
            return(self.score(game, self), game.get_move(game, game.get_legal_moves(self), self.TIMER_THRESHOLD))



        ## Similar to minimax the alpha-beta pruning is implemented using two helper functions 
        ## (min_value and max_value).
        ## This algorithm is implemented based on the pseudocode specified in Russell & Norvig (2010)

        ## The main 'function' uses recursive sub-functions to minimize / maximize the values obtained
        ## at each depth of the game tree. If the player is a maximizing player, then they are directed
        ## to the minimizing function, where they get the values at that depth (or further). 

        ## The only difference between this and the minimax tree is, this algorithm uses two values alpha
        ## and beta, which it uses to prune the game tree, thus, successfully reducing the number of 
        ## nodes explored.

        def min_value_ab(game, n_game, n_depth, max_depth, alpha, beta, maximizing_player):

            ## This is the terminal test. If the search reaches the maximum depth specified or if any 
            ## of the players wins / loses, then it returns the values at that node without 
            ## further recursing.
            if n_depth == max_depth or n_game.is_winner(self) == True or n_game.is_loser(self) == True:
                return((self.score(n_game, self)))

            ## Here the decision is made based on whether the original player is maximizing / not.
            ## If the original player is maximizing, then at this minimizing node, it is the opponent's moves
            ## that needs to be considered (their scores have to be minimized)
            if maximizing_player:
                n_moves = n_game.get_legal_moves(game.get_opponent(self))
            else:
                n_moves = n_game.get_legal_moves(self)

            score = float('Inf') ## Highest possible score
            n_depth = n_depth + 1 ## Depth is increased before it is explore further

            for m in n_moves:

                next_game = n_game.forecast_move(m) ## Deep copy of the next move

                ## The value obtained from the lower subroutine is compared with that of the 
                ## value specified in this function--minimum of those is chosen
                score = min(score, max_value_ab(game, next_game, n_depth, max_depth, alpha, beta, maximizing_player))

                ## Here is where alpha-beta pruning is different from minimax

                ## The value obtained above is compared with the value alpha passed down to this function
                ## if it is smaller, it is returned, else the loop keeps going until it finds the value 
                ## smaller than alpha. This will be used to prune the tree in the main function
                if score <= alpha:
                    return(score)

                ## The value of beta is assigned the minimum of the new value found vs. the previous beta value
                beta = min(beta, score)


            return(score)

        def max_value_ab(game, n_game, n_depth, max_depth, alpha, beta, maximizing_player):

            ## This is the terminal test. If the search reaches the maximum depth specified or if any 
            ## of the players wins / loses, then it returns the values at that node without 
            ## further recursing.
            if n_depth == max_depth or n_game.is_winner(self) == True or n_game.is_loser(self) == True:
                return((self.score(n_game, self)))

            ## Here the decision is made based on whether the original player is maximizing / not.
            ## If the original player is maximizing, then at this maximizing node, it has to be the same person.
            if maximizing_player:
                n_moves = n_game.get_legal_moves(self)
            else:
                n_moves = n_game.get_legal_moves(game.get_opponent(self))

            score = float('-Inf') ## Lowest possible value
            n_depth = n_depth + 1 ## Depth is increased before it is explore further

            for m in n_moves:
                next_game = n_game.forecast_move(m) ## Deep copy of the next move

                ## The value obtained from the lower subroutine is compared with that of the 
                ## value specified in this function--maximum of those is chosen
                score = max(score, min_value_ab(game, next_game, n_depth, max_depth, alpha, beta, maximizing_player))


                ## Here is where alpha-beta pruning is different from minimax

                ## The value obtained above is compared with the value beta passed down to this function.
                ## if it is greater, it is returned, else the loop keeps going until it finds the value 
                ## larger than beta. This will be used to prune the tree in the main function
                if score >= beta:
                    return(score)

                ## The value of alpha is assigned the maximum of the new value found vs. the previous alpha value
                alpha = max(alpha, score)

            return(score)


        try:

            num_legal_moves = game.get_legal_moves(self)

            ## This is given as the 'best move' and if no further moves are found suitable,
            ## the program returns this.
            best_move = (-1, -1)


            if maximizing_player:
                best_score = alpha ## Lowest possible value
            else:
                best_score = beta ## Highest possible value

            for m in num_legal_moves:
                next_game = game.forecast_move(m)

                ## If the player is at the maximizing node, then the next level is opponent's turn
                ## so the program has to look at the minimizing subroutine
                if maximizing_player:
                    score = min_value_ab(game, next_game, 1, depth, alpha, beta, maximizing_player)
                    if score > best_score:
                        best_move = m
                        best_score = score

                    ## Pruning occurs here, when the best score returned is greater than beta.
                    ## The loop breaks and returns the best move. It doesn't loop further 
                    ## to look at the remaining nodes.
                    if best_score >= beta:
                        break

                    alpha = max(alpha, best_score)
                    
                else:
                    score = max_value_ab(game, next_game, 1, depth, alpha, beta, maximizing_player)
                    if score < best_score:
                        best_move = m
                        best_score = score

                    ## Pruning occurs here, when the best score returned is smaller than alpha.
                    ## The loop breaks and returns the best move. It doesn't loop further 
                    ## to look at the remaining nodes.
                    if best_score <= alpha:
                        break

                    beta = min(alpha, best_score)

            return(best_score, best_move)

        except TimeoutError:
            return(best_score, best_move)

    def get_move(self, game, legal_moves, time_left):
        """This function searches for the best move from the available legal moves and returns a
        result before the time limit expires.

        This function performs iterative deepening if self.iterative=True,
        and it uses the search method (minimax or alphabeta) corresponding
        to the self.method value.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        try:

            ## This routine calls for the best move as quickly as possible first. 
            ## Then, while time remains, it looks at iterative deepening for each of 
            ## the specified method.

            ## In iterative deepening, it explores the nodes at each depth
            ## increasing it by one level every time. It saves the previous
            ## result, so when time runs of it returns the best move to the player


            d = 1
            if self.method == "minimax":
                best_score, best_move = self.minimax(game, 1)

                ## A high margin is given for searching moves,especially for playing in tournaments
                ## where time is really important to get back to the quick best move
                while self.time_left() >= 600: 
                    if self.iterative:
                        d = d + 1
                        best_score, best_move = self.minimax(game, d)
            elif self.method == "alphabeta":
                best_score, best_move = self.alphabeta(game, 1)

                ## A high margin is given for searching moves,especially for playing in tournaments
                ## where time is really important to get back to the quick best move
                while self.time_left() >= 600: 
                    if self.iterative:
                        d = d + 1
                        best_score, best_move = self.alphabeta(game, d)
                

        except TimeoutError:
            return(best_move)

        # Returns the best move from the last completed search iteration
        if best_move in legal_moves:
            return(best_move)
        elif not legal_moves:
            return((-1,-1))





