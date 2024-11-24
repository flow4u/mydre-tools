#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI implementation for myDRE Uploader.

This tool is specifically designed for use with myDRE (my Data Research Environment) 
workspaces and cannot be used with other platforms.
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import json
from datetime import datetime
import sys
import webbrowser

# Handle both package import and direct script execution
try:
    from .uploader import Upload, derive_key, decrypt_data
except ImportError:
    from uploader import Upload, derive_key, decrypt_data

REQUIRED_KEYS = [
    "WORKSPACE_NAME",
    "WORKSPACE_DESCRIPTION",
    "WORKSPACE_KEY",
    "SUBSCRIPTION_KEY",
    "USER_NAME"
]

class UploadForm:
    def __init__(self, master):
        self.master = master
        self.keys_data = None
        master.title("Upload Data to myDRE Workspace")
        master.geometry("800x650")
        master.configure(bg='#f0f0f0')

        # Set the icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'favicon.ico')
        if os.path.exists(icon_path):
            master.iconbitmap(icon_path)

        # Initialize GUI components
        self.init_gui()

    def init_gui(self):
        """Initialize all GUI components."""
        # Set default font
        default_font = ('Helvetica', 9)
        self.master.option_add("*Font", default_font)
        self.master.option_add("*Background", '#f0f0f0')
        
        # Main container
        main_container = tk.Frame(self.master, bg='#f0f0f0')
        main_container.pack(padx=15, pady=10, fill='both')

        # Config section
        config_section = tk.LabelFrame(main_container, text="Configuration", bg='#f0f0f0', padx=10, pady=5)
        config_section.pack(fill='x', pady=(0, 10))
        
        self.config_button = tk.Button(config_section, text="SELECT CONFIG FILE", 
                                     command=self.select_config,
                                     bg='#007bff', fg='white',
                                     padx=20, pady=5)
        self.config_button.pack(side=tk.LEFT)
        self.config_label = tk.Label(config_section, text="No config file selected")
        self.config_label.pack(side=tk.LEFT, padx=10)

        # PIN section
        pin_section = tk.LabelFrame(main_container, text="Authentication", bg='#f0f0f0', padx=10, pady=10)
        pin_section.pack(fill='x', pady=(0, 10))
        
        self.pin_label = tk.Label(pin_section, text="Enter PIN:")
        self.pin_label.pack(side=tk.LEFT)
        self.pin_entry = tk.Entry(pin_section, show="*", state=tk.DISABLED, width=20)
        self.pin_entry.pack(side=tk.LEFT, padx=10)

        # Workspace info section
        workspace_section = tk.LabelFrame(main_container, text="Workspace Information", bg='#f0f0f0', padx=10, pady=10)
        workspace_section.pack(fill='x', pady=(0, 10))
        
        self.logo_label = tk.Label(workspace_section, 
                                 text="Please select config file", 
                                 font=('Helvetica', 11, 'bold'))
        self.logo_label.pack(pady=(0, 10))
        
        # Description frame
        self.description_frame = tk.Frame(workspace_section, bg='#f0f0f0')
        self.description_frame.pack(fill='x', pady=5)
        self.description_header = tk.Label(self.description_frame, 
                                         text="Workspace Description:", 
                                         font=('Helvetica', 9, 'bold'))
        self.description_header.pack(anchor='w')
        self.description_label = tk.Label(self.description_frame, text="", wraplength=700)
        self.description_label.pack(anchor='w', padx=20)
        
        # Uploader frame
        self.uploader_frame = tk.Frame(workspace_section, bg='#f0f0f0')
        self.uploader_frame.pack(fill='x', pady=5)
        self.uploader_header = tk.Label(self.uploader_frame, 
                                      text="Name Uploader:", 
                                      font=('Helvetica', 9, 'bold'))
        self.uploader_header.pack(anchor='w')
        self.uploader_label = tk.Label(self.uploader_frame, text="")
        self.uploader_label.pack(anchor='w', padx=20)

        # File selection section
        file_section = tk.LabelFrame(main_container, text="File Selection", bg='#f0f0f0', padx=10, pady=10)
        file_section.pack(fill='x', pady=(0, 10))
        
        self.file_button = tk.Button(file_section, text="Select Files", 
                                   command=self.select_files, 
                                   state=tk.DISABLED,
                                   bg='#28a745', fg='white',
                                   padx=20, pady=5)
        self.file_button.pack(side=tk.LEFT)
        self.file_label = tk.Label(file_section, text="No files selected")
        self.file_label.pack(side=tk.LEFT, padx=10)

        # Files list section
        self.files_listbox = tk.Listbox(main_container, width=50, height=3,
                                      relief='solid', borderwidth=1)
        self.files_listbox.pack(pady=(0, 10), fill='x')

        # Bottom container for confirmation, buttons, and powered by
        bottom_container = tk.Frame(main_container, bg='#f0f0f0')
        bottom_container.pack(fill='x', side=tk.BOTTOM, pady=10)

        # Confirmation section
        confirm_section = tk.Frame(bottom_container, bg='#f0f0f0')
        confirm_section.pack(fill='x', pady=(0, 10))
        
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(confirm_section, 
                                     text="I confirm that I am authorized to upload this data", 
                                     variable=self.checkbox_var, 
                                     command=self.toggle_upload_button,
                                     state=tk.DISABLED)
        self.checkbox.pack()

        # Buttons section
        button_section = tk.Frame(bottom_container, bg='#f0f0f0')
        button_section.pack(fill='x', pady=(0, 10))
        
        self.upload_button = tk.Button(button_section, text="Upload", 
                                     state=tk.DISABLED, 
                                     command=self.uploading,
                                     bg='#28a745', fg='white',
                                     padx=30, pady=5)
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        self.close_button = tk.Button(button_section, text="Close", 
                                    command=self.close_application,
                                    bg='#dc3545', fg='white',
                                    padx=30, pady=5)
        self.close_button.pack(side=tk.LEFT, padx=5)

        # Footer frame
        footer_frame = tk.Frame(bottom_container, bg='#f0f0f0')
        footer_frame.pack(fill='x', pady=(10, 0))

        # Version label
        version_label = tk.Label(footer_frame, text="Version: 0.5",
                               font=("Helvetica", 8), bg='#f0f0f0')
        version_label.pack(side=tk.LEFT)

        # Powered by section
        powered_label = tk.Label(footer_frame, text="Powered by ",
                               font=("Helvetica", 8), bg='#f0f0f0')
        powered_label.pack(side=tk.RIGHT)

        powered_link = tk.Label(footer_frame, text="andrea-cloud.com",
                              font=("Helvetica", 8, "bold"), fg="#007bff",
                              cursor="hand2", bg='#f0f0f0')
        powered_link.pack(side=tk.RIGHT)
        powered_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://andrea-cloud.com"))

        self.selected_files = []

    def select_config(self):
        """Handle configuration file selection."""
        try:
            file_path = filedialog.askopenfilename(
                title="Select configuration file",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:  # User cancelled the file selection
                return
                
            with open(file_path, "r") as f:
                self.keys_data = json.load(f)
                
            # Validate all required keys are present
            missing_keys = [key for key in REQUIRED_KEYS if key not in self.keys_data]
            if missing_keys:
                raise KeyError(f"Missing required keys in configuration file: {', '.join(missing_keys)}")
            
            # Show the filename instead of generic message
            config_filename = os.path.basename(file_path)
            self.config_label.config(text=config_filename)
            
            ws_name = self.keys_data["WORKSPACE_NAME"]
            self.logo_label.config(text=f"Upload to Workspace {ws_name}")
            self.description_label.config(text="Enter PIN to see workspace description")
            self.uploader_label.config(text="Enter PIN to see uploader name")
            self.checkbox.config(text=f"I confirm that I am authorized\nto upload this data to {ws_name}")
            
            # Enable controls after successful config load
            self.pin_entry.config(state=tk.NORMAL)
            self.file_button.config(state=tk.NORMAL)
            self.checkbox.config(state=tk.NORMAL)
            
            # Bind the PIN entry to update description when PIN is entered
            self.pin_entry.bind('<KeyRelease>', self.update_description)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config file: {str(e)}")

    def update_description(self, event=None):
        """Update the workspace description and uploader name when PIN is entered."""
        pin = self.pin_entry.get()
        if pin and self.keys_data:
            try:
                decryption_key = derive_key(pin)
                ws_description = decrypt_data(self.keys_data["WORKSPACE_DESCRIPTION"], decryption_key)
                user_name = decrypt_data(self.keys_data["USER_NAME"], decryption_key)
                self.description_label.config(text=ws_description)
                self.uploader_label.config(text=user_name)
            except Exception:
                # If decryption fails (wrong PIN), show generic message
                self.description_label.config(text="Enter correct PIN to see workspace description")
                self.uploader_label.config(text="Enter correct PIN to see uploader name")

    def select_files(self):
        """Handle file selection."""
        self.selected_files = filedialog.askopenfilenames()
        if self.selected_files:
            self.file_label.config(text=f"{len(self.selected_files)} file(s) selected")
            self.update_files_listbox()
            self.checkbox.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="No files selected")
            self.checkbox.config(state=tk.DISABLED)
            self.upload_button.config(state=tk.DISABLED)
        self.toggle_upload_button()

    def update_files_listbox(self):
        """Update the listbox with selected files."""
        self.files_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.files_listbox.insert(tk.END, os.path.basename(file))

    def toggle_upload_button(self):
        """Enable/disable upload button based on conditions."""
        if self.selected_files and self.checkbox_var.get() and self.pin_entry.get():
            self.upload_button.config(state=tk.NORMAL)
        else:
            self.upload_button.config(state=tk.DISABLED)

    def uploading(self):
        """Handle the file upload process."""
        pin = self.pin_entry.get()
        if not pin:
            messagebox.showerror("Error", "Please enter a PIN")
            return

        try:
            ws_name = self.keys_data["WORKSPACE_NAME"]
            decryption_key = derive_key(pin)
            ws_description = decrypt_data(self.keys_data["WORKSPACE_DESCRIPTION"], decryption_key)
            ws_key = decrypt_data(self.keys_data["WORKSPACE_KEY"], decryption_key)
            tenant_key = decrypt_data(self.keys_data["SUBSCRIPTION_KEY"], decryption_key)
            user_name = decrypt_data(self.keys_data["USER_NAME"], decryption_key)

            # Sanitize user_name for filename
            sanitized_user_name = self.sanitize_filename(user_name)

            # Create progress window
            progress_window = tk.Toplevel(self.master)
            progress_window.title("Upload Progress")
            progress_window.geometry("300x150")

            label = tk.Label(progress_window, text="Uploading files...")
            label.pack(pady=10)

            progress_bar = ttk.Progressbar(progress_window, length=200, mode='determinate')
            progress_bar.pack(pady=10)

            file_label = tk.Label(progress_window, text="")
            file_label.pack(pady=5)

            uploader = Upload(ws_name, ws_description, ws_key, tenant_key, user_name)
            uploader.create_workspace_container()

            # Create and upload the user name file
            user_file_path = f"{sanitized_user_name}.txt"
            with open(user_file_path, "w") as f:
                # Write the uploader information and upload timestamp
                upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Uploaded by: {user_name}\n")
                f.write(f"Uploaded on: {upload_time}\n\n")
                f.write("List of all the uploaded files:\n")

            # Calculate total files including the user name file
            total_files = len(self.selected_files) + 1
            
            # Upload user name file first
            progress = (1 / total_files) * 100
            progress_bar['value'] = progress
            file_label.config(text=f"Uploading: {user_file_path}")
            self.master.update_idletasks()
            uploader.file2(user_file_path)
            
            # Upload selected files
            for i, file in enumerate(self.selected_files, start=2):
                progress = (i / total_files) * 100
                progress_bar['value'] = progress
                file_label.config(text=f"Uploading: {os.path.basename(file)}")
                self.master.update_idletasks()

                uploader.file2(file)

                # Append the uploaded file name to the user file
                with open(user_file_path, "a") as f:
                    f.write(f"{os.path.basename(file)}\n")

            uploader.commit_workspace_container()

            # Clean up the temporary user name file
            os.remove(user_file_path)

            progress_bar['value'] = 100
            file_label.config(text="Upload complete!")
            self.master.update_idletasks()

            messagebox.showinfo("Upload Complete", f"All files have been uploaded successfully to {ws_name}!")

            progress_window.destroy()
            
            # Reset UI elements
            self.files_listbox.delete(0, tk.END)
            self.selected_files = []
            self.file_label.config(text="No files selected")
            self.checkbox.config(state=tk.DISABLED)
            self.upload_button.config(state=tk.DISABLED)
            self.checkbox_var.set(False)
            self.pin_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred, probably wrong PIN: {str(e)}")

    def sanitize_filename(self, name):
        """Sanitize the user name to create a valid filename."""
        # Replace invalid characters with underscores
        return ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in name)

    def close_application(self):
        """Close the application."""
        self.master.quit()
        self.master.destroy()
        sys.exit()

if __name__ == "__main__":
    # For development/testing in Spyder or direct execution
    import sys
    import os
    
    # Add the parent directory to Python path if running directly
    if os.path.dirname(__file__) not in sys.path:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    
    root = tk.Tk()
    app = UploadForm(root)
    root.mainloop()