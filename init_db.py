import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 1. Connect to default postgres DB to create the finsage database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port=5432
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Check if database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'finsage'")
    exists = cur.fetchone()
    
    if not exists:
        cur.execute("CREATE DATABASE finsage")
        print("Created database: finsage")
    else:
        print("Database finsage already exists")
    
    cur.close()
    conn.close()
except Exception as e:
    print("Error creating database:", e)
    import sys
    sys.exit(1)

# 2. Connect to the finsage DB and run the schemas
try:
    conn = psycopg2.connect(
        host="localhost",
        database="finsage",
        user="postgres",
        password="postgres",
        port=5432
    )
    cur = conn.cursor()
    
    with open('data/schema.sql', 'r') as f:
        schema = f.read()
    
    with open('data/seed_data.sql', 'r') as f:
        seed = f.read()
    
    print("Running schema.sql...")
    cur.execute(schema)
    
    print("Running seed_data.sql...")
    cur.execute(seed)
    
    conn.commit()
    print("Successfully created tables and seeded data!")
    
    cur.close()
    conn.close()
except Exception as e:
    print("Error executing SQL scripts:", e)
    
