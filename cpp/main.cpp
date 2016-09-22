#include "resta1.h"
#include <iostream>
#include <cstdio>
#include <string>
#include <algorithm>
#include <ncursesw/curses.h>

int main(int argc, char **argv)
{
  Board B;
  std::vector<std::string> undo;
  setlocale(LC_CTYPE, "");
  initscr();
  mousemask(ALL_MOUSE_EVENTS, NULL);
  start_color();
  init_pair(1, COLOR_WHITE, COLOR_BLACK);
  init_pair(2, COLOR_RED, COLOR_WHITE);
  attron(COLOR_PAIR(1));
  raw();
  keypad(stdscr, TRUE);		/* We get F1, F2 etc..		*/
	noecho();
  bool selected=false;
  int col=0;
  int row=0;
  int sel_col=0;
  int sel_row=0;
  MEVENT event;
  while (B.hasValidMoves())
  {
    mvprintw(0,0,B.printable().c_str());
    if (selected)
    {
      mvchgat(sel_row,sel_col,1,A_NORMAL,2,NULL);
    }
    move(row,col);
    int ch = getch();
    if (ch == 'q')
    {
      mvprintw(B.lines(),0,"Are you sure? [y/N]");
      if (getch() == 'y')
      {
        break;
      }
      else
      {
        move(B.lines(),0);
        clrtoeol();
      }
    }
    switch (ch)
    {
      case KEY_MOUSE:
        if(getmouse(&event) == OK)
        {
          if (B.isCellInsideBoard(event.y,event.x))
          {
            row=event.y;
            col=event.x;
            ungetch(' ');
          }
        }
        break;
      case KEY_UP:
        row = std::max(0,row-1);
        break;
      case KEY_DOWN:
        row = std::min(row+1,B.lines()-1);
        break;
      case KEY_LEFT:
        col = std::max(0,col-1);
        break;
      case KEY_RIGHT:
        col = std::min(col+1,B.columns()-1);
        break;
      case 'u':
        if (!selected && undo.size()>0)
        {
          B.load(undo.back());
          undo.pop_back();
        }
        break;
      case ' ':
      case 10:
        if (!selected)
        {
          if (B.isPlayable(col,row))
          {
            selected = true;
            sel_col = col;
            sel_row = row;
          }
        }
        else
        {
          std::string save = B.save();
          if (B.move(sel_col,sel_row,col,row))
          {
            undo.push_back(save);
          }
          selected = false;
        }
        break;
      default:
        break;
    }
    move(row,col);
  }
  mvprintw(0,0,B.printable().c_str());
  move(B.lines(),0);
  clrtoeol();
  if (!B.hasValidMoves())
  {
    if (B.resta1())
    {
      printw("Congratulations!\n");
    }
    else
    {
      printw("Try again\n");
    }
  }
  printw("Press any key to quit...");
  getch();
  endwin();
}
