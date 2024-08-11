# Dependencies Installation

This document provides instructions for installing and managing the project dependencies for ResuMate.

## Setting Up the Virtual Environment

First, ensure you have set up the virtual environment as described in the Environment Setup section. If not, follow these steps:

<procedure title="Set Up Virtual Environment" id="setup-virtual-environment">
    <step>
        <p>Open your terminal or command prompt and navigate to the root directory of your project.</p>
    </step>
    <step>
        <p>Create a virtual environment by running the following command:</p>
        <ul>
            <li>
                <code>python -m venv .venv</code>
            </li>
        </ul>
    </step>
    <step>
        <p>Activate the virtual environment:</p>
        <ul>
            <li>
                <strong>Windows:</strong>
                <ul>
                    <li><code>.\.venv\Scripts\Activate.ps1</code></li>
                </ul>
            </li>
            <li>
                <strong>macOS/Linux:</strong>
                <ul>
                    <li><code>source .venv/bin/activate</code></li>
                </ul>
            </li>
        </ul>
    </step>
</procedure>

## Installing Dependencies

With the virtual environment activated, you can install the project dependencies.

<procedure title="Install Dependencies" id="install-dependencies">
    <step>
        <p>Ensure you have a <code>requirements.txt</code> file in your project root directory. If not, create one and add the required dependencies.</p>
    </step>
    <step>
        <p>Install the dependencies using the following command:</p>
        <ul>
            <li>
                <code>pip install -r requirements.txt</code>
            </li>
        </ul>
    </step>
</procedure>

## Managing Dependencies

To manage dependencies effectively, follow these guidelines:

### Adding New Dependencies

<procedure title="Add New Dependencies" id="add-new-dependencies">
    <step>
        <p>When you need to add a new package to your project, use the following command:</p>
        <ul>
            <li>
                <code>pip install &lt;package_name&gt;</code>
            </li>
        </ul>
    </step>
    <step>
        <p>After installing the new package, update the <code>requirements.txt</code> file:</p>
        <ul>
            <li>
                <code>pip freeze &gt; requirements.txt</code>
            </li>
        </ul>
    </step>
</procedure>

### Updating Dependencies

<procedure title="Update Dependencies" id="update-dependencies">
    <step>
        <p>To update a specific package, use the following command:</p>
        <ul>
            <li>
                <code>pip install --upgrade &lt;package_name&gt;</code>
            </li>
        </ul>
    </step>
    <step>
        <p>After updating, remember to update the <code>requirements.txt</code> file:</p>
        <ul>
            <li>
                <code>pip freeze &gt; requirements.txt</code>
            </li>
        </ul>
    </step>
</procedure>

### Removing Dependencies

<procedure title="Remove Dependencies" id="remove-dependencies">
    <step>
        <p>If you need to remove a package, use the following command:</p>
        <ul>
            <li>
                <code>pip uninstall &lt;package_name&gt;</code>
            </li>
        </ul>
    </step>
    <step>
        <p>After removing the package, update the <code>requirements.txt</code> file:</p>
        <ul>
            <li>
                <code>pip freeze &gt; requirements.txt</code>
            </li>
        </ul>
    </step>
</procedure>

## Checking Dependency Versions

<procedure title="Check Dependency Versions" id="check-dependency-versions">
    <step>
        <p>To check the installed versions of all dependencies, use the following command:</p>
        <ul>
            <li>
                <code>pip list</code>
            </li>
        </ul>
    </step>
</procedure>

## New Dependencies for User Authentication

To set up user authentication, we added the following dependencies:

- `Flask-Login`: For user session management.
- `Flask-Bcrypt`: For hashing passwords.

### Installing New Dependencies

<procedure title="Install New Dependencies" id="install-new-dependencies">
    <step>
        <p>To install the new dependencies, use the following command:</p>
        <ul>
            <li>
                <code>pip install flask-login flask-bcrypt</code>
            </li>
        </ul>
    </step>
    <step>
        <p>After installing the new packages, update the <code>requirements.txt</code> file:</p>
        <ul>
            <li>
                <code>pip freeze &gt; requirements.txt</code>
            </li>
        </ul>
    </step>
</procedure>

## Common Issues and Troubleshooting

### Issue: Package Installation Error

<procedure title="Resolve Package Installation Error" id="resolve-package-installation-error">
    <step>
        <p>If you encounter an error during package installation, try the following steps:</p>
        <ul>
            <li>Ensure your virtual environment is activated.</li>
            <li>Verify the package name and version.</li>
            <li>Check your internet connection.</li>
            <li>If the issue persists, consult the package documentation or community forums.</li>
        </ul>
    </step>
</procedure>

### Issue: Dependency Conflicts

<procedure title="Resolve Dependency Conflicts" id="resolve-dependency-conflicts">
    <step>
        <p>If there are conflicts between package versions, consider using a tool like <code>pip-tools</code> to manage dependencies and resolve conflicts:</p>
        <ul>
            <li><code>pip install pip-tools</code></li>
            <li><code>pip-compile</code></li>
        </ul>
    </step>
</procedure>

## Conclusion

Managing project dependencies is crucial for maintaining a stable and functional development environment.
By following these guidelines, you can ensure that all necessary packages are installed and up to date,
making it easier to collaborate and develop the ResuMate project.
