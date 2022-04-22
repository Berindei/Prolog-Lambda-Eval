from functools import reduce

def listToString(l, extraspace=""):
	if len(l)==0: return "[]"
	body = reduce(lambda x,y: f"{x},{extraspace}{y}", l[1:], l[0])
	return f"[{body}]"
