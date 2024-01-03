import psycopg2
from config import postgres_query
# Connect to your postgres DB
#TODO:create tables automatically if not present

conn = psycopg2.connect(postgres_query)
