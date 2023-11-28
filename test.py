from utils import tryN
class A:
  def __init__(self, N):
    self.N = N
  def do(self):
    self.N -= 1
    if self.N >= 0:
      raise Exception("aaa")
    return self.N

MICRO_DELAY = 0.01

assert(tryN(A(1).do, 5, MICRO_DELAY) == -1)
assert(tryN(A(4).do, 5, MICRO_DELAY) == -1)

try:
    tryN(A(5).do, 5, MICRO_DELAY)
    assert(False)
except:
    pass

