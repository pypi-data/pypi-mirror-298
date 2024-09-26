from typing import List
import random


class Sudoku:
    def __init__(self, dimension: int, difficulty: float) -> None:
        self.base = dimension
        self.difficulty = difficulty
        self.puzzle: List[List[str]] = []

    def generate(self) -> None:
        base = self.base
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        r_base = range(base)
        rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
        cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
        nums = shuffle(range(1, base * base + 1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = int(squares * self.difficulty)

        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = "."

        self.sudoku = board

    def show(self) -> None:
        for line in self.sudoku:
            print(" ".join(str(n) for n in line))

    def solution(self) -> List[List[str]]:
        return self.sudoku
