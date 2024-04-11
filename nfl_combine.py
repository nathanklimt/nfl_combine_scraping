from bs4 import BeautifulSoup as bs
import requests
import csv

def fetch_data(url_list):
    data_list = []
    for url in url_list:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        data_list.append(soup)
    return data_list

def extract_table_data(soup):
    table = soup.find('table')
    table_data = []

    if table:
        header_row = table.find('thead').find('tr')
        if header_row:
            headers = [cell.text.strip() for cell in header_row.find_all('td')]
            table_data.append(headers)

        body_rows = table.find('tbody').find_all('tr')
        for row in body_rows:
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            table_data.append(row_data)

    return table_data

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def main():
    url_list = [f"http://nflcombineresults.com/nflcombinedata_expanded.php?year={num}&pos=&college=" for num in range(1987, 2025)]
    filename = "nfl_combine.csv"

    data_list = fetch_data(url_list)

    header_data = extract_table_data(data_list[0])
    export_to_csv(header_data, filename)

    player_data = []
    for data in data_list:
        player_data.extend(extract_table_data(data))

    export_to_csv(player_data, filename)

main()