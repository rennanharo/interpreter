# Writing an intepreter from scratch

> This repo follows the implementation in the book https://craftinginterpreters.com, by Robert Nystrom.

## Why bother doing this at all?
Few projects give you the opportunity to touch on most logical parts of a computer. By logical parts I mean parts that are not really related to hardware so much, but rather parts that will directly affect how code gets executed -- almost like a vertical view of the computer stack: start from a simple `print("Hello World!")`, to tokens, to AST, to semantics to bytecode to `48 C7 C7 01 00 00 00 48 C7 C0 01 00 00 00 48 89 E6 B8 01 00 00 00 0F 05`.

## Introduction
### Parts of a language

![img](https://craftinginterpreters.com/image/a-map-of-the-territory/mountain.png)

1. **Scanning = lexing = lexical analysis**
   -  A scanner (or lexer) takes in the linear stream of characters and chunks them together into a series of something more akin to “words”. In programming languages, each of these words is called a token. Some tokens are single characters, like `(` and `,`. Others may be several characters long, like numbers (`123`), string literals (`"hi!"`), and identifiers (`min`).
   - "Lexical" comes from the Greek root "lex", meaning “word”.
2. **Parsing**
   - A parser takes the flat sequence of tokens and builds a tree structure that mirrors the nested nature of the grammar. These trees have a couple of different names—parse tree or abstract syntax tree—depending on how close to the bare syntactic structure of the source language they are. In practice, language hackers usually call them syntax trees, ASTs, or often just trees.
   - **Parsing has a long, rich history in computer science that is closely tied to the artificial intelligence community. Many of the techniques used today to parse programming languages were originally conceived to parse human languages by AI researchers who were trying to get computers to talk to us.**
3. **Static analysis**
   - In an expression like `a + b`, we know we are adding `a` and `b`, but we don't know what those names refert to. Are they local variables? Global? Where are they defined?
   -  The first bit of analysis that most languages do is called **binding** or **resolution**. For each identifier, we find out where that name is defined and wire the two together. This is where **scope** comes into play—the region of source code where a certain name can be used to refer to a certain declaration.
   - If the language is statically typed, this is when we type check. Once we know where `a` and `b` are declared, we can also figure out their types. Then if those types don’t support being added to each other, we report a type error.
     - If dynamically typed, we do this later, at **runtime**
   - We must store all that information (metadata) somewhere. There are three viable options:
     - Store it right back as **attributes** on the syntax tree itself (extra fields in the nodes)
     - As a lookup table off to the side. AKA **symbol table**
     - Transform the tree into an entirely new data structure
   > Everything up to this point is considered the **front end** of the implementation.
4. **Intermediate representations**
   - You can think of the compiler as a pipeline where each stage’s job is to organize the data representing the user’s code in a way that makes the next stage simpler to implement.
5. **Optimization**
   - Once we understand what the user’s program means, we are free to swap it out with a different program that has the same semantics but implements them more efficiently—we can optimize it.
   - A simple example is constant folding: if some expression always evaluates to the exact same value, we can do the evaluation at compile time and replace the code for the expression with its result. If the user typed in this:
   - `pennyArea = 3.14159 * (0.75 / 2) * (0.75 / 2);`, we could do all of that arithmetic in the compiler and change the code to: `pennyArea = 0.4417860938;`
   > This wraps up the **middle end** of the implementation.
6. **Code generation**
   - 