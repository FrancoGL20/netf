# Desktop Application

A scalable desktop application built with PySide6.

## Requirements

- Python 3.8+
- PySide6

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the application using the command line

1. Navigate to the project directory
2. Run the following command:

   Windows:
   ```bash
   python .\main.py
   ```

   Linux/Mac:
   ```bash
   python3 main.py
   ```

## Compile the application to an executable

<!-- ### Windows
1. Install Visual Studio
2. In visual Studio install the following components:
   - Compiling tools for C++ (x64/x86)
   - Windows SDK (10 or 11 latest version) 
   - Clang compiler (optional)
3. Open the command line and navigate to the project directory
4. Create the pysidedeplosy.spec file with the following content:
   ```spec
   title = NetF
   extra_args = --msvc=latest --enable-plugin=pyside6 --windows-console-mode=disable
   ```
5. Run the following command to compile the application:
   ```bash
   pyside6-deploy .\main.py
   ``` -->

### Windows

1. Navigate to the project directory
2. Run the following command:
   ```bash
   pyinstaller --noconfirm --clean NetF.spec
   ```

## Project Structure

The application is organized in a modular way to facilitate maintenance and scalability:

- `src/`: Contains all source code
  - `config/`: Application configurations
  - `ui/`: User interfaces and widgets
  - `controllers/`: Business logic
  - `utils/`: General utilities
- `assets/`: Static resources
- `tests/`: Test files