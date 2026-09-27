# C-Minus Compiler

A one-pass compiler for **C-minus**, a small subset of C (from K. Louden, *Compiler Construction: Principles and Practice*), written in Python for the Compiler Design course at Sharif University of Technology (Spring 2025).

The compiler reads a source file, and in a single pass over the token stream it scans, parses, checks semantics and generates three-address code. Errors at each stage are reported and the compiler keeps going instead of stopping at the first one.

> **Branches.** `final_code` holds the complete compiler. `scanner` (phase 1, lexical analysis only) and the `*_phase2` / `*_phase3` branches are kept as the history of the three course phases.

## Pipeline

```
input.txt ──► Scanner ──► LL(1) Parser ──► Semantic actions / Code generator ──► output.txt
                │              │                     │
                │              ├── parse_tree.txt    └── semantic_errors.txt
                │              └── syntax_errors.txt
                └── lexical errors (phase-1 scanner: token.txt, symbol_table.txt, lexical_errors.txt)
```

### 1. Scanner
A hand-written, DFA-style scanner that is called on demand by the parser (`get_next_token`).

- Token classes: `KEYWORD` (`if else void int while break return`), `ID`, `NUM`, `SYMBOL` (`; : , [ ] ( ) { } + - * / = == <`), plus whitespace and `/* ... */` comments.
- Lexical errors: invalid characters, malformed numbers (e.g. `1gh`), unmatched `*/`, and unclosed comments. The scanner records the error and resumes at the next character.

### 2. Parser
A predictive **LL(1) recursive-descent parser**, with one method per grammar non-terminal (`construct_Program`, `construct_Expression`, ...). The grammar was rewritten to remove left recursion and left-factored, which is where the `...Prime` and `...Zegond` non-terminals come from.

- Productions are chosen with the FIRST/FOLLOW (predict) sets of the transformed grammar.
- **Panic-mode error recovery.** When the lookahead does not fit, the parser either reports a *missing* token and continues, or discards the *illegal* token, depending on whether the lookahead is in the FOLLOW set of the current non-terminal. It also reports an *unexpected EOF*.
- The parse tree is printed with indentation to `parse_tree.txt`.

### 3. Semantic analysis
Semantic routines run as action symbols inside the parser, with a scoped symbol table (`name, type, address/attributes, scope`). Checks:

- use of undeclared identifiers
- variables declared with type `void`
- `break` outside a `while` loop
- operand type mismatches (e.g. `int` vs. array)
- wrong number of arguments and wrong argument types in function calls

### 4. Code generation
A syntax-directed translator using a semantic stack emits three-address code into `output.txt`:

```
(ADD|SUB|MULT|LT|EQ, a, b, result)   (ASSIGN, src, dst, )
(JP, target, , )   (JPF, cond, target, )   (PRINT, value, , )
```

Operands are direct addresses, `#constant` immediates or `@indirect` addresses. The generator handles expressions, assignments, arrays and indexing, `if`/`else`, `while` with `break`, function definitions and calls with parameter passing and return values, and the built-in `output(...)`.

## Usage

Requires Python 3 and no other packages.

```bash
git checkout final_code
# write your program into input.txt
python3 Compiler.py
```

Output files, written next to `Compiler.py`:

| File | Content |
|---|---|
| `output.txt` | generated three-address code (one numbered instruction per line) |
| `parse_tree.txt` | indented parse tree |
| `syntax_errors.txt` | syntax errors with line numbers, or `There is no syntax error.` |
| `semantic_errors.txt` | semantic errors with line numbers |

### Example

```c
void main(void) {
    int i;
    i = 0;
    while (i < 5) {
        output(i);
        i = i + 1;
    }
}
```

The `input.txt` in the repository is deliberately broken (bad characters, a malformed number, a stray comment) so that it exercises the scanner's and parser's error recovery.

## Tests

`testcases - phase1/` and `testcases - phase1 - part2/` contain the course test programs for the scanner, each with the expected `tokens.txt`, `symbol_table.txt` and `lexical_errors.txt`.

## Authors

- AmirAli Sheikhi ([@Amiraliii29](https://github.com/Amiraliii29))
- Mehrshad Dehghani ([@Mehrshad-D](https://github.com/Mehrshad-D))
