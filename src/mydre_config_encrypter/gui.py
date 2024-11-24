#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI implementation for myDRE Config Encrypter.
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import webbrowser

# Handle both package import and direct script execution
try:
    from .encrypter import ConfigEncrypter
except ImportError:
    from encrypter import ConfigEncrypter

PADDING = 10
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2196F3"
WARNING_COLOR = "#ff5722"
DISABLED_BG = "#e0e0e0"

class EncrypterForm:
    def __init__(self, master):
        self.master = master
        self.encrypter = ConfigEncrypter()  # Create instance of ConfigEncrypter
        master.title("myDRE - Config Encrypter")
        master.configure(bg=BG_COLOR)
        master.resizable(False, False)

        # Center the window
        window_width = 500
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Set the icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'favicon.ico')
        if os.path.exists(icon_path):
            master.iconbitmap(icon_path)

        self.init_gui()

    def init_gui(self):
        """Initialize GUI components."""
        # Main frame
        main_frame = tk.Frame(self.master, bg=BG_COLOR)
        main_frame.pack(padx=PADDING, pady=PADDING, fill='both', expand=True)

        # Warning section
        warning_frame = tk.Frame(main_frame, bg=BG_COLOR)
        warning_frame.pack(fill='x', pady=(0, PADDING))

        warning_text = "⚠️ Warning: Anybody with the PIN and keys.json can upload data to my Workspace."
        warning_label = tk.Label(warning_frame, text=warning_text, wraplength=400,
                               justify="left", fg=WARNING_COLOR, bg=BG_COLOR,
                               font=('Helvetica', 10, 'bold'))
        warning_label.pack(pady=PADDING)

        self.checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(warning_frame, text="I understand and accept",
                                variable=self.checkbox_var, command=self._toggle_fields,
                                bg=BG_COLOR, font=('Helvetica', 9))
        checkbox.pack(pady=(0, PADDING))

        # Entries section
        entries_frame = tk.Frame(main_frame, bg=BG_COLOR)
        entries_frame.pack(fill='x', pady=PADDING)

        # Create entry widgets
        self.pin_entry = tk.Entry(entries_frame, show="*", state=tk.DISABLED)
        self.name_entry = tk.Entry(entries_frame, state=tk.DISABLED)
        self.description_entry = tk.Entry(entries_frame, state=tk.DISABLED)
        self.key1_entry = tk.Entry(entries_frame, state=tk.DISABLED)
        self.key2_entry = tk.Entry(entries_frame, state=tk.DISABLED)
        self.user_entry = tk.Entry(entries_frame, state=tk.DISABLED)
        self.filename_entry = tk.Entry(entries_frame, state=tk.DISABLED)

        # Configure fields
        fields = [
            ("PIN:", "Enter a PIN of at least 6 characters", self.pin_entry),
            ("WORKSPACE NAME:", "Enter your workspace name", self.name_entry),
            ("WORKSPACE DESCRIPTION:", "Enter a description for your workspace", self.description_entry),
            ("WORKSPACE KEY:", "Enter your workspace key", self.key1_entry),
            ("SUBSCRIPTION KEY:", "Enter your subscription key", self.key2_entry),
            ("USER NAME:", "Enter name of the uploader", self.user_entry),
            ("FILENAME:", "Enter name of json config file (without .json extension)", self.filename_entry)
        ]

        for row, (label_text, tooltip_text, entry_widget) in enumerate(fields):
            label = tk.Label(entries_frame, text=label_text, bg=BG_COLOR, font=('Helvetica', 9))
            label.grid(row=row, column=0, sticky="e", padx=(0, PADDING), pady=5)
            
            entry_widget.configure(width=40, font=('Helvetica', 9))
            entry_widget.grid(row=row, column=1, sticky="w", pady=5)
            self._create_tooltip(entry_widget, tooltip_text)

        # Buttons section
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.pack(pady=PADDING*2)

        button_style = {
            'font': ('Helvetica', 9),
            'width': 15,
            'borderwidth': 0,
            'pady': 8,
            'cursor': 'hand2'
        }

        self.save_button = tk.Button(button_frame, text="Save Keys", command=self._save_keys,
                                   state=tk.DISABLED, bg=PRIMARY_COLOR, fg='white',
                                   activebackground='#1976D2', activeforeground='white',
                                   **button_style)
        self.save_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="Close", command=self._close_application,
                               bg='#e0e0e0', activebackground='#bdbdbd',
                               **button_style)
        close_button.pack(side=tk.LEFT, padx=5)

        # Footer section
        footer_frame = tk.Frame(main_frame, bg=BG_COLOR)
        footer_frame.pack(side=tk.BOTTOM, fill='x', pady=PADDING)

        # Version label
        version_label = tk.Label(footer_frame, text="Version: 0.5",
                               font=("Helvetica", 8), bg=BG_COLOR)
        version_label.pack(side=tk.LEFT)

        # Powered by section
        powered_label = tk.Label(footer_frame, text="Powered by ",
                               font=("Helvetica", 8), bg=BG_COLOR)
        powered_label.pack(side=tk.RIGHT)

        powered_link = tk.Label(footer_frame, text="andrea-cloud.com",
                              font=("Helvetica", 8, "bold"), fg=PRIMARY_COLOR,
                              cursor="hand2", bg=BG_COLOR)
        powered_link.pack(side=tk.RIGHT)
        powered_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://andrea-cloud.com"))

    def _toggle_fields(self):
        """Toggle the state of input fields based on checkbox."""
        state = tk.NORMAL if self.checkbox_var.get() else tk.DISABLED
        for widget in (self.pin_entry, self.name_entry, self.description_entry,
                      self.key1_entry, self.key2_entry, self.user_entry,
                      self.filename_entry, self.save_button):
            widget.config(state=state)

    def _save_keys(self):
        """Save the encrypted configuration file."""
        try:
            # Save the config directly using the ConfigEncrypter instance
            self.encrypter.save_config(
                pin=self.pin_entry.get(),
                ws_name=self.name_entry.get(),
                ws_description=self.description_entry.get(),
                ws_key=self.key1_entry.get(),
                tenant_key=self.key2_entry.get(),
                user_name=self.user_entry.get(),
                filename=self.filename_entry.get()
            )
            messagebox.showinfo("Success", f"Keys saved successfully to {self.filename_entry.get()}")
            
        except (ValueError, IOError) as e:
            messagebox.showerror("Error", str(e))

    def _close_application(self):
        """Close the application."""
        self.master.quit()
        self.master.destroy()
        sys.exit()

    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, justify='left',
                           background="#ffffe0", relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.after(2000, hide_tooltip)
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

def main():
    root = tk.Tk()
    app = EncrypterForm(root)
    root.mainloop()

if __name__ == "__main__":
    # For development/testing in Spyder or direct execution
    import sys
    import os
    
    # Add the parent directory to Python path if running directly
    if os.path.dirname(__file__) not in sys.path:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    
    root = tk.Tk()
    app = EncrypterForm(root)
    root.mainloop()