#  Résumé Parsing with SpaCy

This document provides instructions for setting up  Résumé parsing using SpaCy in your Flask application.

## Install SpaCy and Language Model
First, ensure SpaCy and the necessary language model are installed in your virtual environment.

<procedure title="Install SpaCy and Language Model" id="install-spacy">
    <step>
        <p>Open your terminal or command prompt.</p>
    </step>
    <step>
        <p>Run the following command to install SpaCy:</p>
    </step>

        pip install spacy

<p>Download the English language model:</p>

    python -m spacy download en_core_web_sm

</procedure>

## Initialize SpaCy in Your Application
Set up SpaCy in your Flask application by initializing it in a new file, such as `nlp.py`, in the `app` directory.

### Example `nlp.py`:

<procedure title="Initialize SpaCy" id="initialize-spacy">
    <step>
        <p>Create a new file <code>nlp.py</code> in the <code>app</code> directory and add the following code:</p>

                import spacy      

<step><p>Load the pre-trained SpaCy model</p></step>

    nlp = spacy.load('en_core_web_sm')
</step>
</procedure>

## Create  Résumé Parsing Function

Define a function to parse Résumés using SpaCy in the `nlp.py` file.

### Example  Résumé Parsing Function:

<procedure title="Create  Résumé Parsing Function" id="create-parsing-function">
<step>
    <p>Add the following code to your <code>nlp.py</code>:</p>

    from collections import defaultdict

    def parse_ Résumé( Résumé_text):
    doc = nlp( Résumé_text)
    parsed_ Résumé = defaultdict(str)

    # Extracting entities
    for ent in doc.ents:
        parsed_ Résumé[ent.label_] += ent.text + ' '
    
    return parsed_ Résumé

</step>
</procedure>

## Integrate Résumé Parsing with Flask

Update your `routes.py` file to include a route for parsing  Résumés.

### Example `routes.py`:

<procedure title="Integrate  Résumé Parsing with Flask" id="integrate-parsing">
<step>
    <p>Add the following code to your <code>routes.py</code>:</p>

    from flask import request, jsonify
    from .nlp import parse_ Résumé

    @app.route('/parse_ Résumé', methods=['POST'])
    def parse_ Résumé_route():
     Résumé_text = request.json.get(' Résumé_text', '')
    parsed_ Résumé = parse_ Résumé( Résumé_text)
    return jsonify(parsed_ Résumé)
</step>
</procedure>

## Test the Résumé Parsing Endpoint

Create a simple client to test the  Résumé parsing endpoint.

### Example Client Code:

<procedure title="Test  Résumé Parsing Endpoint" id="test-parsing-endpoint">
<step>
    <p>Create a new file <code>test_ Résumé_parsing.py</code> in the root directory and add the following code:</p>
    <code>
import requests

url = 'http://127.0.0.1:5000/parse_ Résumé'
data = {' Résumé_text': 'Experienced Python developer with a background in machine learning and data analysis.'}

response = requests.post(url, json=data)
print(response.json())
</code>
</step>
<step>
    <p>Run the client script to test the endpoint:</p>
    <ul>
        <li><code>python test_ Résumé_parsing.py</code></li>
    </ul>
</step>
</procedure>

## Conclusion

Setting up  Résumé parsing with SpaCy involves installing SpaCy and the necessary language model, initializing SpaCy in your application, creating a  Résumé parsing function, integrating it with Flask, and testing the endpoint. By following these steps, you can add powerful  Résumé parsing capabilities to your application.
