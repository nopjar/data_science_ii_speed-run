import bs4
import requests
import pandas as pd

def get_column_titles(table):
    col_names = []
    for th in table.select_one('tr').select('th'):
        col_names.append(th.text.strip())
    return col_names

def map_alt_to_place(alt):
    if alt == 'First place':
        return 1
    if alt == 'Second place':
        return 2
    if alt == 'Third place':
        return 3
    return -1

def get_multi_data(table, column_titles):
    data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    for i, row in enumerate(table.select('tbody tr')):
        for j, col in enumerate(row.select('td')):
            if j == 0 and col.select('img'):
                # first three places are not displayed as text
                img = col.select_one('img')
                data[j].append(map_alt_to_place(img['alt']))
                continue

            if j == 4:
                row.
            data[j].append(col.text.strip())

    df = pd.DataFrame.from_dict(data)
    df.columns = column_titles
    return df

def main():
    response = requests.get("https://www.speedrun.com/sm64?h=120_Star-n64&x=wkpoo02r-e8m7em86.9qj7z0oq")
    print(response.status_code)

    bsoup = bs4.BeautifulSoup(response.text, "lxml")
    table = bsoup.select_one('table')

    col_names = get_column_titles(table)
    df = get_multi_data(table, col_names)
    print(df)


if __name__ == '__main__':
    main()
