# Python Stepper
We are working on implementing an algebraic stepper for Python 3, similar to the one for Racket (previously known as DrScheme).

## What is a stepper?
A stepper is a tool that allows a programmer to see how their program is evaluated. It works by rewriting the program using algebraic transformations, that preserve its semantics, but allow the reconstruction of the source code expressions at runtime. It then allows the programmer to see how reduction rules are applied to expressions to evaluate them.

The stepper does not evaluate the program itself. Instead, it produces a program whose expressions will evaluate to equivalent values, but is also annotated with additional code that allows the stepper's runtime system to show how those expressions are evaluated. Instead of providing its own evaluator, the stepper produces calls into a library that the transformed program will use at runtime. The transformed program can be evaluated in any environment the original program can be.

The finished stepper will differ from the one in Racket because of the semantic differences in the languages. Racket programs tend to be composed of immutable data and expressions, while Python programs tend to be composed of mutable data and statements. This means that in addition to showing the reduction of expressions to values, the Python stepper must be able to show how statements transform program state. We will model mutation algebraically to do this.

## Is it a stepper yet?
We are building this in stages. The code here does not yet meet the definition of a stepper above.

Right now we are working on the source-to-source compiler part of the stepper. This is what annotates the original source code to produce the transformed program that reports how itself is evaluated. The input and output are both Python 3 programs.

## Usage
Currently there isn't a full UI shell built around the core of the tool (which itself isn't finished).

To see what it does right now, you must first transform your source code with the source-to-source compiler:

```sh
$ python3 stepper/transform.py < input.py > stepper/output.py
```

It is important to put the output right now into the stepper directory because the import of the stepper's own library is very crude right now. It assumes that the stepper's library module that is imported will be globally available or in the same directory as the script importing it.

There are no plans to change this until we create a UI to use the tool, because barring making the stepper library globally available, the relative locations of your program and the library will be dependent on how we implement the UI.

Next you can run your transformed program, just as you would the original. For example, if you transformed `test.py`, included right now in the repository root, then you can run it as:

```sh
$ python3 stepper/test.py {NUMBER} {NUMBER} {NUMBER}
```

where {NUMBER} are number literals in Python 3.

## Todo

- [x] Be able to transform Python 3 programs (PoC)
- [ ] Annotation of lambda expressions and function definitions
- [ ] Annotation of application
- [ ] Annotation of primitive expressions
- [ ] Annotation of primitive statements
- [ ] Annotation of mutating statements
- [ ] Support for calling into user code from library functions (higher order library functions)
- [ ] Support for mutation of program state by library functions
- [ ] Support for interactive evaluation of the program
- [ ] Full terminal-based UI to evaluate program

At this point, a minimal version of a fully usable stepper will be complete.

One of the goals of this project is to produce a tool that is easy to use for students in entry level courses. To support this, we would also like to create web-based interface if time permits

- [ ] Extend the stepper core implementation to be usable by a variety of UIs
- [ ] Create a web application (server side) capable of transforming a program and running it with suspension
- [ ] Create a client side application that drives the interactive evaluation of the program by asking the server to resume evaluation
