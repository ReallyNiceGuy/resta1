#include "resta1.h"
#include <vector>
#include <tuple>
#include <utility>
#include <iostream>
#include <sstream>

const std::string Cell::m_printable[3]{" ","\xE2\x97\x8B","\xE2\x97\x8F"};
const std::string Board::DEFAULTBOARD{
"7 7\n"
"0022200"
"0022200"
"2222222"
"2221222"
"2222222"
"0022200"
"0022200"
};


bool Board::isPlayable(int col, int line) const
{
  if (!isCellInsideBoard(col,line)) return false;
  return isPlayableNoCheck(col,line);
}

bool Board::isPlayableNoCheck(int col, int line) const
{
  for(auto &&pos: std::vector<std::pair<int,int>>{{-2,0},{2,0},{0,-2},{0,2}})
  {
    int to_col,to_line;
    std::tie(to_col,to_line) = pos;
    to_col+=col;
    to_line+=line;
    if (!isCellInsideBoard(to_col,to_line)) continue;
    if (std::get<0>(isMoveValid(col,line,to_col,to_line))) return true;
  }
  return false;
}

bool Board::hasValidMoves() const
{
  for(int line=0; line<m_lines; ++line)
  {
    for(int col=0; col<m_columns; ++col)
    {
      if (isPlayableNoCheck(line,col)) return true;
    }
  }
  return false;
}

bool Board::resta1() const
{
  int count = 0;
  for (auto cell : m_cells)
  {
    if (cell.isFull()) ++count;
    if (count>1) return false;
  }
  return count == 1;
}


Board::Board(std::string b)
{
  if (!load(b))
  {
    load(DEFAULTBOARD);
  }
}

bool Board::load(std::string b)
{
  std::istringstream s(b);
  std::string t;
  s>>m_columns;
  s>>m_lines;
  s>>t;
  m_cells.clear();
  for(auto ch : t)
  {
    m_cells.push_back(ch);
  }
  return true;
}

std::string Board::save() const
{
  std::ostringstream s;
  s<<m_columns<<' '<<m_lines<<'\n';
  for(int line=0; line<m_lines; ++line)
  {
    for(int col=0; col<m_columns; ++col)
    {
      s<<getCellNoCheck(col,line);
    }
  }
  return s.str();
}

std::string Board::printable() const
{
  std::ostringstream s;
  for(int line=0; line<m_lines; ++line)
  {
    for(int col=0; col<m_columns; ++col)
    {
      s<<getCellNoCheck(col,line).printable();
    }
    s<<'\n';
  }
  return s.str();
}
