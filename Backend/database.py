
# import sqlite3
# from datetime import datetime

# def init_db():
#     conn = sqlite3.connect('safekarachi.db')
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS reports (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             location TEXT,
#             description TEXT,
#             vehicle_type TEXT,
#             timestamp TEXT
#         )
#     ''')
    
#     # Check if table is empty and add sample data
#     c.execute('SELECT COUNT(*) FROM reports')
#     count = c.fetchone()[0]
    
#     if count == 0:
#         print("Database is empty. Adding sample data...")
#         sample_data = [
#             ('Karachi Central', 'Speeding car detected by camera #CAM-001', 'car', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#             ('Clifton', 'Reckless motorcycle driving - no helmet', 'motorcycle', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#             ('Saddar', 'Illegal parking blocking traffic', 'truck', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#             ('Gulshan', 'Bus overspeeding in residential area', 'bus', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#             ('North Karachi', 'Car driving wrong way on one-way street', 'car', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#             ('Defence', 'Signal violation at red light', 'car', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#             ('Korangi', 'Rash driving near school zone', 'motorcycle', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#         ]
        
#         c.executemany('INSERT INTO reports (location, description, vehicle_type, timestamp) VALUES (?, ?, ?, ?)', sample_data)
#         print(f"✅ Added {len(sample_data)} sample records to database")
#     else:
#         print(f"📊 Database already contains {count} records")
    
#     conn.commit()
#     conn.close()

# def add_report(location, description, vehicle_type):
#     conn = sqlite3.connect('safekarachi.db')
#     c = conn.cursor()
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     c.execute('INSERT INTO reports (location, description, vehicle_type, timestamp) VALUES (?, ?, ?, ?)',
#               (location, description, vehicle_type, timestamp))
#     conn.commit()
#     conn.close()
#     print(f"📝 New report added: {vehicle_type} at {location}")

# def get_reports():
#     conn = sqlite3.connect('safekarachi.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM reports ORDER BY timestamp DESC')
#     reports = [{'id': r[0], 'location': r[1], 'description': r[2], 'vehicle_type': r[3], 'timestamp': r[4]} for r in c.fetchall()]
#     conn.close()
#     return reports

# def get_heatmap_data():
#     conn = sqlite3.connect('safekarachi.db')
#     c = conn.cursor()
#     c.execute('SELECT location, COUNT(*) as count FROM reports GROUP BY location')
#     data = [{'location': r[0], 'count': r[1]} for r in c.fetchall()]
#     conn.close()
#     return data


# truck logic 

import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('traffic_reports.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            priority TEXT DEFAULT 'MEDIUM',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_report(location, description, vehicle_type, priority='MEDIUM'):
    conn = sqlite3.connect('traffic_reports.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reports (location, description, vehicle_type, priority, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (location, description, vehicle_type, priority, datetime.now()))
    conn.commit()
    conn.close()

def get_reports():
    conn = sqlite3.connect('traffic_reports.db')
    c = conn.cursor()
    c.execute('''
        SELECT location, description, vehicle_type, priority, timestamp 
        FROM reports 
        ORDER BY timestamp DESC
    ''')
    reports = []
    for row in c.fetchall():
        reports.append({
            'location': row[0],
            'description': row[1],
            'vehicle_type': row[2],
            'priority': row[3],
            'timestamp': row[4]
        })
    conn.close()
    return reports

def get_heatmap_data():
    conn = sqlite3.connect('traffic_reports.db')
    c = conn.cursor()
    c.execute('''
        SELECT location, COUNT(*) as count, 
               SUM(CASE WHEN priority = 'HIGH' THEN 1 ELSE 0 END) as high_priority_count
        FROM reports 
        GROUP BY location
    ''')
    heatmap = []
    for row in c.fetchall():
        heatmap.append({
            'location': row[0],
            'count': row[1],
            'high_priority_count': row[2]
        })
    conn.close()
    return heatmap