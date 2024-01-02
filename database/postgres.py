import psycopg2
from configs.configs import postgres_query
# Connect to your postgres DB
#TODO:create tables automatically if not present

conn = psycopg2.connect(postgres_query)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM my_data")

# Retrieve query results
records = cur.fetchall()#TODO: данек))))0)