# Roadmap

This describes, what should be implemented

## Pep8

### Code Lay-out

- [X] Use 4 spaces for indentation level
- [X] Space instead of tabs
- [X] Maximum line length
- [X] Line break must be after binary operation
- [X] Top-level functions and class definition should be surrounded with two blank lines
- [ ] Method definitions inside a class are surrounded by a single blank line
- [ ] Code in the core Python distribution should always use UTF-8, and should not have an encoding declaratio
- [X] Imports must be on separate lines
- [X] Relative imports not recommend
- [ ] Module level dunders
- [ ] For triple-quoted strings, always use double quote characters to be consistent with the docstring convention in PEP 257

### Whitespace in Expressions and Statements

- [ ] Avoid extraneous whitespace inside parentheses, brackets, or braces
- [ ] Between a trailing comma and a following close parenthesis
- [ ] Before a comma, semicolon or colon
- [ ] Do not use spaces in slices
- [X] File must be ends with new line
- [ ] Before the open parenthesis that starts the argument list of a function call
- [ ] Immediately before the open parenthesis that starts an indexing or slicing
- [ ] More than one space around an assignment (or other) operator to align it with another
- [ ] Don't use spaces around `=` sign 
- [ ] Compound statements (multiple statements on the same line) are generally discouraged
- [ ] Every block must be on new line
- [ ] Trailing comma 

### Comments
- [ ] Comments should be complete sentences. The first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!)
- [ ] You should use one or two spaces after a sentence-ending period in multi-sentence comments, except after the final sentence
- [ ] Every comment must be on english
- [ ] Comment must start with space

### Docstrings
- [ ] Every function or method should starts with docstring

### Naming
- [ ] Avoid some characters
- [ ] ASCII compatibility
- [ ] Module should have short, all-lowercase names
- [ ] C-extension should have leading underscore (e.g `_socket`)
- [ ] Class names should normally use the CapWords
- [ ] Exception names should end with `Error`
- [ ] Function names should be lowercase
- [ ] Variable names also should be lowecase
- [ ] Constants should be in upper case

### Programming recommendations
- [ ] Use `Excpet` with concrete Exceptions
- [ ] Never use `==` with None, use `is` instead
- [ ] Use `starstwith` and `endswith` instead of slices
- [ ] Object type comparisons should always use isinstance() instead of comparing types directly
- [ ] For sequences, (strings, lists, tuples), use the fact that empty sequences are false
- [ ] Don’t compare boolean values to True or False using `==`

### Annotations
- [ ] Annotations for module level variables, class and instance variables, and local variables should have a single space after the colon
- [ ] There should be no space before the colon
- [ ] If an assignment has a right hand side, then the equality sign should have exactly one space on both sides

## Little-lint
- [ ] Forbid using `print()` use `logging` or `loguru` instead
- [ ] Forbid call function in top level (exclude assigns), use `if __name__ == "__main__"`

### Typing
 - [ ] Forbid using `Any` in annotations
 - [ ] Use only typed functions

### Standard library
- [ ] Forbid using f-strings in `logging`
- 

