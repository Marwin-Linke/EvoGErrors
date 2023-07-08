from typing import Dict, List, Set, Callable
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from evogfuzz.fitness_functions import fitness_function_failure
from evogfuzz.multi_probabilistic_grammar import MultiProbabilisitcGrammar
from evogfuzz.evogfuzz_class import EvoGFuzz
from fuzzingbook.Grammars import Grammar
from pathlib import Path
import builtins

class EvoGErrors:

    def __init__(
            self,
            grammar: Grammar,
            program: Callable,
            inputs: List[str] = [],
            fitness_function: Callable[[Input], float] = fitness_function_failure,
            min_iterations: int = 3,
            final_iterations: int = 10,
            working_dir: Path = None,
    ):
        self._grammar = grammar
        self._program = program
        self._inputs = inputs
        self._fitness_function = fitness_function
        self._min_iterations = min_iterations
        self._final_iterations = final_iterations
        self._working_dir = working_dir

        self._last_grammars = {}


    def get_all_error_types(self):
        """
        Retrieves all built-in exceptions.
        """
        built_in_exceptions = []
        for name in dir(builtins):
            obj = getattr(builtins, name)
            if isinstance(obj, type) and issubclass(obj, BaseException):
                built_in_exceptions.append(obj)
        return built_in_exceptions


    def _dynamic_oracle(self) -> Dict[Exception, List[Callable]]:
        """
        Creates a list of oracle for every type of exception.
        """
        functions = {}

        error_types = self.get_all_error_types()

        for error_type in error_types:
            error_type_name = error_type.__name__

            # Dynamically creates oracle function
            def dynamic_function(inp, error_type=error_type):
                def internal(inp):
                    try:
                        self._program(inp)
                        return False
                    except Exception as error:
                        if type(error) == error_type:
                            return True
                        return False

                return OracleResult.BUG if internal(inp) else OracleResult.NO_BUG

            # Renames function
            dynamic_function.__name__ = f"{error_type_name}_Oracle"

            # Adds function to dictionary
            functions[error_type] = dynamic_function

        return functions


    def fuzz(self) -> Dict[Exception, Set[Input]]:
        """
        Runs EvoGFuzz for every oracle for min_iterations.
        If a bug was found, changes maximum iterations and continues EvoGFuzz.
        """
        
        oracle_list: Dict[Exception, List[Callable]]  = self._dynamic_oracle()
        result = dict()

        # Visuals
        index = 0

        for oracle_exception, oracle_function in oracle_list.items():
            
            # Visuals
            index += 1
            length = len(oracle_list)
            print(f"[{index}/{length}] Currently searching for: {oracle_exception.__name__}")

            # Runs EvoGFuzz for min_iterations
            evo_fuzz = EvoGFuzz(self._grammar, oracle_function, self._inputs, self._fitness_function, self._min_iterations)
            found_exceptions = evo_fuzz.fuzz()

            # Checks if any bugs were found
            if len(found_exceptions) > 0:
                
                # Visuals
                print(f"[{index}/{length}] Looking deeper into: {oracle_exception.__name__}")

                # Continues EvoGFuzz for final_iterations
                evo_fuzz.change_max_iterations_to(self._final_iterations)
                result[oracle_exception] = evo_fuzz.fuzz(False)
                self._last_grammars[oracle_exception] = evo_fuzz.get_last_grammar()
        
        return result


    def get_last_grammar(self) -> MultiProbabilisitcGrammar:
        """
        Returns a multi probabilistic grammar that combines 
        all probabilistic grammars of each exception that found a bug.
        """
        multi_probabilistic_grammar = MultiProbabilisitcGrammar(self._grammar)

        for exception, grammar in self._last_grammars.items():
            multi_probabilistic_grammar.append(exception.__name__, grammar)
        
        return multi_probabilistic_grammar