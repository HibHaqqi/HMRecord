# app/services/fuel_service.py
import pandas as pd
from app.models.fuel import Fuel
from app import db

def upload_fuel_data(file_path, user_id):
    df = pd.read_excel(file_path)

    required_columns = {'Date', 'Unit FT', 'Unit Code', 'Contractor', 'Fuel Issued', 'Name', 'Location'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Excel file is missing required columns.")

    df = df.dropna(subset=['Date', 'Unit FT', 'Unit Code', 'Contractor', 'Fuel Issued', 'Name', 'Location'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Fuel Issued'] = pd.to_numeric(df['Fuel Issued'], errors='coerce')

    if df.empty or not user_id:
        raise ValueError("No records to insert or user ID missing.")

    records = df.apply(lambda row: {
        'date': row['Date'],
        'unit_ft': row['Unit FT'],
        'unit_code': row['Unit Code'],
        'contractor': row['Contractor'],
        'fuel_issued': row['Fuel Issued'],
        'name': row['Name'],
        'location': row['Location'],
        'user_id': user_id
    }, axis=1).tolist()

    if not records:
        raise ValueError("No records to insert.")

    db.session.bulk_insert_mappings(Fuel, records)
    db.session.commit()
    return "Data uploaded and validated successfully."
