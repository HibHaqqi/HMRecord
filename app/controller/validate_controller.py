from flask import Blueprint, render_template, redirect,request,flash,url_for
from app.services.validate_service import DataValidate
import pandas as pd
from app.models.equipment import Equipment,db
val_bp = Blueprint('val', __name__)

@val_bp.route('/validate-hour-meters', methods=['GET'])
def validate_hour_meters():
    return DataValidate.get_daily_hour_meters_over_22_hours()

@val_bp.route('/total-hour-meters', methods=['GET'])
def total_hour_meters():
    return DataValidate.get_total_hour_meters_by_unit_code()

@val_bp.route('/hour-meter-details/<unit_code>/<date>', methods=['GET'])
def hour_meter_details(unit_code, date):
    date = pd.to_datetime(date).date()
    details = DataValidate.get_hour_meter_details(unit_code, date)
    return render_template('hour_meter_details.html', details=details, unit_code=unit_code, date=date.strftime('%d/%m/%y'))

@val_bp.route('/total-hour-meter-details/<unit_code>//<date>', methods=['GET'])
def total_hour_meter_details(unit_code,date):
    date = pd.to_datetime(date).date()
    details = DataValidate.get_total_hour_meter_details(unit_code,date)
    return render_template('total_hour_meter_details.html', details=details, unit_code=unit_code,date=date.strftime('%d/%m/%y'))

@val_bp.route('/edit-hour-meter/<int:id>', methods=['GET', 'POST'])
def edit_hour_meter(id):
    # Fetch the existing record
    record = Equipment.query.get(id)
    
    if not record:
        flash("Record not found.")
        return redirect(url_for('some_route'))  # Redirect to a relevant route

    if request.method == 'POST':
        # Get data from the form
        unit_code = request.form.get('unit_code')
        hm_start = request.form.get('hm_start')
        hm_stop = request.form.get('hm_stop')
        hm = request.form.get('hm')
        opex_capex = request.form.get('opex_capex')
        cost_category = request.form.get('cost_category')
        cost_activity = request.form.get('cost_activity')
        location = request.form.get('location')
        notes = request.form.get('notes')

        try:
            # Call the edit service
            message = DataValidate.edit_hour_meter_record(id, unit_code,hm_start, hm_stop, hm, opex_capex, cost_category, cost_activity, location, notes)
            flash(message)
            return redirect(url_for('eqp.upload'))  # Redirect to a relevant route after editing
        except Exception as e:
            flash(f"Error: {e}")

    # Render the edit form with existing record data
    return render_template('edit_hour_meter.html', record=record)
@val_bp.route('/delete-hour-meter/<int:id>', methods=['POST'])
def delete_hour_meter(id):
    # Find the record by ID
    record = Equipment.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
        flash('Record deleted successfully.', 'success')
    else:
        flash('Record not found.', 'danger')
    
    return redirect(url_for('eqp.upload'))