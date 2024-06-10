# Project Structure

This document provides an overview of the project's directory structure, explaining the purpose of each directory and file.

## Root Directory
The root directory contains the main project files and folders.

<procedure title="Create ResuMate Project Structure" id="create-resumate-structure">
<step>
<ul>
    <li><code>.idea/</code></li>
    <li><code>.venv/</code></li>
    <li>
        <code>app/</code>
        <ul>
            <li><code>__init__.py</code></li>
            <li><code>routes.py</code></li>
        </ul>
    </li>
    <li><code>static/</code></li>
    <li>
        <code>templates/</code>
        <ul>
            <li><code>upload.html</code></li>
        </ul>
    </li>
    <li>
        <code>test/</code>
        <ul>
            <li><code>__init__.py</code></li>
            <li><code>test_app.py</code></li>
        </ul>
    </li>
    <li><code>uploads/</code></li>
    <li>
        <code>Writerside/</code>
        <ul>
            <li><code>images/</code></li>
            <li><code>topics/</code>
                <ul>
                    <li><code>Implementation Details/</code></li>
                    <li><code>Introduction/</code></li>
                    <li><code>Next Steps/</code></li>
                    <li><code>Project Setup/</code></li>
                    <li><code>Testing/</code></li>
                    <li><code>Sprint Review and Retrospective/</code></li>
                </ul>
            </li>
        </ul>
    </li>
    <li><code>config.py</code></li>
    <li><code>requirements.txt</code></li>
    <li><code>run.py</code></li>
</ul>
</step>
</procedure>

## Directory and File Descriptions

### .idea/
Contains IDE-specific settings and project configuration files.

### .venv/
Contains the virtual environment for the project, including installed dependencies.

### app/
The main application directory containing the core Flask application files.

- **__init__.py**: Initializes the Flask application.
- **routes.py**: Contains the routes for handling different web requests.

### static/
Contains static files such as CSS, JavaScript, and images.

### templates/
Contains HTML templates for rendering web pages.

- **upload.html**: Template for the file upload page.

### test/
Contains unit tests for the application.

- **__init__.py**: Initializes the test module.
- **test_app.py**: Contains unit tests for the Flask application.

### uploads/
Directory for storing uploaded files.

### Writerside/
Contains documentation files and images for the Writerside documentation tool.

- **images/**: Contains images used in the documentation.
- **topics/**: Contains markdown files for different documentation topics.
  - **Implementation Details/**: Detailed implementation guides.
  - **Introduction/**: Introduction to the project.
  - **Next Steps/**: Future plans and features.
  - **Project Setup/**: Setup instructions.
  - **Testing/**: Testing guides.
  - **Sprint Review and Retrospective/**: Review and retrospective notes.

### config.py
Configuration file for the Flask application.

### requirements.txt
Lists the project dependencies that need to be installed.

### run.py
Script to run the Flask development server.

## Conclusion
The project structure is organized to separate different concerns, making the project easy to navigate and maintain. Each directory and file has a specific role, contributing to the overall functionality and organization of the project.
