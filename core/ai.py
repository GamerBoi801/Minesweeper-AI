from .board import Minesweeper
from itertools import chain

class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def known_mines(self):
        if self.count == len(self.cells):
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI:
    def __init__(self, height=8, width=8, log_callback=None):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []
        self.log_callback = log_callback

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        if self.log_callback:
            self.log_callback(f"Marked {cell} as a mine")

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        if self.log_callback:
            self.log_callback(f"I'm pretty sure {cell} won't explode - let's open to see. ")

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        surrounding = self.get_nearby(cell)
        self.knowledge.append(Sentence(surrounding, count))

        changed = True
        while changed:
            changed = False
            removed = []
            for sentence in list(self.knowledge):
                if sentence.count==0:
                    for c in sentence.cells.copy():
                        if c not in self.safes:
                            self.mark_safe(c)
                            changed = True
                    removed.append(sentence)
                if sentence.count==len(sentence.cells):
                    for c in sentence.cells.copy():
                        if c not in self.mines:
                            self.mark_mine(c)
                            changed = True
                    removed.append(sentence)
            for r in removed:
                if r in self.knowledge:
                    self.knowledge.remove(r)

            # subset inference
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1==s2: continue
                    if s1.cells.issubset(s2.cells):
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        temp = Sentence(new_cells, new_count)
                        if temp not in self.knowledge and len(temp.cells)>0:
                            self.knowledge.append(temp)
                            changed = True

    def make_safe_move(self):
        for item in self.safes:
            if item not in self.moves_made and item not in self.mines:
                if self.log_callback:
                    self.log_callback(f"AI safe move at {item}")
                return item
        if self.log_callback:
            self.log_callback("No safe moves")
        return None

    def make_random_move(self):
        import random
        while True:
            x = random.randint(0,self.height-1)
            y = random.randint(0,self.width-1)
            if (x,y) not in self.moves_made and (x,y) not in self.mines:
                if self.log_callback:
                    self.log_callback(f"AI random move at {(x,y)}")
                return (x,y)

    def get_nearby(self, cell):
        cells = set()
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                nr, nc = cell[0]+dr, cell[1]+dc
                if 0<=nr<self.height and 0<=nc<self.width:
                    pt=(nr,nc)
                    if pt not in self.safes and pt not in self.mines and pt not in self.moves_made:
                        cells.add(pt)
        return cells
