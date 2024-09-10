def lerp(number: float, left: float, right: float) -> float:
  if number < left:
    return left
  elif number > right:
    return right
  else:
    return number
