import math
from evogfuzz.evogerrors import EvoGErrors
import time

st = time.time()

# This function contains various errors that must be found and classified.
def calculator(inp: str) -> float:
    if not str(inp).find("inc") == -1:
        return eval(str(inp), {"inc": math.increment}) # math.increment does not exist -> AttributeError

    if not str(inp).find("factorial") == -1:
        return eval(str(inp))

    if not str(inp).find("is_int") == -1:
        return eval(str(inp))
    
    return eval(
        str(inp), {
            "sqrt": math.sqrt, # square roots of negative numbers are not defined -> ValueError
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log # the logarithm is only defined for positive numbers -> ValueError
            }
    )

def factorial(n):
    if n >= 2:
        return n * factorial(n) # infinite recursion -> RecursionError
    else:
        return 1

def is_int(inp):
    assert isinstance(inp, int) # if inp is not an integer -> AssertionError
    return True

# Included exceptions with example inputs
# AssertionError -> is_int(5.2)
# AttributeError -> inc(5)
# RecursionError -> factorial(5)
# SyntaxError -> leading zero
# TypeError -> len(5)
# ValueError -> sqrt(-1)
# ZeroDivisionError -> 5 / 0


from fuzzingbook.Grammars import Grammar, is_valid_grammar

"""
This grammar covers all potentially valid inputs to the calculator function,
including mathematical expressions like square roots, trigonometric functions, factorial, division, incrementing
and length of a number, as well as checking whether a number is an integer.
"""
CALCGRAMMAR: Grammar = {
    "<start>":
        ["<start1>"],

    "<start1>":
        ["<expr>", "<term> / <term>"],

    "<expr>":
        ["<function>(<term>)"],

    "<function>":
        ["sqrt", "tan", "cos", "sin", "log", "len", "inc", "factorial", "is_int"],
    
    "<term>":
        ["-<value>", "<value>"], 
    
    "<value>":
        ["<integer>.<integer>", "<integer>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
}
    
assert is_valid_grammar(CALCGRAMMAR)

# Initial inputs that serve as a starting point for the fuzzer
initial_inputs = []

# Initialisation of the EvoGError instance
epp = EvoGErrors(
    grammar=CALCGRAMMAR,
    program=calculator,
    inputs=initial_inputs,
    no_bug_iterations = 3,
    iterations = 10
)

# start the fuzzing
found_exception_inputs = epp.fuzz()
print(f"EvoGFuzz found {len(found_exception_inputs)} Exception types!")

# print the found exception types
for inp in list(found_exception_inputs):
    print(str(inp))

# print the probabilistic grammar
print(epp.get_last_grammar())

# for the evaluation experiments (saves the output in a file)
# uncomment for evaluation
"""
et = time.time()
elapsed = et - st
grammar_output = epp.get_last_grammar()

# Specify the correct path to the output file
with open("evogerrors_output.txt", "a") as f:
    f.write("Runtime: "+str(elapsed)+"\n")
    f.write("Exceptiontypes: "+str(len(found_exception_inputs))+"\n")
    f.write(str(grammar_output))
"""