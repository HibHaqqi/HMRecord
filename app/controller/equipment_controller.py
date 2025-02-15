from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.services.equipment_service import upload_hour_meter_data
import os

eqp_bp = Blueprint('eqp', __name__)


@eqp_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file_path = os.path.join('app/uploads', file.filename)
            file.save(file_path)
            try:
                user_id = session.get('user_id')  # Assuming user_id is stored in session
                message = upload_hour_meter_data(file_path, user_id)
                flash(message)
            except ValueError as e:
                flash(str(e))
            return redirect(url_for('eqp_bp.upload'))
    return render_template('upload.html')
