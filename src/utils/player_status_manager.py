from src.utils.bool_status import BoolStatus
from config import NONE_STATUS_DURATION, IMMUNE_STATUS_DURATION, DEAD_STATUS_DURATION

class PlayerStatusManager:
  def __init__(self) -> None:
    self.none = BoolStatus(True, NONE_STATUS_DURATION)
    self.immune = BoolStatus(False, IMMUNE_STATUS_DURATION)
    self.dead = BoolStatus(False, DEAD_STATUS_DURATION)

  def update(self) -> None:
    self.none.update()
    self.immune.update()
