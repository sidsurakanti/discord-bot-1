from .tokens import Token

types = {"+": "ADD",
         "-": "SUB",
         "*": "MUL",
         "/": "DIV",
         "(": "LPAREN",
         ")": "RPAREN"}

class Lexer:
  def __init__(self, expression):
    self.expression = iter(expression)
    self.current = None
    self.next()

  def next(self):
    try:
      self.current = next(self.expression)
    except StopIteration:
      self.current = None
  
  def lexer(self):
    while self.current is not None:
      if self.current in (' ', '\r', '\t', '\b', '\n'):
        self.next()

      elif self.current.isdigit():
        num = ""

        while (self.current is not None) and (self.current.isdigit() or self.current == "."):
          num += self.current
          self.next()

        yield Token("NUMBER", float(num))

      elif self.current in ("+", "-", "*", "/"):
        operator = self.current 
        self.next()
        yield Token(types[operator], operator)
      
      elif self.current in ("(", ")"):
        parenthesis = self.current
        self.next()
        yield Token(types[parenthesis], parenthesis)
    
      else:
        raise SyntaxError("Invalid Syntax")






