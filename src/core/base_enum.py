from enum import Enum
from typing import List

class BaseEnum(Enum):
  @classmethod
  def cases(cls) -> List['BaseEnum']:
    return [case for case in cls]

  @classmethod
  def values(cls) -> List[str]:
    return [case.value for case in cls]

  @classmethod
  def names(cls) -> List[str]:
    return [case.name for case in cls]
