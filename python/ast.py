from enum import Enum
import python.utils

Type = Enum('NodeType', "λ app var")

class AST():

	def __init__(self, type, values):
		self.type = type
		if (type == Type.λ):
			self.binders, self.body = values
		elif (type == Type.app):
			self.fun, self.arg = values
		else: self.name = values

	def stringify(self):
		if (self.type == Type.λ):
			return f"lambda({utils.listToString(self.binders)}, {self.body.stringify()})"
		if (self.type == Type.app):
			return f"app({self.fun.stringify()},{self.arg.stringify()})"
		else:
			return self.name

	def __str__(self):
		if (self.type == Type.λ):
			return f"λ{utils.listToString(self.binders)[1:-1]}.{self.body}"
		if (self.type == Type.app):
			if self.fun.type != Type.var and self.arg.type != Type.var:
				return f"({self.fun}) ({self.arg})"
			elif self.fun.type != Type.var:
				return f"({self.fun}) {self.arg}"
			elif self.arg.type != Type.var:
				return f"{self.fun} ({self.arg})"
			return f"{self.fun} {self.arg}"
		else:
			return self.name

