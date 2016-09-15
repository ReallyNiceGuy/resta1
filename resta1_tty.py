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

cls()
l,c=(1,1)
b = Board()
selected=False
print(b.saveGame())
moveTo(l,c)
while b.hasValidMoves():
  ch = getKey() 
  if ch == ord("q"):
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
        reverse()
        print(str(b.getCell(c-1,l-1)),end="")
        normal()
        origin=(c-1,l-1)
        selected = True
    else:
      selected = False
      target=(c-1,l-1)
      b.move(origin,target)
      home()
      print(b.saveGame())
  moveTo(l,c)
moveTo(b.numLines+1,1)
if b.resta1():
  print("Parabéns!")
else:
  print("Tente novamente")

