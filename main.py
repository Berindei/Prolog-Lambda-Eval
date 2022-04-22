from pyswip import Prolog
from python.cli import CLI
import os
import sys
from python.errors import *

os.system('cls' if os.name=='nt' else 'clear')

prolog = Prolog()
prolog.consult("lambdaEval.pl")

welcomeString =\
	"Welcome to the Lambda Evaluator in Prolog Command-Line Interface.\n\nRun \"details\" for more details on the enviroment and use \"help [command name]\" to find out more about the functionality of commands. Run multiple commands by separating them with semicolons(;). An entire line of commands is atomic.\n\nNotice: usage of builtin terms is not available due to a bug in pyswip :(\n"


cli = CLI(prolog, welcomeString)

debug = False
if len(sys.argv) > 1:
	if sys.argv[1] == "dbg": debug = True


while True:
	string = input("λ>>")
	cmnds = string.split(';')
	cli.doBackup()
	msg=""

	for indx, cmnd in enumerate(cmnds):
		try:
			msg += cli.run(cmnd.lstrip())
			msg += '\n'
		except Exception as e:
			msg = f"Error in command {indx}: "

			if isinstance(e, (ParserError, LexerError, PrologParserError, UnknownCommandError)):
				msg += f"{e.__class__.__name__}: {e}"
			elif isinstance(e, (CommandError, PrologQuerryError)):
				msg += f"{e.__class__.__name__} from command {e.command}: {e}"
			elif isinstance(e, ImpossibleError):
				msg += "This shouldn't ever happen :("
			else:
				if not debug:
					msg += "Unknown error"
				else:
					raise e
			cli.recover()
			break
	print(msg)

