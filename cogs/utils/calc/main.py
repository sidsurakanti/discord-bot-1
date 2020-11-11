from .lexer import Lexer
from ._parser import Parser
from ._interpreter import Interpreter
from colorama import Fore, Style


def calc(expression):
	tokens = Lexer(expression).lexer()
	parsed = Parser(tokens).parse()
	results = Interpreter(parsed).run()
	return "".join(map(str, [*results]))


if __name__ == "__main__":
	print('Type "quit" to quit the program')
	while True:
		print(Fore.GREEN + ">>>" + Style.RESET_ALL, end=" ")
		expr = input()
		print(calc(expr))
