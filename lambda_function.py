import os
import json
import pg8000

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

TRUNCS = {
    'hour': "DATE_TRUNC('hour', date_time)",
    'day':  "DATE_TRUNC('day',  date_time)",
    'week': "DATE_TRUNC('week', date_time)"
}

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    period = params.get('period', 'hour')
    if period not in TRUNCS:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'period must be hour, day or week'})
        }

    conn = pg8000.connect(
        host=DB_HOST,
        port=5432,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cur = conn.cursor()
    cur.execute(f"""
      SELECT {TRUNCS[period]} as period, COUNT(*)
      FROM dns_logs
      GROUP BY period
      ORDER BY period;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [{'period': str(r[0]), 'count': r[1]} for r in rows]
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
