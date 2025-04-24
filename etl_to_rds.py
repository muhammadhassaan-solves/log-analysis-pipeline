import os
import boto3
import psycopg2
import pandas as pd
import re

# ---------- CONFIG SECTION ----------
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
bucket_name = os.environ['BUCKET_NAME']
file_key = os.environ['FILE_KEY']

db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
# ------------------------------------

# compile regex for “queries: info: client X.X.X.X#PORT: query: NAME CLASS TYPE”
pattern = re.compile(
    r"^(?P<date>\d{2}-\w{3}-\d{4})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+queries:\s+info:\s+client\s+"
    r"(?P<client_ip>\d{1,3}(?:\.\d{1,3}){3})#(?P<client_port>\d+):\s+"
    r"query:\s+(?P<query_name>\S+)\s+(?P<query_class>\S+)\s+(?P<dns_record_type>\w+)"
)

# 1) Download lines from S3
s3 = boto3.client('s3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)
obj = s3.get_object(Bucket=bucket_name, Key=file_key)
lines = obj['Body'].read().decode('utf-8').splitlines()

# 2) Parse
records = []
for line in lines:
    m = pattern.match(line)
    if not m:
        continue
    gd = m.groupdict()
    dt = f"{gd['date']} {gd['time']}"
    records.append({
        'date_time':       dt,
        'client_ip':       gd['client_ip'],
        'client_port':     int(gd['client_port']),
        'dns_record_type': gd['dns_record_type'],
        'query_name':      gd['query_name'],
        'query_class':     gd['query_class'],
        'geography':       '',           # fill if you have geo data
        'raw_line':        line
    })

df = pd.DataFrame(records)
print(f"Parsed {len(df)} query lines")

# 3) Insert into RDS
conn = psycopg2.connect(
    host=db_host, dbname=db_name,
    user=db_user, password=db_pass
)
cur = conn.cursor()
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO dns_logs (
          date_time, client_ip, client_port,
          dns_record_type, query_name,
          query_class, geography, raw_line
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row['date_time'], row['client_ip'], row['client_port'],
        row['dns_record_type'], row['query_name'],
        row['query_class'], row['geography'], row['raw_line']
    ))
conn.commit()
cur.close()
conn.close()
print("✅ ETL Complete: Data loaded into dns_logs")
