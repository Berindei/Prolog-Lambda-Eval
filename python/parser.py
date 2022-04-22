from python.ast import AST
from python.ast import Type as Node
from enum import Enum
from python.errors import LexerError, ParserError, PrologParserError

Tokens = Enum("Tokens", "LAMBDA COMMA DOT OPEN_PARAN CLOSE_PARAN VAR VARLIST AST")

def toAST(arg, env):
	return build_tree(tokenize(arg), env)

def tokenize(text):
	res = []
	i = 0
	while i < len(text):
		ch = text[i]
		if ch == 'λ':   res.append((Tokens.LAMBDA,))
#		elif ch == ',': res.append((Tokens.COMMA))
		elif ch == '.': res.append((Tokens.DOT,))
		elif ch == '(': res.append((Tokens.OPEN_PARAN,))
		elif ch == ')': res.append((Tokens.CLOSE_PARAN,))
		elif ch.isalpha():
			st = i
			while i<len(text):
				if text[i].isalpha(): i += 1
				else: break
			varname = text[st:i]
			res += [(Tokens.AST, varname)] if varname.isupper() else [(Tokens.VAR, varname)]
			i -= 1
		else:
			raise LexerError(f"Unknown character at position {i}")
		i += 1
	return res

def build_tree(tokens, env):
	inter = []
	i=0;
	while i<len(tokens):
		tkn = tokens[i]
		if tkn[0] != Tokens.LAMBDA: inter+=[tkn]
		else: 
			var = []
			i+=1
			while i<len(tokens):
				if tokens[i][0] == Tokens.VAR: var+=tokens[i][1]
				elif tokens[i][0] == Tokens.DOT: break
				else:
					raise ParserError("Incorrect formating of a lambda abstraction") 
				i+=1
			inter += [(Tokens.LAMBDA, ), (Tokens.VARLIST, var)]
		i+=1

	return solve(inter, env)


def find_closing(tokens):
	count = 1
	for i in range(1, len(tokens)):
		if tokens[i][0]==Tokens.OPEN_PARAN: count += 1
		elif tokens[i][0]==Tokens.CLOSE_PARAN: count -= 1
		if count==0: return i
	raise ParserError("Unmatched paranthesis")

def solve_piece(tokens, env):
	cur = tokens[0]
	if cur[0] == Tokens.OPEN_PARAN:
		end = find_closing(tokens[0:])
		return (solve(tokens[1:end], env), end+1)
	elif cur[0] == Tokens.LAMBDA:
		partial = solve(tokens[2:], env)
		return (AST(Node.λ, (tokens[1][1], partial)), len(tokens))
	elif cur[0] == Tokens.VAR:
		return (AST(Node.var, cur[1]), 1)
	elif cur[0] == Tokens.AST:
		return (env[cur[1]], 1)
	else: raise ParserError("Incorrect lambda term syntax")

def solve(tokens, env):
	i = 0
	pieces = []
	while i<len(tokens):
		piece, cnt = solve_piece(tokens[i:], env)
		pieces += [piece]
		i += cnt

	sol = pieces[0]

	for piece in pieces[1:]:
		sol = AST(Node.app, (sol, piece))

	return sol

def findComma(string):
	cnt = 0
	for i in range(len(string)):
		ch = string[i]
		if   ch=='(': cnt+=1
		elif ch==')': cnt-=1
		elif ch==',' and cnt==0: return i
	raise PrologParserError()

def fromProlog(prologString):
	prologString = prologString.replace(" ", "")
#	print(f"Working on processing this from prolog:{prologString}")

	if prologString.startswith("lambda"):
		listEnd = prologString.find("]")
		listString = prologString[8:listEnd]
		body = fromProlog(prologString[listEnd+2:-1])
		return AST(Node.λ, (listString.split(","), body))

	if prologString.startswith("app"):
		comma = 4+findComma(prologString[4:])
		func = fromProlog(prologString[4:comma])
		arg = fromProlog(prologString[comma+1:-1])
		return AST(Node.app, (func, arg))

	else:
		return AST(Node.var, prologString)




