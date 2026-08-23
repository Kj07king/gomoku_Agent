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



    def _generate_position_matrix(self, rows, cols):
      '''Generates a concentric heatmap matrix assigning higher values to central cells, 
           used to prioritize move ordering and reward controlling the board's center.'''
        center_r, center_c = rows // 2, cols // 2
        max_dist = max(center_r, center_c) + 1
        matrix = []
        for r in range(rows):
            row = []
            for c in range(cols):
                dist = max(abs(r - center_r), abs(c - center_c))
                val = max_dist - dist
                row.append(val)
            matrix.append(row)
        return matrix


    def _auto_detect_symbols(self, board, rows, cols):
        """Counts board pieces to dynamically assign 'X' or 'O' to the agent depending on whose turn it is,
           assuming 'X' always moves first"""
        x_count = 0
        o_count = 0

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'X':
                    x_count += 1
                elif board[r][c] == 'O':
                    o_count += 1

        if x_count > 0 or o_count > 0 or (self.agent_symbol in ['X', 'O'] and self.opponent_symbol in ['X', 'O']):
            if x_count == o_count:
                self.agent_symbol = 'X'
                self.opponent_symbol = 'O'
            else:
                self.agent_symbol = 'O'
                self.opponent_symbol = 'X'


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
  def _search_board(self, board,rows, cols):
    #search board value combin pattern scores and positional matrix bias 
    agent_score = self.score_patterens(board, self.agent_symbol, rows, cols)
    opp_score = self._score_patterns(board, self.opponent_symbol, rows, cols)
    
    pos_score = 0
    total_stones = 0
    for r in range (rows):
      for c in range (cols):
        val = board[r][c]
        if val != self.blank_symbol:
          total_stones += 1
          if val == self.agent_symbol:
            pos_score += self.agent_symbol:
            if val == self.opponemt_symbol:
                pos_score += self.position_matrix[r][c]
            elif val == self.opponemt_symbol:
                pos_score -= self.position_matrix[r][c]
      multiplier = 1.1 if total_stones > 100 else 1.3
      pattern_eval = agent_scoe - int(opp_score * multiplier)

      return pattern_evsl + pos_score  
    
def _score_patterns(self, board, symbol, rows, cols):
        #Scores patterns once per sequence to avoid over-counting.
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == symbol:
                    for dr, dc in directions:
                        score += self._search_line_one_direction(board, r, c, dr, dc, symbol, rows, cols)

        return score
