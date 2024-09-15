
import time

class GameTime:
  desired_fps = 60
  fixed_delta_time = 1.0 / 200.0
  delta_time = 0.0

  _acumulator = 0.0
  _time = time.time()
  _frame_time = time.time()

  @staticmethod
  def update():
    new_time = time.time()
    GameTime.delta_time = new_time - GameTime._time
    GameTime._time = new_time
    GameTime._acumulator += GameTime.delta_time

  @staticmethod
  def has_physics_time():
    return GameTime._acumulator > GameTime.fixed_delta_time

  @staticmethod
  def fixed_update():
    GameTime._acumulator -= GameTime.fixed_delta_time

  @staticmethod
  def wait_fps():
    frame_duration = time.time() - GameTime._frame_time
    time_to_wait = max(0, (1 / GameTime.desired_fps) - frame_duration)
    time.sleep(time_to_wait)
    GameTime._frame_time = time.time()
