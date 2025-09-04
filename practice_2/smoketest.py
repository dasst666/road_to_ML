from sqlalchemy import text, create_engine
print("Import OK")

engine = create_engine("postgresql+psycopg://fastDB_user:strong_password@127.0.0.1:5432/fastDB", echo=False)
with engine.connect() as conn:
    print(conn.execute(text("select 1")).scalar())
print("Connect OK")