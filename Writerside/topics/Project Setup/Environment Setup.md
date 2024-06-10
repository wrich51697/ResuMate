# Environment Setup

## Install Python
Ensure Python is installed on your system. Download it from the [official website](https://www.python.org/downloads/) if needed.

## Set Up a Virtual Environment
Create a virtual environment to manage project dependencies separately from the global Python environment.

### Command to create a virtual environment:

python -m venv .venv

### Command to activate the virtual environment:

- **Windows**:
  `.\.venv\Scripts\Activate.ps1`

- **MacOS/Linux**:
  `source .venv/bin/activate`

## Verify the Virtual Environment
After activation, your command prompt or terminal should indicate that you are working within the virtual environment 
(usually by showing the name of the virtual environment before the prompt).

## Install Project Dependencies
With the virtual environment activated, install the necessary project dependencies. Ensure you have a `requirements.txt` 
file in your project root directory. Install the dependencies using the following command:
`pip install -r requirements.txt`

## Additional Tools

### Install Git
Ensure Git is installed for version control. You can download it from the [official Git website](https://git-scm.com/).
Verify the installation by running: `git --version`

### Set Up Your IDE
Use an Integrated Development Environment (IDE) like PyCharm or Visual Studio Code for a more efficient development workflow. 
Here are basic steps for setting up PyCharm:

- **Install PyCharm**: Download and install PyCharm from the [JetBrains website](https://www.jetbrains.com/pycharm/download/).
- **Open the Project**: Open PyCharm and select "Open" to navigate to your project directory.
- **Configure the Python Interpreter**: Go to `File > Settings > Project: [Your Project] > Python Interpreter` 
- and select the interpreter from your `.venv` directory.

## Final Check
Ensure all setups are complete by running the Flask development server. Navigate to your project directory and run:
`python run.py`

Visit `http://127.0.0.1:5000/` in your web browser to check if the application is running correctly.









