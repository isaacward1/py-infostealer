# PyGlutton
A guide on the build process, obfuscation techniques, and analysis of simple python-based infostealer malware.<p>
<b>** Disclaimer ** This tutorial is intended for educational purposes only. I do not condone the malicious use of this material.</b>


<br>

## Prerequisites
- Windows 10/11 VM
- Python 3.1X
> pip install -U -R requirements.txt

<br>

## Creating Your Own Malware
[to do later]

<br>

## Malware Analysis

[PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor) - A Python script to extract the contents of a PyInstaller generated Windows 
executable file. The contents of the pyz file (usually pyc files) present inside the 
executable are also extracted and automatically fixed so that a Python bytecode decompiler will recognize it.

[uncompyle6](https://github.com/rocky/python-uncompyle6/) - A cross-version Python bytecode decompiler. Translates Python bytecode back into equivalent Python source code.
