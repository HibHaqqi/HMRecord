# app/services/equipment_service.py
import pandas as pd
from app.models.equipment import Equipment, db


def upload_hour_meter_data(file_path, user_id):
    df = pd.read_excel(file_path)

    required_columns = {'Date','Unit Code','Contractor','HM Start','HM Stop','HM',
                        'Opex/Capex','Cost Category','Cost Activity','Location','Notes'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Excel file is missing required columns.")

    df = df.dropna(subset=['Date', 'HM Start', 'HM Stop', 'HM'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df[['HM Start','HM Stop','HM']] = df[['HM Start','HM Stop','HM']].apply(pd.to_numeric, errors='coerce')

    if df.empty or not user_id:
        raise ValueError("No records to insert or user ID missing.")

    records = df.apply(lambda row: {
        'date': row['Date'],
        'unit_code': row['Unit Code'],
        'contractor': row['Contractor'],
        'hm_start': row['HM Start'],
        'hm_stop': row['HM Stop'],
        'hm': row['HM'],
        'opex_capex': row['Opex/Capex'],
        'cost_category': row['Cost Category'],
        'cost_activity': row['Cost Activity'],
        'location': row['Location'],
        'notes': row.get('Notes', None),
        'user_id': user_id
    }, axis=1).tolist()

    if not records:
        raise ValueError("No records to insert.")

    db.session.bulk_insert_mappings(Equipment, records)
    db.session.commit()
    return "Data uploaded and validated successfully."