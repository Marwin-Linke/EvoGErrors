from fuzzingbook.Grammars import Grammar, is_valid_grammar
from fuzzingbook.ProbabilisticGrammarFuzzer import is_valid_probabilistic_grammar
from typing import Dict, List, Tuple

class MultiProbabilisitcGrammar:

    ProbablisitcGrammar = Dict[str, List[Tuple[str, Dict[str, str]]]]

    def __init__(self, grammar: Grammar) -> None:

        assert(is_valid_grammar(grammar)), "Exit! Grammar is not valid."

        # Creates empty multi probablistic grammar structure
        self._multi_probabilistic_grammar = {}
        for nonterminal, productions in grammar.items():
            self._multi_probabilistic_grammar[nonterminal] = []
            for production in productions:
                self._multi_probabilistic_grammar[nonterminal].append((production, {}))


    def append(self, exception: str, probablistic_grammar: ProbablisitcGrammar):
        
        assert(is_valid_probabilistic_grammar(probablistic_grammar)), "Exit! Probabilistic grammar is not valid."
        
        # Appends probabilities to corresponding exception
        for nonterminal, productions in probablistic_grammar.items():
            for i in range(len(productions)):
                probability = probablistic_grammar[nonterminal][i][1]['prob']
                self._multi_probabilistic_grammar[nonterminal][i][1][exception] = probability

    def __str__(self) -> str:
        return self.display()
        
    def __repr__(self) -> str:
        return repr(self._multi_probabilistic_grammar)
    
    def display(self) -> str:
        display = ""
        for nonterminal, productions in self._multi_probabilistic_grammar.items():
            first_production = (productions[0][0], {key: round(value, 4) if value is not None else None for key, value in productions[0][1].items()})
            display += f"{nonterminal}:\n   {str(first_production)}\n"
            for production in productions[1:]:
                rounded_probabilities = {key: round(value, 4) if value is not None else None for key, value in production[1].items()}
                pair = (production[0], rounded_probabilities)
                display += f" | {str(pair)}\n"
        return display