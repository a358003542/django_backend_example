#!/usr/bin/env python
# -*-coding:utf-8-*-

import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(dbname='django_backend',
                        user='django_backend',
                        password='django_backend',
                        host='localhost',
                        port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
# cur.execute("SELECT * FROM django_backend")

# Retrieve query results
# records = cur.fetchall()