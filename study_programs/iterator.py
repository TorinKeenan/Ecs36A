#making my own iterators
class Range:
    def __init__(self, start, finish):
        self.i = start
        self.n = finish

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            self.i += 1
            return self.i - 1


def range_by_generator(start, finish):
    i = start
    while i < finish:
        yield i
        i += 1


for i in Range(4, 10):
    print(i)
print("\n")
for i in range_by_generator(3, 7):
    print(i)
