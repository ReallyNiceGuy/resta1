#!/usr/bin/python3
# -- encoding: utf-8 --

import sys
import tty
import termios

from resta1 import *

ESC="\033["
K_UP=8593
K_DOWN=8595
K_RIGHT=8594
K_LEFT=8592

def ansi(*kargs):
  print(*kargs,sep="",end="")
  sys.stdout.flush()

def home():
  ansi(ESC,"H")

def cls():
  ansi(ESC,"2J",ESC,"H")

def getch():
  """
  Gets a single character from STDIO.
  """
  fd = sys.stdin.fileno()
  old = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    return sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)

def moveTo(l,c):
  ansi(ESC,l,";",c,"H")


def getKey():
  ch = getch()
  if ch == "\033":
    ch = getch()
    if ch == "[":
      ch = getch()
      if ch == "A":
        return K_UP
      elif ch == "B":
        return K_DOWN
      elif ch == "C":
        return K_RIGHT
      elif ch == "D":
        return K_LEFT
  return ord(ch)

def reverse():
  ansi(ESC,"31;47;5m")

def normal():
  ansi(ESC,"39;49m")

undo=[]
cls()
l,c=(1,1)
b = Board()
selected=False
home()
print(b.saveGame())
while b.hasValidMoves():
  if selected:
    reverse()
    moveTo(origin[1]+1,origin[0]+1)
    print(b.getCell(origin[0],origin[1]),end="")
    normal()
  moveTo(l,c)
  ch = getKey() 
  if ch == ord("q"):
    moveTo(b.numLines+1,1)
    ansi("Sair realmente [Y/n]?")
    ch = getch()
    ansi(ESC,"1K")
    if ch != "n":
      break
  elif ch == K_UP:
    l=max(1,l-1)
  elif ch == K_DOWN:
    l=min(b.numLines,l+1)
  elif ch == K_LEFT:
    c=max(1,c-1)
  elif ch == K_RIGHT:
    c=min(b.numCols,c+1)
  elif ch == ord(" "):
    if not selected:
      if len(b.getPossibleMoves(c-1,l-1))>0:
        origin=(c-1,l-1)
        selected = True
    else:
      selected = False
      target=(c-1,l-1)
      sg = b.saveGame()
      if b.move(origin,target):
        undo.append(sg) 
  elif not selected and ch == ord("u") and len(undo)>0:
    b.loadGame(undo.pop())
  home()
  print(b.saveGame())

moveTo(b.numLines+1,1)
if b.resta1():
  print("Parabéns!")
elif not b.hasValidMoves():
  print("Tente novamente")

