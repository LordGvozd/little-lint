import ast

code = """
def main():
    pass
"""

print(ast.parse(code).body[0].__dict__)
