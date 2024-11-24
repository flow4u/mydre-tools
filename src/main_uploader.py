#!/usr/bin/env python3
"""
Main entry point for myDRE Uploader
"""

import tkinter as tk
import sys
import os

# Add the parent directory to Python path if running directly
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mydre_uploader.gui import UploadForm

def main():
    root = tk.Tk()
    app = UploadForm(root)
    root.mainloop()

if __name__ == "__main__":
    main() 