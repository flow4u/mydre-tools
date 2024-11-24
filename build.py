#!/usr/bin/env python3
import os
import platform
import subprocess
import sys

def check_dependencies():
    """Check and install required dependencies."""
    required_packages = [
        'pyinstaller',
        'cryptography',
        'Pillow',
        'requests',
        'azure-storage-blob',
        'requests'
    ]
    
    print("Checking dependencies...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}: {e}")
                return False
    return True

def build_executables():
    """Build executables for the current platform."""
    
    # Check dependencies first
    if not check_dependencies():
        print("Error: Required dependencies could not be installed.")
        return False

    # Ensure python is used to run pyinstaller
    pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
    
    # Platform-specific path separator
    sep = ';' if platform.system() == 'Windows' else ':'
    
    # Common PyInstaller options
    base_options = [
        '--noconsole',
        '--onefile',
        f'--icon=assets{os.sep}favicon.ico',
        '--clean',
        f'--add-data=assets{os.sep}favicon.ico{sep}assets',  # Fixed syntax
        '--collect-submodules=mydre_uploader',  # Include all submodules
        '--collect-submodules=mydre_config_encrypter',  # Include all submodules
        '--hidden-import=cryptography',  # Explicitly include cryptography
        '--hidden-import=azure.storage.blob',  # Explicitly include azure storage
        '--hidden-import=requests'
    ]
    
    # Platform-specific options
    if platform.system() == 'Darwin':  # macOS
        base_options.append('--windowed')
    
    try:
        # Build myDRE Uploader
        print("Building myDRE Uploader...")
        uploader_options = [
            *pyinstaller_cmd,
            *base_options,
            '--name', 'mydre-uploader',
            '--paths', 'src',  # Add source directory to Python path
            'src/main_uploader.py'  # Use main entry point
        ]
        subprocess.run(uploader_options, check=True)
        
        # Build myDRE Config Encrypter
        print("Building myDRE Config Encrypter...")
        encrypter_options = [
            *pyinstaller_cmd,
            *base_options,
            '--name', 'mydre-config-encrypter',
            '--paths', 'src',  # Add source directory to Python path
            'src/main_encrypter.py'  # Use main entry point
        ]
        subprocess.run(encrypter_options, check=True)
        
        print("Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def ensure_assets():
    """Ensure assets are in the correct location for both development and build."""
    if not os.path.exists('assets'):
        os.makedirs('assets')
    if not os.path.exists('assets/favicon.ico'):
        # Look for favicon.ico in source directories
        possible_locations = [
            'favicon.ico',
            'src/favicon.ico',
            'src/mydre_uploader/favicon.ico',
            'src/mydre_config_encrypter/favicon.ico',
        ]
        for loc in possible_locations:
            if os.path.exists(loc):
                import shutil
                shutil.copy(loc, 'assets/favicon.ico')
                break

if __name__ == "__main__":
    ensure_assets()
    if build_executables():
        print("\nExecutables created successfully in the 'dist' directory.")
    else:
        print("\nBuild process failed. Please check the error messages above.") 