from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import UploadedFile
from app.utils.file_utils import save_file

views = Blueprint('views', __name__)


@views.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path, filename = save_file(file, current_app.config['UPLOAD_FOLDER'])
        uploaded_file = UploadedFile(user_id=1, filename=filename, file_path=file_path)
        db.session.add(uploaded_file)
        db.session.commit()

        # Import process_file dynamically to avoid circular import
        from app.tasks import process_file
        process_file.delay(uploaded_file.id, file_path)
        return jsonify({"message": "File uploaded successfully"}), 200


@views.route('/process/<int:file_id>', methods=['GET'])
def process_file(file_id):
    # Dummy function to demonstrate AI processing
    # Implement actual AI processing logic here
    uploaded_file = UploadedFile.query.get(file_id)
    if not uploaded_file:
        return jsonify({"error": "File not found"}), 404

    # Simulate AI processing
    result = {"status": "Processing completed", "file_id": file_id, "file_path": uploaded_file.file_path}

    return jsonify(result), 200
