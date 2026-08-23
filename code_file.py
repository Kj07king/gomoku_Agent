import time

class GomokuAgent:
  def __init__(self, agent_symbol='X', blank_symbol='.', opponent_symbol='O'):
    self.name = "gomoku-agent-pro-max-alpha"
    self.agent_symbol = agent_symbol
    self.blank_symbol = blank_symbol
    self.opponent_symbol = opponent_symbol
    self.time_limit = 4.2  # it makes the move decison in less then 5 seconds 
    self.position_matrix = None
