import sys

class Board:
    def __init__(self):
        self.sz = 5
        self.num_pos = {}
        self.pos_num = {}
        self.pos_mark = {}

    def read(self, fi):
        rn = 0
        for ln in fi:
            ln = ln.strip()
            if not ln:
                break
            nums = list(map(int, ln.split()))
            self.sz = len(nums)
            for idx, num in enumerate(nums):
                self.num_pos[num] = (rn, idx)
                self.pos_num[(rn, idx)] = num
            rn += 1

    def play(self, num):
        if num in self.num_pos:
            self.pos_mark[self.num_pos[num]] = True

    def check_wins(self):
        for i in range(self.sz):
            for x in range(self.sz):
                if not self.pos_mark.get((i, x)):
                    break
            else:
                return True
            for y in range(self.sz):
                if not self.pos_mark.get((y, i)):
                    break
            else:
                return True
        return False

    def score(self):
        return sum(num for num in self.num_pos if not self.pos_mark.get(self.num_pos[num]))

    def __repr__(self):
        return f'<Board {self.num_pos!r}>'

    def show(self):
        for x in range(self.sz):
            for y in range(self.sz):
                print(f'{self.pos_num[(x, y)]}{"*" if self.pos_mark.get((x, y)) else " "}', end='\t')
            print()
        print()

plays = [int(i) for i in sys.stdin.readline().strip().split(',')]
sys.stdin.readline()  # blank

boards = []
try:
    while True:
        board = Board()
        board.read(sys.stdin)
        boards.append(board)
except KeyboardInterrupt:
    pass

for play in plays:
    print(f'play {play}')
    for idx, bd in enumerate(boards):
        bd.play(play)
        bd.show()
        if bd.check_wins():
            score = bd.score()
            print(f'board {idx} wins, score raw {score}, play {play}, result {score*play}')
            exit()
