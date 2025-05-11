import csv
from database.models import HydroData
from database.crud import DBSession

def import_csv_data(file_path: str):
    """导入历史水文数据"""
    with DBSession() as session, open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = HydroData(
                sensor_id=int(row['sensor_id']),
                water_level=float(row['water_level']),
                flow_rate=float(row['flow_rate']),
                timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
                is_anomaly=int(row['is_anomaly'])
            )
            session.add(record)
        session.commit()
    print(f"成功导入{reader.line_num}条记录")