class PlayerCommands():
  def __init__(self, up: int, left: int, down: int, right: int) -> None:
    self.__up = up
    self.__left = left
    self.__down = down
    self.__right = right

  def up(self) -> int:
    return self.__up

  def left(self) -> int:
    return self.__left

  def down(self) -> int:
    return self.__down

  def right(self) -> int:
    return self.__right
