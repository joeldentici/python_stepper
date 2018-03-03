# Python Stepper
We are working on implementing an algebraic stepper for Python 3, similar to the one for Racket (previously known as PLT Scheme).

## Installation
For now there isn't any fancy installation package, so you will need to clone the repository to use the stepper. Before you do that though, you will need to take care of installing the necessary dependencies. So here is what you need to do:

1. Install Python 3 if you don't already have it. How this is done depends on your operating system. If you are using Windows or macOS, you probably download some sort of installer. If you are using a Linux distribution, you should use your package manager.
1. Install pip3. This is the preferred package manager for Python 3. This might have been installed when you installed Python 3.
1. Install the `astor` Python module.
	* `$ pip3 install astor`

Now you can clone the repository:
```sh
$ cd <wherever you want to put it>
$ git clone git@github.com:joeldentici/python_stepper.git
$ cd python_stepper
```



## Usage
You can evaluate a Python script with the stepper. Remember that this is a work in progress, so not every valid Python program will work with the stepper yet.

```sh
$ cd <repo directory>
$ src/run_stepper.py <path to Python script> <command line argument>*
```

This will start the script you specify in the stepper. The stepper will allow you to step forward and backward as makes sense, and exit whenever you are ready.

## Milestones

1. [x] Proof of Concept (Fall Quarter)
1. [x] Basic reporting of reductions
1. [x] Useful reporting of reductions
1. [x] Proper tracking of mutation
1. [ ] All basic syntactic forms covered
1. [ ] Advanced syntactic forms
1. [ ] A beginning student friendly UI

Definitions:

* Basic syntactic forms - simple expressions, imperative control flow constructs, function abstraction/application, strict comprehensions, ssa
* Advanced syntactic forms - generators, coroutines, lazy comprehensions
* Beginning student friendly UI - GUI, not terminal
* Proper tracking of mutation - all assignments
* Useful reporting -- statements/expressions are expanded, identifiers are substitued for their values, and then the statements/expressions are evaluated