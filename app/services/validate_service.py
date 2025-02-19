from sqlalchemy import func
from app.models.equipment import Equipment,db
from flask import jsonify

class DataValidate :
   def get_daily_hour_meters_over_22_hours():
    # Query to get the total hour meter for each unique unit code grouped by date
    result = db.session.query(
        Equipment.date,
        Equipment.unit_code,
        func.sum(Equipment.hm).label('total_hm')
    ).group_by(Equipment.date, Equipment.unit_code).having(func.sum(Equipment.hm) > 22).all()

    # Convert the result to a list of dictionaries
    over_22_hours = [
        {
            'date': row.date.strftime('%d/%m/%y'),  # Format date as DD/MM/YY
            'unit_code': row.unit_code,
            'total_hm': row.total_hm,
            'action': f"<a href='/details/{row.unit_code}/{row.date.strftime('%Y-%m-%d')}'>Detail</a>"  # Action link for details
        }
        for row in result
    ]
    return over_22_hours
   def get_total_hour_meters_by_unit_code():
    result = db.session.query(
        Equipment.date,Equipment.unit_code,
        func.sum(Equipment.hm).label('total_hm')
    ).group_by(Equipment.date,Equipment.unit_code).all()

    total_hm_by_unit_code = [{'date':row.date,'unit_code': row.unit_code, 'total_hm': row.total_hm} for row in result]
    return total_hm_by_unit_code



