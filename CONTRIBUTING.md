

# Adding a Check  

To add a new check, follow these steps:  

- Add a `YourViolation(Violation)` class in `src.models`. In the `text` attribute, describe what is wrong. In the `type` field, specify the violation type (`ViolationType.ERROR`, `ViolationType.WARNING`, `ViolationType.NOT_RECOMMENDED`).  
- Create a function in one of the files: `src.rules.file_rules`, `src.rules.line_rules`, or `src.rules.ast_rules`, and wrap it in the appropriate decorator.  
- Write tests for the function in `tests`.  

## Rule Types  

There are three types of rules:  

- **File rules** (search for violations across the entire file code)  
- **Line rules** (search for violations in each line)  
- **AST rules** (search for violations in a specific syntax construct)  

Rules should only be added to their corresponding file (file rules in `src.rules.file_rules`, line rules in `src.rules.line_rules`, AST rules in `src.rules.ast_rules`)!  

### File Rules  

To add a rule that searches for violations in the entire file code, use the `@file_rules.rule` decorator. Your function should take one argument—the entire file code.  

```python  
@file_rules.rule  
def find_some_violation(code: str) -> Violation | None:  
    if "violation" in code:  # For example  
        return YourViolation(1)  # 1 is the line number  
```  

### Line Rules  

To add a rule that searches for violations in each line of the file, use the `@line_rules.rule` decorator. Your function should take two arguments—the line code and its line number in the file.  

```python  
@line_rules.rule  
def break_line_after_bin_op(line: str, number: int) -> Violation | None:  
    if re.match(r"\w+\s*\+\s*$", line):  
        return LineBreakAfterBinOp(number)  
```  

### AST Rules  

To add a rule that searches for violations in a specific syntax construct, use the `@ast_rules.rule(ast.ThingYouWantToHandle, ast.AnotherThing)` decorator. Your function should take one argument—the node corresponding to one of the types specified in the decorator's arguments. You can also take a second argument—the node's source code.  

```python  
@ast_rules.rule(ast.Import)  
def import_on_one_line(node: ast.Import) -> Violation | None:  
    if len(node.names) > 1:  
        return ManyImportOnOneLine(node.lineno)  
```  


