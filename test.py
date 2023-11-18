from utils import tryN
class A:
  def __init__(self, N):
    self.N = N
  def do(self):
    self.N -= 1
    if self.N >= 0:
      raise Exception("aaa")
    return self.N

assert(tryN(A(1).do, 5) == -1)
assert(tryN(A(4).do, 5) == -1)

try:
    tryN(A(5).do, 5)
    assert(False)
except:
    pass

