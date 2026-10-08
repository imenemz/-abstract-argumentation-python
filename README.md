# Abstract Argumentation in Python

A university project implementing an algorithm to compute **complete**, **grounded**, and **preferred** extensions of abstract argumentation frameworks.

Developed by **Oumayma Becher and Imene Mazouz** during the **L3 Artificial Intelligence programme at Université Côte d’Azur, 2026**.

## Overview

An argumentation framework is a directed graph:

- Each node represents an argument.
- Each directed edge represents an attack from one argument to another.

The goal is to determine which sets of arguments can be accepted under different argumentation semantics, including in graphs containing cycles.

## Input Format

Graphs are described using argument declarations and attack relationships:

```text
arg(a).
arg(b).
arg(c).
att(a,b).
att(b,c).
```

Here, `a` attacks `b`, and `b` attacks `c`.

For this example, the complete, grounded, and preferred extensions are all `{a, c}`.

## Algorithm

The implementation follows a **generate-and-test** approach:

1. Parse the arguments and attack relationships.
2. Recursively generate every subset of arguments.
3. Check whether each subset is conflict-free.
4. Check admissibility: the subset must defend all its members.
5. Check completeness: it must also contain every argument it defends.
6. Derive the grounded and preferred extensions from the complete extensions.

## Implemented Semantics

| Semantics | Definition |
|---|---|
| Complete | An admissible set containing every argument it defends |
| Grounded | The least complete extension under set inclusion |
| Preferred | Admissible sets that are maximal under set inclusion |

The implementation computes the grounded extension by intersecting the complete extensions. Preferred extensions are obtained by selecting the inclusion-maximal complete extensions.

## Project Structure

- `arg.py`: Graph parsing, extension computation, and built-in demonstration cases.

## Requirements

- Python 3
- No external libraries are required.

## Running the Project

Download or clone the repository, then run:

```bash
python arg.py
```

On systems where Python 3 uses a separate command:

```bash
python3 arg.py
```

The script prints each example graph and its complete, grounded, and preferred extensions.

To try another graph, modify a `run(...)` call in the demonstration section of `arg.py`.

## Demonstration Cases

The script includes:

- A chain of attacks
- Two mutually attacking arguments
- Mutual attacks with an additional node
- A directed cycle of three arguments
- A branching attack graph
- A self-attacking argument example

## Limitations and Known Issue

This is an educational brute-force implementation intended for small graphs.

For `n` arguments, it generates `2^n` subsets. Property checks and comparisons between extensions add further computational cost.

The current parser removes self-attacking arguments and all attacks involving them. This changes the original framework and can produce incorrect extensions. General support for self-attacks requires preserving these arguments and relationships during parsing.

## Academic Context

The assignment required:

- An executable implementation for graphs with and without cycles
- Computation of complete, grounded, and preferred extensions
- A short presentation explaining the algorithm
- A live demonstration
