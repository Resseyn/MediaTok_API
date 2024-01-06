import psycopg2

from config import postgres_query

# Connect to your postgres DB

conn = psycopg2.connect(postgres_query)
