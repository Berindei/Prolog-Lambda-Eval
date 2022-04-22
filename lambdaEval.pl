%appears(+Value, +List) true if Value in List
appears(X, [X|T]).
appears(X, [_|T]) :- appears(X, T).

%notin(+Value, +List)
notin(X, [Y|T]) :- X \= Y, notin(X, T).
notin(X, []).

%fresh(-Value, +Total, -NewTotal) returns a new value not in Total and gives the new total of values
fresh(W, T, [W|T]) :- appears(V, T), W is V+1, notin(W, T).
fresh(0, [], [0]).

%alphaConv(+LambdaIn, +ToReplace, +ReplaceTo, -LambdaOut) replaces ToReplace with ReplaceTo in LambdaIn until a new binder is met
alphaConv(lambda(Bind, Body), X, Y, lambda(Bind, NBody)) :- notin(X, Bind), alphaConv(Body, X, Y, NBody), !.
alphaConv(lambda(Bind, Body), X, Y, lambda(Bind, Body)) :- appears(X, Bind), !.
alphaConv(app(M, N), X, Y, app(NM, NN)) :- alphaConv(M, X, Y, NM), alphaConv(N, X, Y, NN), !.
alphaConv(X, X, Y, Y).
alphaConv(Z, X, Y, Z) :- Z\=X.

%alphaEchiv(+LamndaIn, -LambdaOut, +InitialUsed, -NewUsed) outputs an alpha equivalent lambda term that uses different binders everywhere
alphaEchiv(lambda([H|T], Body), lambda([Val|NBind], NBody), InitialUsed, Used) :- fresh(Val, InitialUsed, IntUsed),
                                                                    alphaEchiv(lambda(T, Body), Int, IntUsed, Used),
                                                                    alphaConv(Int, H, Val, lambda(NBind, NBody)), !.
alphaEchiv(lambda([], Body), lambda([], Next), InitialUsed, Used) :- alphaEchiv(Body, Next, InitialUsed, Used), !.
alphaEchiv(app(M, N), app(NM, NN), InitialUsed, Used) :- alphaEchiv(M, NM, InitialUsed, Int), alphaEchiv(N, NN, Int, Used), !.
alphaEchiv(X, X, Used, Used).

%subst(+LambdaIn, +ToReplace, +ReplaceTo, -LambdaOut) replaces ToReplace with ReplaceTo everywhere
subst(lambda(Bind, Body), X, Y, lambda(Bind, NBody)) :- subst(Body, X, Y, NBody), !.
subst(app(M, N), X, Y, app(NM, NN)) :- subst(M, X, Y, NM), subst(N, X, Y, NN), !.
subst(X, X, Y, Y) :- !.
subst(Z, X, Y, Z).

%bnf(+LambdaIn, -LambdaOut) outputs the beta normal form of LambdaIn
bnf(lambda(Bind, Body), lambda(Bind, NBody)) :- bnf(Body, NBody), !.
bnf(app(lambda([X]  , Body), Y), Next)             :- subst(Body, X, Y, Int), bnf(Int, Next), !.
bnf(app(lambda([X|T], Body), Y), lambda(T, NBody)) :- subst(Body, X, Y, Int), bnf(Int, NBody), !.
bnf(app(M, N), app(NM, NN)) :- bnf(M, NM), bnf(N, NN), NM\=lambda(_, _), !.
bnf(app(M, N), Next)        :- bnf(M, NM), bnf(N, NN), bnf(app(NM, NN), Next), !.
bnf(X, X).

%eval(+LambdaIn, -LambdaOut)
eval(X, Y) :- alphaEchiv(X, Int, [], Used), bnf(Int, Y).

%comb(+Name, -Lambda) some common combinators hardcoded
comb(plus, (lambda([a, b], lambda([f, x], app(app(a, f), app(app(b, f), x)))))).
comb(omega, lambda([x], app(x, x))).

%churchNum(+Num, -Lambda) outputs the lambda term representing the Church numeral of Num
churchNum(0, lambda([f, x], x)).
churchNum(A, lambda([f, x], app(f, Body))) :- A=\=0, B is A-1, churchNum(B, lambda([f, x], Body)).

%numChurch(-Num, +Lambda) outputs the number represented by the Church num Lambda
numChurch(0, lambda([F, X], X)).
numChurch(Ans, lambda([F, X], app(F, Body))) :- numChurch(Y, lambda([F, X], Body)), Ans is Y+1.