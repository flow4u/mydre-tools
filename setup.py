from setuptools import setup, find_packages
import os

def read_requirements(filename):
    with open(os.path.join("requirements", filename), "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("-r")]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mydre-tools",
    version="0.5",
    author="Stefan van Aalst",
    description="Tools for myDRE (my Data Research Environment) workspace management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mydre-tools",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        'cryptography>=35.0.0',
        'Pillow>=8.0.0',
        'requests>=2.25.0',
        'azure-storage-blob>=12.0.0',
        'tk>=0.1.0',
    ],
    extras_require={
        'mydre_uploader': read_requirements("mydre_uploader.txt"),
        'mydre_config_encrypter': read_requirements("mydre_config_encrypter.txt"),
        'all': read_requirements("mydre_uploader.txt") + read_requirements("mydre_config_encrypter.txt")
    },
    entry_points={
        'console_scripts': [
            'mydre-uploader=mydre_uploader.gui:main',
            'mydre-config-encrypter=mydre_config_encrypter.gui:main',
        ],
    },
    package_data={
        'mydre_tools': ['assets/*'],
        'mydre_uploader': ['../assets/*'],
        'mydre_config_encrypter': ['../assets/*'],
    },
) 