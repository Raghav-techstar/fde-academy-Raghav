import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


# ============================================================
# EXERCISE 2 - POSTGRESQL LOAD
# ============================================================


# ------------------------------------------------------------
# TASK 1: Load cleaned CSV
# ------------------------------------------------------------

df = pd.read_csv(
    "shipments_clean.csv",
    parse_dates=["shipped_date", "delivered_date"]
)

print("========================================")
print("TASK 1: LOAD CLEANED DATA")
print("========================================")

print("Python cleaned row count:")
print(len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ------------------------------------------------------------
# TASK 2: Connect to PostgreSQL
# ------------------------------------------------------------

username = "fde_user"
password = "Sep@2026"
host = "localhost"
port = 5432
database = "fde_academy"

# Encode special characters such as @ in password
encoded_password = quote_plus(password)

connection_url = (
    f"postgresql+psycopg2://"
    f"{username}:{encoded_password}@"
    f"{host}:{port}/{database}"
)

engine = create_engine(connection_url)


print("\n========================================")
print("TASK 2: POSTGRESQL CONNECTION")
print("========================================")


# Test connection
with engine.connect() as connection:

    result = connection.execute(
        text("SELECT current_database(), current_user")
    )

    database_name, user_name = result.fetchone()

    print("Connected successfully!")
    print("Database:", database_name)
    print("User:", user_name)


# ------------------------------------------------------------
# TASK 3: Load cleaned data into PostgreSQL
# ------------------------------------------------------------

print("\n========================================")
print("TASK 3: LOAD DATA INTO POSTGRESQL")
print("========================================")

df.to_sql(
    "shipments_clean",
    engine,
    if_exists="replace",
    index=False,
    method="multi",
    chunksize=1000
)

print("shipments_clean table created/loaded successfully.")


# ------------------------------------------------------------
# TASK 4: Verify PostgreSQL row count
# ------------------------------------------------------------

print("\n========================================")
print("TASK 4: VERIFY ROW COUNT")
print("========================================")

with engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM shipments_clean")
    )

    postgres_count = result.scalar()


python_count = len(df)

print("Python row count:")
print(python_count)

print("\nPostgreSQL row count:")
print(postgres_count)

print("\nRow counts match:")
print(postgres_count == python_count)


# ------------------------------------------------------------
# TASK 5: Spot check PostgreSQL data
# ------------------------------------------------------------

print("\n========================================")
print("TASK 5: SPOT CHECK")
print("========================================")

with engine.connect() as connection:

    result = connection.execute(
        text("""
            SELECT *
            FROM shipments_clean
            LIMIT 5
        """)
    )

    rows = result.fetchall()

print("First 5 rows from PostgreSQL:\n")

for row in rows:
    print(row)


# ------------------------------------------------------------
# TASK 6: Verify table exists
# ------------------------------------------------------------

print("\n========================================")
print("TASK 6: VERIFY TABLE")
print("========================================")

with engine.connect() as connection:

    result = connection.execute(
        text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'shipments_clean'
        """)
    )

    table = result.fetchone()

if table:
    print("Table 'shipments_clean' exists in PostgreSQL.")
else:
    print("Table 'shipments_clean' was not found.")


# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------

print("\n========================================")
print("EXERCISE 2 COMPLETED")
print("========================================")

if postgres_count == python_count:
    print("SUCCESS: All cleaned records were loaded correctly.")
else:
    print("WARNING: Python and PostgreSQL row counts do not match.")