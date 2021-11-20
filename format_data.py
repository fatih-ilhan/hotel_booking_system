import random

import pandas as pd
import os
import json
from googlesearch import search
import pyzipcode


def format_hotels_data():

    file_path = 'data/Hotels.xls'
    df = pd.read_excel(file_path)

    columns_to_filter = ['NAME,C,80', 'ADDRESS,C,80', 'ZIP,C,80', 'PHONE,C,80', 'WEB_URL,C,142']
    new_column_names = ['name', 'address', 'zip_code', 'phone', 'web_url']
    df = df[columns_to_filter]
    df.columns = new_column_names

    return df


def format_findhotel_data():

    folder_path = 'data/findhotel'

    file_path = 'findhotel.csv'
    formatted_file_path = os.path.join(folder_path, 'formatted_data.csv')
    if os.path.isfile(formatted_file_path):
        return pd.read_csv(formatted_file_path)
    elif os.path.isfile(file_path):
        df = pd.read_csv(file_path)
    else:
        df_list = []
        for f in os.listdir(folder_path):
            print(f)
            data = json.load(open(os.path.join(folder_path, f)))
            for hotel in data['hotel']:
                hotel_data = []
                for k, v in hotel.items():
                    if k in ['name', 'rating']:
                        hotel_data.append(v[0])
                    elif k == 'price':
                        hotel_data.append(v[0][1:])
                    elif k == 'address':
                        hotel_data.append(v[0].split('|')[0])
                    elif k == 'num_review':
                        hotel_data.append(v[0].split(' ')[0])
                    else:
                        hotel_data.append('')

                # to search
                query = hotel_data[0]

                for url in search(query, tld="com", num=1, stop=1, pause=2):
                    hotel_data.append(url)

                df_list.append(hotel_data)

        df = pd.DataFrame(df_list)
        df.columns = ['name', 'price', 'address', 'rating', 'num_review', 'web_url']
        df.to_csv(file_path)

    df_list = []
    zcdb = pyzipcode.ZipCodeDatabase()
    for i, r in df.iterrows():
        data = list(r.values)
        if len(r.values[2]) > 5:
            data = data[:2] + [str(random.randint(70, 300))] + data[2:-1]
            df.iloc[i] = data
        else:
            if pd.isna(r.rating) or len(r.rating) > 4:
                data = data[:4] + ['', '', data[4]]

        city = df.iloc[i].address.split(',')[-2][1:]
        state = df.iloc[i].address.split(',')[-1][1:]
        try:
            zip_code = zcdb.find_zip(city, state)[0].zip
        except:
            zip_code = ''
        df_list.append(data + [zip_code, ''])

    df = pd.DataFrame(df_list).iloc[:, 1:]
    df.columns = ['name', 'price', 'address', 'rating', 'num_review', 'web_url', 'zip_code', 'phone']
    df = df[['name', 'address', 'zip_code', 'phone', 'web_url', 'rating', 'num_review', 'price']]
    df['rating'] = df[["rating"]].apply(pd.to_numeric)
    df['num_review'] = df[["num_review"]].apply(lambda x: x.str.replace(',', ''))
    df['num_review'] = df[["num_review"]].apply(pd.to_numeric, downcast='integer')

    return df

df = format_findhotel_data()
df.to_csv('data/findhotel/formatted_data.csv', index=False)
