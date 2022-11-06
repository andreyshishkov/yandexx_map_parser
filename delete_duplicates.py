import pandas as pd

df = pd.read_csv('contacts_from_yandex.csv', delimiter=';')
print(df.shape)

new_df = df.drop_duplicates()
print(new_df.shape)

new_df.to_csv('contacts_from_yandex.csv', index=False, sep=';', encoding='utf-8-sig')
