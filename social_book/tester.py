from sqlalchemy import create_engine, text

# establish a connection to the database
engine = create_engine('postgresql://postgres:password@localhost:5432/social')

# create a connection object
conn = engine.connect()

# execute the SQL query
query = text("SELECT * FROM account_book;")
results = conn.execute(query)

# print out the results
for row in results:
    print(row)

# close the connection
conn.close()