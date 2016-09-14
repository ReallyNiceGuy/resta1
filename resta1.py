#!/usr/bin/python3
# -- encoding: utf-8 -- 

from enum import Enum

DEFAULTGAME = """\
..XXX..
..XXX..
XXXXXXX
XXXOXXX
XXXXXXX
..XXX..
..XXX..
"""
class CellType(Enum):
  closed = 0
  empty = 1
  full = 2

class Cell(object):
  def __init__(self,celType):
    if celType == "X":
      self.type = CellType.full
    elif celType == "O":
      self.type = CellType.empty
    else:
      self.type = CellType.closed

  def __str__(self):
    if self.type == CellType.full:
      return "X"
    elif self.type == CellType.empty:
      return "O"
    else:
      return "."

  def isEmpty(self):
    return self.type == CellType.empty

  def isFull(self):
    return self.type == CellType.full

  def isClosed(self):
    return self.type == CellType.closed

  def setEmpty(self):
    self.type = CellType.empty

  def setFull(self):
    self.type = CellType.full

  def setClosed(self):
    self.type = CellType.closed


class Board(object):
  def __init__(self,gameState=DEFAULTGAME):
    self.loadGame(gameState)

  def loadGame(self,gameState):
    lines = gameState.split()
    numCols = len(max(lines))
    self.lines = []
    for line in lines:
      line = line + ("."*(numCols-len(line)))
      linecell = []
      for cell in line:
        linecell.append(Cell(cell))
      self.lines.append(linecell)

  def linesAsString(self):
    lines = []
    for line in self.lines:
      cols =  []
      for cell in line:
        cols.append(str(cell))
      lines.append("".join(cols))
    return lines
 
  def saveGame(self):
   return "\n".join(self.linesAsString())

  def __str__(self):
    result = []
    lines = self.linesAsString()
    numCols = len(max(lines))
    result.append("  "+"".join([ str(x) for x in range(numCols)]))
    count = 0
    for line in lines:
     result.append(("%i " % count)+line)
     count = count + 1
    return "\n".join(result)

  def getPossibleMoves(self,col,line):
    moves = []
    if col<0 or line <0:
      return False
    lines = len(self.lines)
    if line >= lines:
      return False
    columns = len(self.lines[line])
    if col >= columns:
      return False
    for i in [(-1,0),(1,0),(0,-1),(0,1)]:
      col_offset, line_offset = i
      target_line = line + line_offset*2
      target_col = col + col_offset*2
      over_line = line + line_offset
      over_col = col + col_offset
      if target_line<0 or target_line>=lines:
        continue
      if target_col<0 or target_col>=columns:
        continue
      if self.lines[target_line][target_col].isEmpty() and \
         self.lines[over_line][over_col].isFull() and \
         self.lines[line][col].isFull():
         moves.append( ( (col,line),(target_col,target_line),(over_col,over_line)) )
    return moves 

  def move(self, origin, target):
    over = (origin[0]+(target[0]-origin[0])//2,origin[1]+(target[1]-origin[1])//2)
    fullMove = (origin, target, over)
    if fullMove in self.getPossibleMoves(*origin):
      self.lines[origin[1]][origin[0]].setEmpty() 
      self.lines[over[1]][over[0]].setEmpty()
      self.lines[target[1]][target[0]].setFull()
      return True
    return False

  def hasValidMoves(self):
    for line in range(len(self.lines)):
      for col in range(len(self.lines[line])):
        if self.lines[line][col].isFull():
          if len(self.getPossibleMoves(col,line))>0:
            return True
    return False


  def resta1(self):
    count = 0
    for line in self.lines:
      for cell in line:
        if cell.isFull():
           count = count+1
    return 1 == count

if __name__ == "__main__":
  a = Board()
  print(str(a))
  while a.hasValidMoves():
    i = input("de_col de_linha para_col para_linha:")
    move = list(map(int,i.split()))
    if len(move) != 4 or not a.move( (move[0],move[1]),(move[2],move[3]) ):
        print("Invalid move")
    print(str(a))

  if a.resta1():
    print("Parabéns!")
  else:
    print("Tente outra vez")

