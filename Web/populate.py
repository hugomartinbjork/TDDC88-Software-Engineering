import pandas as pd
from sqlalchemy import create_engine
import psycopg2


'''Engine with deployed postgreSQL-database'''
engine = create_engine(
"postgresql://admin:rdxsolutions@postgres-service:5432/postgresdb")

# '''Engine with local SQLite-database'''
# engine = create_engine("sqlite:///mydatabase1")


with pd.ExcelFile('db_data/groupinfo.xlsx') as xls:
    df = pd.read_excel(xls)
    df.to_sql(name='backend_group', con=engine,
              if_exists='append', index=False)

# with pd.ExcelFile('db_data/costcenter.xlsx') as xls:
#     df = pd.read_excel(xls)
#     df.to_sql(name='backend_costcenter', con=engine,
#               if_exists='append', index=False)

# with pd.ExcelFile('db_data/supplier.xlsx') as xls:
#     df = pd.read_excel(xls)
#     df.to_sql(name='backend_supplier', con=engine,
#               if_exists='append', index=False)


# with pd.ExcelFile('db_data/testarticles.xlsx') as xls:
#     df = pd.read_excel(xls)
#     df.to_sql(name='backend_article', con=engine,
#               if_exists='append', index=False)

with pd.ExcelFile('db_data/storages.xlsx') as xls:
    df = pd.read_excel(xls)
    df.to_sql(name='backend_storage', con=engine,
              if_exists='append', index=False)

with pd.ExcelFile('db_data/compartments.xlsx') as xls:
    df = pd.read_excel(xls)
    df.to_sql(name='backend_compartment', con=engine,
              if_exists='append', index=False)

with pd.ExcelFile('db_data/transactions.xlsx') as xls:
    df = pd.read_excel(xls)
    df.to_sql(name='backend_transaction', con=engine,
              if_exists='append', index=False)



# Verkar inte fungera jättebra med att läsa in user.

# with pd.ExcelFile('scripts/user.xlsx') as xls:
#     df = pd.read_excel(xls)
#     df.to_sql(name='auth_user', con=engine, if_exists='append', index=False)

# with pd.ExcelFile('user_info.xlsx') as xls:
#     df = pd.read_excel(xls)
#     df.to_sql(name='backend_userinfo', con=engine,
#               if_exists='append', index=False)


# with pd.ExcelFile('scripts/transaction.xlsx') as xls:
#     df = pd.read_excel(xls)
#     df.to_sql(name='backend_transaction', con=engine,
#               if_exists='append', index=False)

