# Routes and Views

This document provides instructions for setting up routes and views in your Flask application.

## Define Routes

Create routes in the `routes.py` file to handle different web requests.

### Example `routes.py`:

<procedure title="Define Routes" id="define routes">
<step>
    <p>Add the following code to your <code>routes.py</code>:</p>
    
    from flask import render_template, request, jsonify, current_app as app
    from .nlp import parse_resume

    @app.route('/')
    def index():
    return render_template('index.html')

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_resume():
    if request.method == 'POST':
    resume_text = request.files['resume'].read().decode('utf-8')
    parsed_resume = parse_resume(resume_text)
    return jsonify(parsed_resume)
    return render_template('upload.html')

    @app.route('/parse_resume', methods=['POST'])
    def parse_resume_route():
    resume_text = request.json.get('resume_text', '')
    parsed_resume = parse_resume(resume_text)
    return jsonify(parsed_resume)

</step>
</procedure>

## Create HTML Templates

Create HTML templates for rendering web pages. These templates should be placed in the `templates` directory.

### Example `index.html`:

<procedure title="Create index.html" id="create-index-html">
<step>
    <p>Create a new file <code>index.html</code> in the <code>templates</code> directory and add the following code:</p>

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResuMate</title>
    </head>
    <body>
        <h1>Welcome to ResuMate</h1>
            <a href="/upload">Upload Resume</a>
        </body>
    </html>
</step>
</procedure>

### Example `upload.html`:

<procedure title="Create upload.html" id="create-upload-html">
<step>
    <p>Create a new file <code>upload.html</code> in the <code>templates</code> directory and add the following code:</p>
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Resume</title>
    </head>
    <body>
        <h1>Upload Your Resume</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="resume">
                <input type="submit" value="Upload">
            </form>
    </body>
    </html>
</step>
</procedure>

## Test Routes and Views

Ensure that your routes and views are working correctly by running the Flask application and visiting the corresponding URLs.

<procedure title="Test Routes and Views" id="test-routes-views">
<step>
    <p>Start the Flask application by running the following command in your terminal or command prompt:</p>
    
        python run.py
    
</step>
<step>
    <p>Visit the following URLs in your web browser to test the routes and views:</p>
    <ul>
        <li><code>http://127.0.0.1:5000/</code> - To view the index page.</li>
        <li><code>http://127.0.0.1:5000/upload</code> - To view the upload resume page.</li>
    </ul>
</step>
</procedure>

## Conclusion

Setting up routes and views in Flask involves defining routes in the `routes.py` file and creating HTML templates for rendering web pages. By following these steps, you can ensure a properly configured and functional web application.
