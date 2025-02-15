# app/services/equipment_service.py
import pandas as pd
from app.models.equipment import Equipment, db
from datetime import datetime

def upload_hour_meter_data(file_path, user_id):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Validate the data
    required_columns = ['Date', 'Unit Code', 'Contractor', 'HM Start', 'HM Stop', 'HM', 
                        'Opex/Capex', 'Cost Category', 'Cost Activity', 'Location', 'Notes']
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Excel file must contain a '{column}' column.")

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if df['Date'].isnull().any():
        raise ValueError("Some dates are invalid or missing.")

    # Save the data to the database
    for index, row in df.iterrows():
        equipment = Equipment(
            date=row['Date'],
            unit_code=row['Unit Code'],
            contractor=row['Contractor'],
            hm_start=row['HM Start'],
            hm_stop=row['HM Stop'],
            hm=row['HM'],
            opex_capex=row['Opex/Capex'],
            cost_category=row['Cost Category'],
            cost_activity=row['Cost Activity'],
            location=row['Location'],
            notes=row['Notes'] if pd.notnull(row['Notes']) else None,
            user_id=user_id
        )
        db.session.add(equipment)
    db.session.commit()

    return "Data uploaded and validated successfully."
