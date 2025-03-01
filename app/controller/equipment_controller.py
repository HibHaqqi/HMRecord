from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app,send_from_directory
from app.services.equipment_service import upload_hour_meter_data
from app.models.user import User
import os
from werkzeug.utils import secure_filename

from app.services.validate_service import DataValidate

eqp_bp = Blueprint('eqp', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@eqp_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        flash('Session expired. Please log in again.')
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    user = User.query.get(user_id)
    current_app.logger.info(f"Session active with user_id={user_id}, role={user.role}")

    
    
    over_22_hours = []
    total_hm_by_unit_code = []

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.strip():
            flash('No file selected')
            return redirect(request.url)

        file_path = os.path.join('app/uploads', secure_filename(file.filename))
        file.save(file_path)

        try:
            message = upload_hour_meter_data(file_path, user_id)
            flash(message)
        except Exception as e:
            current_app.logger.error(f"Upload failed: {e}")
            flash(f"Error: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
        over_22_hours = DataValidate.get_daily_hour_meters_over_22_hours(user)
        total_hm_by_unit_code = DataValidate.get_total_hour_meters_by_unit_code(user)
        return redirect(url_for('eqp.upload'))

    over_22_hours = DataValidate.get_daily_hour_meters_over_22_hours(user)
    total_hm_by_unit_code = DataValidate.get_total_hour_meters_by_unit_code(user)
    return render_template('upload.html',over_22_hours=over_22_hours, total_hm_by_unit_code=total_hm_by_unit_code)
@eqp_bp.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    print(f"Looking for file at: {file_path}")  # Debugging line
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        print("File not found")  # Debugging line
        return "File not found", 404