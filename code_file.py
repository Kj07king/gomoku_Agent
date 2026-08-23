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
        if not candidates:
          return(rows //2, cols // 2)
          
       
