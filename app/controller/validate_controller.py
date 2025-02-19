from flask import Blueprint
from app.services.validate_service import DataValidate

val_bp = Blueprint('val', __name__)

@val_bp.route('/validate-hour-meters', methods=['GET'])
def validate_hour_meters():
    return DataValidate.get_daily_hour_meters_over_22_hours()

@val_bp.route('/total-hour-meters', methods=['GET'])
def total_hour_meters():
    return DataValidate.get_total_hour_meters_by_unit_code()