from typing import Tuple
import math

def lerp(number: float, left: float, right: float) -> float:
  if number < left:
    return left
  elif number > right:
    return right
  else:
    return number

def format_seconds_to_min_sec(seconds: int) -> str:
  mins: int = seconds // 60
  secs: int = seconds % 60

  return f'{mins:02d}:{secs:02d}'

def distance_from_points(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
  return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def between(a: float, b1: float, b2: float) -> bool:
  return a >= b1 and a <= b2