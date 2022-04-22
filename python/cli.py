from python.command import Command
from python.parser import fromProlog, toAST
import python.utils as utils
from python.errors import CommandError, UnknownCommandError, PrologQuerryError

class CLI:

	def __init__(self, prolog, msg="Welcome to this CLI\n"):
		self.prolog = prolog
		self.env = {}
		self.coms = {
			"builtin":    self.Builtin(self),
			"help":       self.Help(self),
			"var":        self.Var(self),
			"eval":       self.Eval(self),
			"bind":       self.Bind(self),
			"prologform": self.PrologForm(self),
			"details":    self.Details(self),
			"exit":       self.Exit(self),
			"lambda":     self.Lambda(self)
		}
		print(msg)

	def run(self, string):
		args = string.split(" ")
		try:
			return str(self.coms[args[0]].run(args[1:]))
		except KeyError as ke:
			raise UnknownCommandError(f"Unknown command: {arglist[0]}")

	def doBackup(self):
		self.bup_env = self.env

	def recover(self):
		self.env = self.bup_env

	class Lambda(Command):

		def run(self, arglist):
			return "λ"

		@property
		def help(self):
			return "Prints out a lambda(\"λ\")"

	class Help(Command):

		def run(self, arglist):
			if len(arglist)==0:
				return "Usage: \"help [command name]\""
			try:
				return self.env.coms[arglist[0]].help
			except KeyError as ke:
				raise CommandError(f"Unknown command: {arglist[0]}").source("help")

		@property
		def help(self):
			return "If you managed to run this command you already know how this works"
		

	class Builtin(Command):

		def run(self, arglist):
			if arglist[0]=="churchnum":
				try:
					prologString = next(self.env.prolog.query(f"churchNum({arglist[1]}, X)"))["X"]
				except:
					raise PrologQuerryError(f"Error caused by the querry: churchNum({arglist[1]}, X)").source("builtin")
				return fromProlog(prologString)
			elif arglist[0]=="comb":
				try:
					prologString = next(self.env.prolog.query(f"comb({arglist[1]}, X)"))["X"]
				except:
					raise PrologQuerryError(f"Error caused by the querry: comb({arglist[1]}, X)").source("builtin")
				return fromProlog(prologString)
			else: raise CommandError("Unknown source").source("builtin")

		@property
		def help(self):
			return"\
Subcommand for accessing built-in lambda terms. Returns ASTs.\n\n\
Usage:\n\
builtin [churchnum/comb] arg1\n\n\
Details:\n\
builtin churchnum arg1: returns the AST of the lambda term representing the Church Numeral representation of arg1\n\
builtin comb arg1: returns the AST of of the lambda term representing the combinator named by arg1. Run \"details\" for list of available combinators"


	class Var(Command):

		def run(self, arglist):
			try:
				return self.env.env[arglist[0]]
			except:
				raise CommandError(f"Unkown variable {arglist[0]}").source("var")

		@property
		def help(self):
			return"\
			Subcommand for accessing previously bound lambda terms. Returns ASTs.\n\n\
Usage:\n\
var arg1\n\n\
Details:\n\
arg1 := The name of the variable to be querried. Must be all capitalized"


	class Eval(Command):

		def run(self, arglist):
			prologString = toAST(" ".join(arglist), self.env.env).stringify()
			try:
				result = next(self.env.prolog.query(f"eval({prologString}, X)"))["X"]
			except:
				raise PrologQuerryError(f"Error caused by the querry: eval({prologString}, X)")
			return fromProlog(result)

		@property
		def help(self):
			return"\
Subcommand for computing the β-normal form of lambda terms. Returns ASTs.\n\n\
Usage:\n\
eval arg1\n\n\
Details:\n\
arg1 := the lambda term to be evaluated. Can contain previously bound variables"


	class Bind(Command):

		def run(self, arglist):
			if not arglist[0].isupper(): raise CommandError("Variables must be all UPERCASE").source("bind")
			if arglist[1]=="to":
				res = toAST(" ".join(arglist[2:]), self.env.env)
			else:
				try:
					res = self.env.coms[arglist[1]].run(arglist[2:])
				except KeyError as ke:
					raise UnknownCommandError(f"Unknown command: {arglist[1]}")
			self.env.env[arglist[0]] = res
			return f"Bound {arglist[0]} to {res}"

		@property
		def help(self):
			return"\
Command that binds an AST to a variable in the enviroment. Variable names must be all capitalized. Should this command be run with a previously bound variable, the previous value will be overwritten.\n\n\
Usage:\n\
bind varname [args/to arg1]\n\n\
Details:\n\
varname := the name of the variable to be bound to. Must be all capitalized\n\
args := a subcommand that returns an AST which will be bound to the variable with name varname\n\
arg1 := a lambda term that to be directly bound to the variable with name varname"


	class PrologForm(Command):

		def run(self, arglist):
			if arglist[0]=="of":
				res = toAST(" ".join(arglist[1:]), self.env.env)
			else:
				try:
					res = self.env.coms[arglist[0]].run(arglist[1:])
				except KeyError as ke:
					raise UnknownCommandError(f"Unknown command: {arglist[1]}")
			return res.stringify()

		@property
		def help(self):
			return"\
Command that prints the prolog form of an AST.\n\n\
Usage:\n\
prologform [args/of arg1]\n\n\
Details:\n\
args := a subcommand that returns an AST which will be printed in its prolog form\n\
arg1 := a lambda term to be direclty shown in its prolog form"


	class Details(Command):

		def getCommands(self):
			return list(self.env.coms)

		def getVariables(self):
			return list(self.env.env)

		def getCombinators(self):
			res = list(self.env.prolog.query("comb(X,_)"))
			return [comb["X"] for comb in res]

		def run(self, arglist):
			comsL = self.getCommands()
			varsL = self.getVariables()
			combL = self.getCombinators()

			coms = utils.listToString(comsL, " ")[1:-1]
			vrs  = utils.listToString(varsL, " ")[1:-1]
			comb = utils.listToString(combL, " ")[1:-1]

			return\
			f"List of available commands:\n\
{coms}\n\n\
List of bound variables:\n\
{vrs}\n\n\
List of available combinators\n\
{comb}"

		@property
		def help(self):
			return\
			"Command that prints details about the current eviroment.\n\nUsage:\ndetails"



	class Exit(Command):

		def run(self, arglist):
			exit()

		@property
		def help(self):
			return "Exits the program"
		



	# class Print(Command):

	# 	def run(self, arglist):
	# 		if arglist[0]=="var":
	# 			return self.env[arglist[1]]
	# 		if arglist[0]=="builtin":
	# 			return parser.fromProlog(self.coms["builtin"].run(arglist[1:]))
	# 		if arglist[0]=="eval":
	# 			return parser.fromProlog(self.coms["eval"].run(arglist[1:]))
	# 		else: exit()