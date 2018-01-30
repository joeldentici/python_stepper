# Python Stepper
We are working on implementing an algebraic stepper for Python 3, similar to the one for Racket (previously known as PLT Scheme).

## Usage
You can evaluate a Python script with the stepper. Remember that this is a work in progress, so not every valid Python program will work with the stepper yet.

```sh
$ src/run_stepper.py <path to Python script> <command line argument>*
```

## Milestones

1. [x] Proof of Concept (Fall Quarter)
1. [x] Basic reporting of reductions
1. [x] Useful reporting of reductions
1. [ ] All basic syntactic forms covered
1. [ ] Proper tracking of mutation
1. [ ] Advanced syntactic forms 
1. [ ] A beginning student friendly UI

Definitions:

* Basic syntactic forms - simple expressions, imperative control flow constructs, function abstraction/application, strict comprehensions, ssa
* Advanced syntactic forms - generators, coroutines, lazy comprehensions
* Beginning student friendly UI - GUI, not terminal
* Proper tracking of mutation - all assignments
* Useful reporting -- statements/expressions are expanded, identifiers are substitued for their values, and then the statements/expressions are evaluated