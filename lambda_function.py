import os
import json
import psycopg2

# read env vars
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

# map period to SQL date_trunc
TRUNCS = {
    'hour': "DATE_TRUNC('hour', date_time)",
    'day':  "DATE_TRUNC('day',  date_time)",
    'week': "DATE_TRUNC('week', date_time)"
}

def lambda_handler(event, context):
    # get period param (hour day or week)
    params = event.get('queryStringParameters') or {}
    period = params.get('period', 'hour')
    if period not in TRUNCS:
        return {
            'statusCode':400,
            'body': json.dumps({'error':'period must be hour day or week'})
        }

    # connect to RDS
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    sql = f"""
      SELECT {TRUNCS[period]} as period, COUNT(*) 
      FROM dns_logs 
      GROUP BY period 
      ORDER BY period;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # format as list of {period, count}
    result = [
      {'period': str(row[0]), 'count': row[1]}
      for row in rows
    ]
    return {
      'statusCode':200,
      'body': json.dumps(result)
    }
