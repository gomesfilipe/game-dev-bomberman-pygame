from typing import Tuple

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
