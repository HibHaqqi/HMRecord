from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app
from app.services.equipment_service import upload_hour_meter_data
import os
from werkzeug.utils import secure_filename

eqp_bp = Blueprint('eqp', __name__)


@eqp_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        flash('Session expired. Please log in again.')
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    current_app.logger.info(f"Session active with user_id={user_id}")

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

        return redirect(url_for('eqp.upload'))

    return render_template('upload.html')