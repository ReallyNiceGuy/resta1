#!/usr/bin/python3
# -- encoding: utf-8 -- 

from enum import Enum

class CellType(str,Enum):
  closed = " "
  full = "o"
  empty = "."
  def values():
    return [e.value for e in CellType]

class Cell(object):
  def __init__(self,celType):
    self.type = CellType.closed
    for item in CellType:
      if celType == item.value:
        self.type = item

  def __str__(self):
    return self.type

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
  DEFAULTGAME = """\
{x}{x}{o}{o}{o}{x}{x}
{x}{x}{o}{o}{o}{x}{x}
{o}{o}{o}{o}{o}{o}{o}
{o}{o}{o}{_}{o}{o}{o}
{o}{o}{o}{o}{o}{o}{o}
{x}{x}{o}{o}{o}{x}{x}
{x}{x}{o}{o}{o}{x}{x}\
""".format(x=CellType.closed,o=CellType.full,_=CellType.empty)

  def __init__(self,gameState=DEFAULTGAME):
    self.loadGame(gameState)

  def loadGame(self,gameState):
    lines = gameState.split("\n")
    numCols = len(max(lines))
    self.lines = []
    for line in lines:
      line = line + (CellType.closed*(numCols-len(line)))
      for cell in line:
        self.lines.append(Cell(cell))
    self.numCols = numCols
    self.numLines = len(lines)

  def linesAsString(self):
    lines = []
    for line in range(self.numLines):
      cols =  []
      for col in range(self.numCols):
        cols.append(str(self.__getCellNoCheck(col,line)))
      lines.append("".join(cols))
    return lines
 
  def saveGame(self):
   return "\n".join(self.linesAsString())

  def __str__(self):
    result = []
    lines = self.linesAsString()
    result.append("  "+"".join([ str(x) for x in range(self.numCols)]))
    count = 0
    for line in lines:
     result.append(("%i " % count)+line)
     count = count + 1
    return "\n".join(result)

  def isInsideBoard(self,col,line):
    return col>=0 and col < self.numCols and \
           line>=0 and line < self.numLines

  def __getCellNoCheck(self,col,line):
    return self.lines[line*self.numLines+col]

  def getCell(self,col,line):
    if not self.isInsideBoard(col,line):
      return Cell(CellType.closed)
    return self.__getCellNoCheck(col,line)

  def getPossibleMoves(self,col,line):
    moves = []
    if not self.isInsideBoard(col,line):
      return []
    for i in [(-1,0),(1,0),(0,-1),(0,1)]:
      col_offset, line_offset = i
      target_line = line + line_offset*2
      target_col = col + col_offset*2
      over_line = line + line_offset
      over_col = col + col_offset
      if not self.isInsideBoard(target_col,target_line):
        continue
      if self.__getCellNoCheck(target_col,target_line).isEmpty() and \
         self.__getCellNoCheck(over_col,over_line).isFull() and \
         self.__getCellNoCheck(col,line).isFull():
         moves.append( ( (col,line),(target_col,target_line),(over_col,over_line)) )
    return moves 

  def move(self, origin, target):
    origin_col,origin_line = origin
    target_col,target_line = target
    over_col = origin_col+(target_col-origin_col)//2
    over_line = origin_line+(target_line-origin_line)//2
    over = (over_col,over_line)
    fullMove = (origin, target, over)
    if fullMove in self.getPossibleMoves(*origin):
      self.__getCellNoCheck(origin_col,origin_line).setEmpty()
      self.__getCellNoCheck(over_col,over_line).setEmpty()
      self.__getCellNoCheck(target_col,target_line).setFull()
      return True
    return False

  def hasValidMoves(self):
    for line in range(self.numLines):
      for col in range(self.numCols):
        if self.__getCellNoCheck(col,line).isFull():
          if len(self.getPossibleMoves(col,line))>0:
            return True
    return False


  def resta1(self):
    count = 0
    for cell in self.lines:
      if cell.isFull():
        count = count+1
    return 1 == count

if __name__ == "__main__":
  import time
  a = Board()
  print(str(a))
  while a.hasValidMoves():
    i = input("de_col de_linha para_col para_linha:")
    try:
      move = list(map(int,i.split()))
      if len(move) != 4 or not a.move( (move[0],move[1]),(move[2],move[3]) ):
        raise "Invalid move"
    except:
      print("Invalid move")
    print(str(a))

  if a.resta1():
    print("Parabéns!")
  else:
    print("Tente outra vez")

