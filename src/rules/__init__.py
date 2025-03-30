from src.core import Scaner
from src.rules.ast_rules import ast_rules
from src.rules.file_rules import file_rules
from src.rules.line_rules import line_rules

scanner = Scaner()

for rule in file_rules.get_all_rules():
    scanner.add_file_rule(rule.checker)

for rule in line_rules.get_all_rules():
    scanner.add_line_rule(rule.checker)

for rule in ast_rules.get_all_rules():
    for ast_type in rule.args:
        scanner.add_ast_rule(ast_type, rule.checker)
