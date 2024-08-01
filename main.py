from io import StringIO

import pandas as pd

from html_extractor import html_parser
from internet_status import is_connected


def adjust_month(rows):
    """
    Adjusts the month column by splitting, then joining, e.g.: 'AUG 2024 NGQ4' -> ['AUG', '2024', 'NGQ4']
    The list turns into month: 'AUG 2024' and ticket: 'NGQ4'
    :param rows: The 'month' column of the dataframe, containing all rows
    :return: month, ticket individually
    """
    row_date = rows.split(' ')
    month = ' '.join(row_date[:2])
    ticket = row_date[-1]
    return month, ticket


def main(url):
    html = html_parser(url)

    if html is None:
        exit()
    else:
        html = StringIO(html)

    df = pd.read_html(html)[0]
    df.columns = ['Month', 'Options', 'Chart', 'Last', 'Change', 'Prior Settle', 'Open', 'High', 'Low', 'Volume',
                  'Updated']
    df = df.drop('Chart', axis=1)

    # Calls the function and then rearranges the month and ticket column
    df['Month'], df['Ticket'] = zip(*df['Month'].apply(adjust_month))

    # Removes the hour of the updated column: '12:30:38 CT 28 Jul 2024' -> '28 Jul 2024'
    df['Updated'] = df['Updated'].apply(lambda x: ' '.join(x.split()[2:]))

    with open('data.csv', 'w', newline='') as file:
        df.to_csv(file, index=False)


if __name__ == '__main__':
    if is_connected():
        URL = 'https://www.cmegroup.com/markets/energy/natural-gas/natural-gas.quotes.html'
        main(URL)
    else:
        print('No internet connection available')
