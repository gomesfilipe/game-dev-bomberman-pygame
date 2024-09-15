from src.core.base_object import BaseObject
from abc import abstractmethod
import pygame

class Display(BaseObject):
  def __init__(self, width: float, height: float) -> None:
    self._width = width
    self._height = height

  def height(self) -> float:
    return self._height

  def width(self) -> float:
    return self._width

  def update(self) -> None:
    return

  def fixed_update(self) -> None:
    return