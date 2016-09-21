#ifndef RESTA1_H
#define RESTA1_H
#include <vector>
#include <string>
#include <cstdlib>
#include <tuple>

class Cell
{
  public:
    Cell(char c = CLOSEDCHAR)
    {
      m_type = getValidType(c); 
    }
    Cell& operator =(char c)
    {
      m_type = getValidType(c);
      return *this;
    }
    operator char() const { return m_type; }
    char printable() const { return m_printable[m_type-'0']; }
    bool isEmpty()  const { return m_type == EMPTYCHAR; }
    bool isFull()   const { return m_type == FULLCHAR; }
    bool isClosed() const { return m_type == CLOSEDCHAR; }
    void setEmpty()  { m_type = EMPTYCHAR; }
    void setFull()   { m_type = FULLCHAR; }
    void setClosed() { m_type = CLOSEDCHAR; }
    static char getValidType(char c)
    {
      switch (c)
      {
        case FULLCHAR:
        case EMPTYCHAR:
          return c;
        default:
          return CLOSEDCHAR;
      }
    }
    static const char CLOSEDCHAR='0';
    static const char EMPTYCHAR='1';
    static const char FULLCHAR='2';
    static const char m_printable[3];
  protected:
    char m_type;

};

class Board
{
  public:
    static const std::string DEFAULTBOARD;
    Board(std::string b);
    Board() : Board(DEFAULTBOARD) {}
    bool move(int from_col, int from_line, int to_col, int to_line)
    {
      if (isMoveInsideBoard(from_col,from_line,to_col,to_line) &&
          isMoveLegal(from_col,from_line,to_col,to_line) )
      {
        bool valid;
        int over_col;
        int over_line;
        std::tie(valid,over_col,over_line) = isMoveValid(from_col,from_line,to_col,to_line);
        if (valid)
        {
          getCellNoCheck(from_col,from_line).setEmpty();
          getCellNoCheck(to_col,to_line).setFull();
          getCellNoCheck(over_col,over_line).setEmpty();
          return true;
        }
      }
      return false;
    }
    int lines() const { return m_lines; }
    int columns() const { return m_columns; }
    bool isPlayable(int col, int line) const;
    bool hasValidMoves() const;
    bool resta1() const;
    bool load(std::string b);
    std::string save() const;
    std::string printable() const;
    Cell getCell(int col, int line) const
    {
      if (isCellInsideBoard(col,line))
      {
        return getCellNoCheck(col,line);
      }
      return Cell{};
    }
  protected:
    bool isPlayableNoCheck(int col, int line) const;
    bool isMoveInsideBoard(int from_col, int from_line, int to_col, int to_line) const
    {
      return isCellInsideBoard(to_col,to_line) && isCellInsideBoard(from_col,from_line);
    }

    bool isMoveLegal(int from_col, int from_line, int to_col, int to_line) const
    {
      int delta_col  = abs(from_col - to_col);
      int delta_line = abs(from_line - to_line);
      return (delta_line == 2 && delta_col == 0) || (delta_col == 2 && delta_line == 0);
    }

    std::tuple<bool,int,int> isMoveValid(int from_col, int from_line, int to_col, int to_line) const
    {
      int over_col = from_col + (to_col - from_col)/2;
      int over_line = from_line + (to_line - from_line)/2;
      if (getCellNoCheck(from_col,from_line).isFull() &&
          getCellNoCheck(to_col,to_line).isEmpty() &&
          getCellNoCheck(over_col,over_line).isFull())
      {
        return std::make_tuple(true,over_col,over_line);
      }
      return std::make_tuple(false,over_col,over_line);
    }

    Cell getCellNoCheck(int col, int line) const
    {
      return m_cells[line*m_lines+col];
    }

    Cell &getCellNoCheck(int col, int line)
    {
      return m_cells[line*m_lines+col];
    }
    bool isCellInsideBoard(int col, int line) const
    {
      return (col >= 0 && line >= 0 && col < m_columns && line < m_lines);
    }
    std::vector<Cell> m_cells;
    int m_lines;
    int m_columns;
};

#endif //RESTA1_H
