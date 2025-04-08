from functools import lru_cache


class Fibonacci:
    def __init__(self, n):
        self.n = n

@staticmethod
@lru_cache(2**16)
def fib(n):
    if n < 2:
        return 1
    return Fibonacci.fib(n-2) + Fibonacci.fib(n-1)
def __len__(self):
    return self.n
def __getitem__(self, index):
    if isinstance(index, int):
        if index < 0 or index > self.n - 1:
            raise IndexError

        return Fibonacci.fib(index)
if __name__=="__main__":
    fib(6)