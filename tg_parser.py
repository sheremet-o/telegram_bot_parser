import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlite.db', echo=False)

data = pd.read_excel('urls.xlsx')
print(data)
data_dict = data.to_sql('urls', engine, if_exists='append')
