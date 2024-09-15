class SkillCommands():
  def __init__(self, drop_bomb: int) -> None:
    self.__drop_bomb = drop_bomb

  def drop_bomb(self) -> int:
    return self.__drop_bomb
