# myDRE Tools

Tools for managing and interacting with myDRE (my Data Research Environment) workspace.

## Prerequisites

Before installation, ensure you have:

1. Python 3.12.x (Do not use Python 3.13)
   - Using in myDRE [allowlist and configure Python usage](https://support.mydre.org/portal/en/kb/articles/domains-to-be-allowlisted#Python)
   - Download from: https://www.python.org/downloads/release/python-3129/
   - Select the appropriate installer for your system (Windows/macOS/Linux)

2. Visual C++ Redistributable (Windows only):
   - in myDRE Workspace: allowlist aka.ms
   - VC_redist.x64: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - VC_redist.x86: https://aka.ms/vs/17/release/vc_redist.x86.exe
  
3. Using from within myDRE Workspace
   - Allowlist azure-api.net

## What is myDRE?

myDRE (my Data Research Environment) is a secure platform for data sharing and collaboration. These tools help you:

- Create encrypted configuration files for workspace access
- Upload files to a myDRE workspace securely


⚠️ **Important**: These tools only work with myDRE Workspaces. If you don't have a myDRE workspace, please visit [andrea-cloud.com](https://andrea-cloud.com) first.

## Installation Guide

### Option 1: Simple Installation (Recommended for Most Users)

1. Download the latest release from: https://github.com/flow4u/mydre-tools/releases
2. Run the installer for your platform:
   - Windows: Double-click the `.exe` file
   - macOS: Mount the `.dmg` and drag to Applications
   - Linux: Use the provided `.AppImage` file

### Option 2: Installation via pip

Install all components:
```bash
pip install .
```

Or install specific components:
```bash
# For uploading files only:
pip install .[mydre_uploader]

# For configuration encryption only:
pip install .[mydre_config_encrypter]
```

### Option 3: Developer Installation

1. Clone the repository:
```bash
git clone https://github.com/flow4u/mydre-tools.git
cd mydre-tools
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install in development mode:
```bash
pip install -e .
```

## Using the Tools

### myDRE Uploader

1. Launch the uploader:
   ```bash
   mydre-uploader
   ```
   Or use the desktop shortcut/application icon

2. First-time setup:
   - Enter your workspace credentials (get these from your administrator)
   - Select the destination folder
   - Choose files to upload

### myDRE Config Encrypter (Administrators Only)

1. Launch the config encrypter:
   ```bash
   mydre-config-encrypter
   ```
   Or use the desktop shortcut/application icon

2. Follow the wizard to:
   - Set up workspace credentials
   - Generate encrypted configuration files
   - Distribute to team members

## Building from Source

Want to create your own executables? Here's how:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Run the build script:
```bash
python build.py
```

The executables will be created in the `dist` directory:
- Windows: `.exe` files
- macOS: `.app` bundles
- Linux: binary executables

## Troubleshooting

### Common Issues

1. **Installation Fails**
   - Ensure Python 3.12.x is installed
   - On Windows, verify both VC++ redistributables are installed
   - Try running as administrator

2. **Build Errors**
   ```
   Error: could not install packages due to an OSError: [errno 22] invalid argument
   ```
   Solution:
   - Close all command prompts
   - Run as administrator
   - Navigate to project: `cd path\to\mydre-tools`
   - Activate environment: `venv\Scripts\activate`
   - Retry: `python build.py`

3. **Runtime Errors**
   - Check your workspace credentials
   - Verify internet connection
   - Contact your workspace administrator

## Additional Resources

- [Detailed Documentation](docs/README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)

## Support

Need help? 
1. Check the [Troubleshooting Guide](docs/troubleshooting.md)
2. Contact your workspace administrator
3. Visit [andrea-cloud.com/support](https://andrea-cloud.com/support)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
