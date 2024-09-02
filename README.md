# Writing an intepreter from scratch

> This repo follows the implementation in the book https://craftinginterpreters.com, by Robert Nystrom.

## Why bother doing this at all?
Few projects offer the opportunity to explore the key logical components of a computer system. By "logical components," I mean elements that aren't directly tied to hardware but significantly influence how code is executed—essentially a vertical view of the computer stack. Starting from something as simple as `print("Hello World!")`, you can trace the journey through interpretation and compilation, ultimately reaching the machine code: `48 C7 C7 01 00 00 00 48 C7 C0 01 00 00 00 48 89 E6 B8 01 00 00 00 0F 05`.

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
   - Getting to the backend of the language. Here we must think about the tradeoffs of our language - which computer architecture to target and so on.
   - To get around that "lock-in" with computer architectures, a common practice is to generate code for **virtual machines**. It is generally called bytecode, because each instruction is ofted a single byte long.
7. **Virtual machine**
   - After compiling to bytecode, your work isn't finished because no chip directly understands bytecode. You have two options: 
     1. Write a mini-compiler for each target architecture to convert the bytecode to native code. This simplifies the last stage and allows reuse of most of the compiler pipeline across different architectures.
     2. Write a virtual machine (VM) that emulates a hypothetical chip supporting your virtual architecture. Although running bytecode in a VM is slower due to runtime simulation, it offers simplicity and portability since the VM can run on any platform with a C compiler.
8. **Runtime**
   - After transforming the user's program into an executable form, the final step is running it. If it's compiled to machine code, the operating system loads the executable. If it's compiled to bytecode, the VM loads and runs it.
   - Most languages require runtime services, such as garbage collection for memory management or type tracking for "instance of" tests. These services make up the runtime. In fully compiled languages, like Go, the runtime is embedded in each executable. For languages run in a VM or interpreter, like Java, Python, and JavaScript, the runtime resides within the VM.

### Compilers vs Interpreters
Here, the fruit vs vegetable analogy is perfect. Some fruits are vegetables, and vice-versa. The key difference is that fruit is a _botanical_ term, while vegetable is a _culinary_ term.

- In terms of programming languages, **compiling** is an _implementation technique_ that involves translating a source language into some other - usually lower-level - form. When you generate **bytecode** or **machine code** you are compiling. When you transpile to another high-level language, you are compiling too.
- When we say a language implementation "is a compiler", we mean it **translates source code to some other form but does not execute it**. The user has to take the resulting output and run it themselves
- Conversely, when we say an implementation "is an interpreter", we mean it **takes in source code and executes it immediately. It runs programs "from source"**.