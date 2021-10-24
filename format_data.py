import pandas as pd


def format_hotels_data():

    file_path = 'data/Hotels.xls'
    df = pd.read_excel(file_path)

    columns_to_filter = ['NAME,C,80', 'ADDRESS,C,80', 'ZIP,C,80', 'PHONE,C,80', 'WEB_URL,C,142']
    new_column_names = ['name', 'address', 'zip_code', 'phone', 'web_url']
    df = df[columns_to_filter]
    df.columns = new_column_names

    return df
