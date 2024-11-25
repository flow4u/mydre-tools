# myDRE Tools

Tools for managing and interacting with myDRE (my Data Research Environment) workspace.

## Components

This repository contains two main tools specifically designed for myDRE Workspaces:
- **myDRE Uploader**: For uploading files to your myDRE workspace
- **myDRE Config Encrypter**: For creating encrypted configuration files required by the myDRE Uploader

## About myDRE

myDRE (my Data Research Environment) is a secure platform for data sharing and collaboration. These tools are specifically designed to work with myDRE Workspaces and cannot be used with other platforms.

## Installation

You can install the components separately or together:

### Install Everything
```bash
pip install .
```

### Install Only the myDRE Uploader
```bash
pip install .[mydre_uploader]
```

### Install Only the myDRE Config Encrypter
```bash
pip install .[mydre_config_encrypter]
```

### Install from Source (Development)
1. Clone the repository:
   ```bash
   git clone https://github.com/flow4u/mydre-tools.git
   cd mydre-tools
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the desired components:
   ```bash
   # For everything:
   pip install -e .

   # For only the myDRE Uploader:
   pip install -e ".[mydre_uploader]"

   # For only the myDRE Config Encrypter:
   pip install -e ".[mydre_config_encrypter]"
   ```

## Usage

### myDRE Uploader
The myDRE Uploader is used to securely upload files to your myDRE workspace:
```bash
mydre-uploader
```

### myDRE Config Encrypter
The myDRE Config Encrypter is used by workspace administrators to create encrypted configuration files:
```bash
mydre-config-encrypter
```

## Building Executables

You can create standalone executables using the provided build script:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

This will create two executables in the `dist` directory:
- `mydre-uploader` - The file upload tool
- `mydre-config-encrypter` - The configuration encryption tool

The executables will be created according to your platform:
- Windows: Creates `.exe` files
- macOS: Creates `.app` bundles (with proper windowing support)
- Linux: Creates binary executables

The build script automatically:
- Includes all necessary modules and dependencies
- Adds the favicon.ico to the executables
- Creates standalone executables that don't require Python installation
- Handles platform-specific requirements (like windowed mode for macOS)

Note: The old PyInstaller commands in the README are no longer needed as the build script handles everything automatically.

## Important Note

These tools are specifically designed for use with myDRE Workspaces. They require proper authentication and configuration from your myDRE workspace administrator. If you don't have a myDRE workspace, these tools will not be useful for you.

For more information about myDRE Workspaces, visit [andrea-cloud.com](https://andrea-cloud.com).

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

# Troubleshooting

## Build Process Errors

If you encounter an error during the build process like:
```
Error: could not install packages due to an OSError: [errno 22] invalid argument
```

Try these steps:
1. Close the Command Prompt completely
2. Open Command Prompt as Administrator (Right-click -> Run as administrator)
3. Navigate to your project directory:
   ```batch
   cd path\to\mydre-tools
   ```
4. Activate the virtual environment:
   ```batch
   venv\Scripts\activate
   ```
5. Run the build process again:
   ```batch
   python build.py
   ```

This often resolves temporary path or lock file issues that can occur during the build process. Running as administrator can help resolve permission-related issues.
