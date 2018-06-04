

class Elem:

    def __init__(self, x, l: 'List'):
        self.x = x
        self.list = l

    def __eq__(self, other):
        self.notify_list(other)
        return self.x == other.x

    def __ne__(self, other):
        self.notify_list(other)
        return self.x != other.x

    def __lt__(self, other):
        self.notify_list(other)
        return self.x < other.x

    def __le__(self, other):
        self.notify_list(other)
        return self.x <= other.x

    def __gt__(self, other):
        self.notify_list(other)
        return self.x > other.x

    def __ge__(self, other):
        self.notify_list(other)
        return self.x >= other.x

    def notify_list(self, other):
        self.list.comparisons += 1
        self.list.high_lighted1 = self.x
        self.list.high_lighted2 = other.x
        self.list.view.update(self.list, True)

