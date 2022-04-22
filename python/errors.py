class ProjException(Exception):
	pass

class LexerError(ProjException):
	pass

class ParserError(ProjException):
	pass

class ImpossibleError(ProjException):
	pass

class PrologParserError(ProjException):
	pass

class CommandError(ProjException):

	def source(self, string):
		self.command = string

class UnknownCommandError(ProjException):
	pass

class PrologQuerryError(CommandError):
	pass