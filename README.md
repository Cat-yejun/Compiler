# 📘 Compilers Term Project


## 📑 Project Overview

This project implements an **SLR Parser** based on a context-free
grammar (CFG).\
The work includes: - Removing ambiguity from the original CFG
- Constructing an SLR Parsing Table
- Implementing the parser with error checking
- Generating a parse tree
- Testing with multiple input cases (VDECL, FDECL, CDECL, ASSIGN)

------------------------------------------------------------------------

## 🛠️ Features

-   **Ambiguity-free CFG**\
    We refined the original grammar to resolve ambiguities in:

    -   `EXPR`: precedence and associativity between `addsub` and
        `multdiv`
    -   `COND`: nesting and precedence in conditional expressions

    ### Non-ambiguous CFG Example

    <img width="489" height="561" alt="image" src="https://github.com/user-attachments/assets/c9f83073-b225-4a1c-b142-69f9dcdbacbf" />

    ### Ambiguity in EXPR

    The original grammar allowed multiple parse trees for the same
    expression.\
    Example: <img width="556" height="125" alt="image" src="https://github.com/user-attachments/assets/6602d1ca-eb1e-4920-b13a-d41968e25c60" />


    By restructuring `EXPR → T addsub EXPR | T` and
    `COND → CONDT comp COND | CONDT`,\
    we eliminated ambiguity and ensured a deterministic parse.

-   **SLR Parsing Table**

    -   Auto-generated using a provided tool (https://jsmachines.sourceforge.net/machines/slr.html)
    -   Converted into `numpy` array for program use

-   **Parser Implementation**

    -   Shift/Reduce actions based on parsing table
    -   Error detection with expected token suggestions
    -   Parse tree construction and export to `output.txt`

------------------------------------------------------------------------

## 📂 Project Structure

    ├── main.py            # Entry point of parser
    ├── table_call.py      # Converts parsing table from Excel → numpy
    ├── SLR_Table.py       # Preprocessed SLR Parsing Table
    ├── tree.py            # Parse tree construction
    ├── input              # Example input file
    │    ├── ASSIGN.txt
    │    ├── CDECL.txt
    │    ├── FDECL.txt
    │    └── VDECL.txt
    ├── output.txt         # Parsing results
    └── README.md          # Project documentation

------------------------------------------------------------------------

## 🚀 How to Run

### Requirements

-   Python 3.x
-   Modules: `numpy`, `pandas`, `sys`, `os`

### Execution (example)

``` bash
python main.py input/ASSIGN.txt
```

Results: - Console prints parsing process (`accepted!` or error)
- Parse tree is saved into `output.txt`

------------------------------------------------------------------------

## 📊 Execution Examples

### ✅ Variable Declaration (VDECL)

**Input:**

    vtype id semi vtype id assign boolstr semi

**Output:**\
Accepted, parse tree generated.

<img width="85" height="107" alt="image" src="https://github.com/user-attachments/assets/812fa109-d1d4-4c00-a0b0-54131581190b" />


------------------------------------------------------------------------

### ❌ Variable Declaration Error

**Input:**

    vtype id semi id assign boolstr semi

**Output:**\
Error detected, `vtype` expected.

<img width="186" height="93" alt="image" src="https://github.com/user-attachments/assets/4c993e55-046b-4c1e-8bf8-744929915d5a" />


------------------------------------------------------------------------

## 🌳 Parse Tree Visualization

-   Built using `Tree` and `TreeNode` classes
-   Printed to console and saved into `output.txt`

------------------------------------------------------------------------

## ⚠️ Warnings

-   Ensure all required `.py` files are in the same directory.
-   Input must be tokenized and space-separated.
-   The parser reports the most probable expected tokens when errors
    occur.

------------------------------------------------------------------------

✨ With this project, we successfully implemented a working **SLR
Parser** with ambiguity-free CFG, robust error handling, and parse tree
visualization - Got an A+ :)
