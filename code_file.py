import time

class GomokuAgent:
  def __init__(self, agent_symbol='X', blank_symbol='.', opponent_symbol='O'):
    self.name = "gomoku-agent-pro-max-alpha"
    self.agent_symbol = agent_symbol
    self.blank_symbol = blank_symbol
    self.opponent_symbol = opponent_symbol
    self.time_limit = 4.2  # it makes the move decison in less then 5 seconds 
    self.position_matrix = None
  
  def play(self, board):
        start_time = time.time()
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        # Create of change matrix-based position bias in the board dimensions
        if self.position_matrix is None or len(self.position_matrix) != rows or len(self.position_matrix[0]) != cols:
            self.position_matrix = self._generate_position_matrix(rows, cols)
        
        #symbol dectection can play as X or 0
        self.detect_symbols(board, rows, cols)
        
        #makes a move within 1 distance of the opponents move
        opponents = self.opponents_move(board, rows, cols, distance=1)

        #Opening move: starts with the center of the board
        if not opponents:
          return(rows //2, cols // 2)

        # check if it is a winning move first depth   
        for r, c in opponents:
          board[r][c] = self.agent_symbole
          if self._check_win(board, r,c, self.agent_symbol,rows, cols):
            board[r][c] = self.blank_symbol
            return (r, c)
          board[r][c] = self.blank_symbol

        # check the opponets move and if blocks the chance to win 
        for r, c in opponents:
          board[r][c] = self.opponent_symbole
          if self._check_win(board, r,c, self.opponent_symbol,rows, cols):
            board[r][c] = self.blank_symbol
            return (r, c)
          board[r][c] = self.blank_symbol
          
        #Alpha-beta Pruning as deep search algorithm
         best_move = opponents[0]
         opponents = self.order_moves(board,candidates, rows, cols)
         for depth in range(1, 6):
           if time.time() - start_time > self.time_limit:
             break
            current_best = None
            best_score = -float('inf')
            alpha = -float('inf')
            beta = float('inf')
           
            # search top candidate moves
           for r, c in candidates[:30]:
             if time.time() - start_time > self.time_limit:
               break
               
              board[r][c] = self.agent_symbol
              score = self._alpha_beta(
                  board, depth - 1, alpha, beta, False, start_time, rows, cols inital_depth=depth )
              board[r][c] = self.blank_symbol
              
              if score > best_score:
                best_score = score
                current_best = (r,c)

              alpha = max(alpha, best_score)
             if time.time()- start_time <= self.time_limit and current_best:
               best_move = current_best
             else:
               break
          return best_move 
    def _alpha_beta(self, board,depth, alpha, beta, is_maximizing, start_time, rows, cols, initial_depth):
      #Add alpha beat search and add depth penalties for move distacne 
      ply = initial-depth - depth # distance from the root node 
       
      if depth == 0 or time.time() - start_time > self.time_limit:
        #discount leaf heuristic score slightly based on ply (prefer immediate position advantage)
        raw_eval = self._evaluate_board(board, rows, cols)
        return int(raw_eval * (0.95 ** ply))

       opponents = self.get_oppoents_moves(board, rows, cols, distance =1)
       if not opponents:
         return 0
        
       opponents = self.order_moves()board, candidates, rows, cols)
       if is_maximizing:
         max_eval = -float('inf')
         for r, c in candidates[:20]:
           board[r][c] = self.agent_symbol


      # Immediate win depth penalty/bonus: win earlier (+100000 - ply * 10)
        if self._check_win(board, r, c, self.agent_symbol, rows, cols):
          board[r][c] = self.blank_symbol
          return 100000 - (ply * 10)

        eval_score = self._alpha_beta(board, depth - 1, alpha, beta, False, start_time, rows, cols, initial_depth)
        board[r][c] = self.blank_symbol
        max_eval = max(max_eval, eval_score)
        alpha = max(alpha, max_eval)

        if beta <= alpha:
            break

    return max_eval

        else:
            min_eval = float('inf')
            for r, c in opponents[:20]:
                board[r][c] = self.opponent_symbol

                # Immediate loss depth penalty/bonus: delay loss (-100000 + ply * 10)
                if self._check_win(board, r, c, self.opponent_symbol, rows, cols):
                    board[r][c] = self.blank_symbol
                    return -100000 + (ply * 10)

                eval_score = self._alpha_beta(board, depth - 1, alpha, beta, True, start_time, rows, cols, initial_depth)
                board[r][c] = self.blank_symbol
              
                min_eval = min(min_eval, eval_score)
                beta = min(beta, min_eval)

                if beta <= alpha:
                    break

      return min_eval


