import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import re

class EagleScriptIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("EagleScript IDE")
        self.root.geometry("800x600")
        
        # Toolbar
        self.toolbar = ttk.Frame(root)
        self.toolbar.pack(fill=tk.X)
        self.run_btn = ttk.Button(self.toolbar, text="Run (F5)", command=self.run_code)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        # Editor and Console
        self.editor = scrolledtext.ScrolledText(root, font=('Consolas', 12), wrap=tk.WORD)
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        self.console = scrolledtext.ScrolledText(root, font=('Consolas', 12), state='disabled')
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Sample code with * comments
        self.editor.insert(tk.END, """* Welcome to EagleScript!
var greetings = {"Hello", "Hola", "Bonjour"}

* Display random greeting
say(greetings)

* Set username
var name = "User"
say("Welcome " + name)""")
        
        self.root.bind("<F5>", lambda e: self.run_code())

    def run_code(self):
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        
        interpreter = EagleScriptInterpreter(self.print_to_console)
        interpreter.interpret(self.editor.get(1.0, tk.END))
        
        self.console.config(state='disabled')

    def print_to_console(self, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')

class EagleScriptInterpreter:
    def __init__(self, output_fn):
        self.vars = {}
        self.output = output_fn

    def interpret(self, code):
        for line in code.split('\n'):
            self.execute_line(line)

    def execute_line(self, line):
        line = line.strip()
        if not line or line.startswith('*'):
            return
            
        if match := re.match(r'var\s+(\w+)\s*=\s*(.*)', line):
            var_name = match.group(1)
            expr = match.group(2)
            self.vars[var_name] = self.eval_expression(expr)
            return
            
        if match := re.match(r'say\s*\(\s*(.*?)\s*\)', line):
            arg = match.group(1)
            result = self.eval_expression(arg)
            if isinstance(result, list):
                self.output(random.choice(result))
            else:
                self.output(result)
            return

    def eval_expression(self, expr):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        elif expr.startswith('{') and expr.endswith('}'):
            items = [item.strip().strip('"') for item in expr[1:-1].split(',')]
            return items
        elif '+' in expr:
            parts = expr.split('+')
            return str(self.eval_expression(parts[0])) + str(self.eval_expression(parts[1]))
        else:
            return self.vars.get(expr, expr)

if __name__ == "__main__":
    root = tk.Tk()
    EagleScriptIDE(root)
    root.mainloop()