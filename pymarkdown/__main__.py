"""
Module to provide for "-m pymarkdown" access to the module,
as if it was run from the console.
"""
import pymarkdown

if __name__ == "__main__":
    pymarkdown.PyMarkdownLint().main()
