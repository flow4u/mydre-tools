#!/usr/bin/env python3
"""
Main entry point for myDRE Config Encrypter
"""

import tkinter as tk
import sys
import os

# Add the parent directory to Python path if running directly
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mydre_config_encrypter.gui import EncrypterForm

def main():
    root = tk.Tk()
    app = EncrypterForm(root)
    root.mainloop()

if __name__ == "__main__":
    main() 