from flask import Blueprint, render_template
from app.services.validate_service import DataValidate
import pandas as pd

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

