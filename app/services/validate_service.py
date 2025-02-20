from sqlalchemy import func
from app.models.equipment import Equipment,db
from flask import jsonify
import pandas as pd

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
            'date': row.date,  # Ensure this is a datetime object
            'unit_code': row.unit_code,
            'total_hm': row.total_hm
        } for row in result
    ]

    return over_22_hours
   
   def get_total_hour_meters_by_unit_code():
    result = db.session.query(
        Equipment.date,Equipment.unit_code,
        func.sum(Equipment.hm).label('total_hm')
    ).group_by(Equipment.date,Equipment.unit_code).all()

    total_hm_by_unit_code = [{'date':row.date,'unit_code': row.unit_code, 'total_hm': row.total_hm} for row in result]
    return total_hm_by_unit_code
   def get_hour_meter_details(unit_code, date):
    result = db.session.query(Equipment).filter(
        Equipment.unit_code == unit_code,
        Equipment.date == date
    ).all()

    details = [{
        'id':record.id,
        'date': record.date.strftime('%d/%m/%y'),
        'unit_code': record.unit_code,
        'hm_start': record.hm_start,
        'hm_stop': record.hm_stop,
        'hm': record.hm,
        'contractor': record.contractor,
        'opex_capex': record.opex_capex,
        'cost_category': record.cost_category,
        'cost_activity': record.cost_activity,
        'location': record.location,
        'notes': record.notes
    } for record in result]

    return details
   def get_total_hour_meter_details(unit_code,date):
     result = db.session.query(Equipment).filter(
        Equipment.unit_code == unit_code,
        Equipment.date == date
    ).all()

     details = [{
        'id':record.id,
        'date': record.date.strftime('%d/%m/%y'),
        'unit_code': record.unit_code,
        'hm_start': record.hm_start,
        'hm_stop': record.hm_stop,
        'hm': record.hm,
        'contractor': record.contractor,
        'opex_capex': record.opex_capex,
        'cost_category': record.cost_category,
        'cost_activity': record.cost_activity,
        'location': record.location,
        'notes': record.notes
    } for record in result]

     return details
   def edit_hour_meter_record(id, hm_start, hm_stop, hm, opex_capex, cost_category, cost_activity, location, notes):
      # Fetch the record by ID
    record = Equipment.query.get(id)
    
    if not record:
        raise ValueError("Record not found.")

    # Update the record fields
    record.hm_start = hm_start
    record.hm_stop = hm_stop
    record.hm = hm
    record.opex_capex = opex_capex
    record.cost_category = cost_category
    record.cost_activity = cost_activity
    record.location = location
    record.notes = notes

    # Commit the changes to the database
    db.session.commit()
    return "Record updated successfully."
    

    





