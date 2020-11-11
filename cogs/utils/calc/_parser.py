from .nodes import NumberNode, OperatorNode


class Parser:
	def __init__(self, tokens):
		self.tokens = iter(tokens)
		self.current = None
		self.next()

	def next(self):
		try:
			self.current = next(self.tokens)
		except StopIteration:
			self.current = None
		
	def parse(self):
		while self.current is not None:
			yield self.add_subtract()

	def add_subtract(self):
		left = self.multiply_divide()

		while (self.current is not None) and (self.current.type in ("ADD", "SUB")):
			operator = self.current
			self.next()
			right = self.multiply_divide()
			left = OperatorNode(left, right, operator)
		
		return left
	
	def multiply_divide(self):
		left = self.factor()

		while (self.current is not None) and (self.current.type in ("MUL", "DIV")):
			operator = self.current
			self.next()
			right = self.factor()
			left = OperatorNode(left, right, operator)
		
		return left

	def factor(self):
		if self.current is not None:

			if self.current.type == "LPAREN":
				self.next()
				res = self.add_subtract()

				if (self.current is None) or (self.current.type != "RPAREN"):
					raise SyntaxError("Invalid Syntax")
				
				self.next()
				return res

			if self.current.type in ("NUMBER"):
				cur = self.current 
				self.next()
				return NumberNode(cur.value)

		raise SyntaxError("Invalid Syntax")

