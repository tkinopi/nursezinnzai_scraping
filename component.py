from time import sleep
import bs4
import requests
from bs4 import BeautifulSoup
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import collections

def get_job_list_url():
    base_url = 'https://www.nursejinzaibank.com/search/addr1_52/'
    first_url = 'https://www.nursejinzaibank.com/search/addr1_52/1'

    response = requests.get(first_url)

    # BeautifulSoupオブジェクトを作成します
    soup = BeautifulSoup(response.text, 'html.parser')
    print(1)

    a_element = ""
    elements = soup.find_all('div', id='pagenav')
    for element in elements:
        span_element = element.find('span', class_='end')
        if span_element:
            a_element = span_element.find('a')

            # aタグが存在する場合、そのテキストを出力
            if a_element:
                print(a_element.text)
                break
    url_list = []

    for i in range(1, int(a_element.text) + 1):
        url_list.append(base_url + str(i))

    return url_list

def get_job_url(url_list):
    urls = []
    base_url = "https://www.nursejinzaibank.com"
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # section class 'resultbox' のすべての要素を取得
        section_elements = soup.find_all('section', class_='resultbox')

        # 取得したsection要素の中から、目的のaタグのhref属性（URL）を抽出
        for section_element in section_elements:
            div_element = section_element.find('div', class_='result-btnArea')

            if div_element:
                a_element = div_element.find('a', class_='blue_btn')

                # aタグが存在し、href属性が存在する場合、そのURLを出力
                if a_element and 'href' in a_element.attrs:
                    print(base_url + a_element['href'])
                    urls.append(base_url + a_element['href'])
    return urls




def get_job_info(url):
    html = requests.get(url).text

    # Beautifulsoup4で解析
    soup = bs4.BeautifulSoup(html, "html.parser")

    # 'table'タグ、class='normal mb1'のすべてを探します
    dl_elements = soup.find_all('dl', {'class': 'jobinfoDetail-defin'})

    # URLを含む辞書を初期化します
    result_dict = {'url': url}

    for dl in dl_elements:
        # 'dt' タグのすべてを探します。
        dts = dl.find_all('dt')

        # 同様に 'dd' タグのすべてを探します。
        dds = dl.find_all('dd')

        # 'dt' と 'dd' の数が一致することを確認します。
        if len(dts) == len(dds):
            for dt, dd in zip(dts, dds):
                key = dt.get_text().strip()
                value = dd.get_text().strip()

                # 辞書に key-value ペアを追加します。
                result_dict[key] = value

    return result_dict


# # あなたのリスト型の求人情報データ
# jobs = [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value3', 'key2': 'value4'}]

def write_to_spreadsheet(jobs):
    # 全角のキーを半角に変換し、特殊な文字を削除または置換します
    for job in jobs:
        for key in list(job.keys()):
            new_key = key.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
            job[new_key] = job.pop(key).replace('\n', ' ').replace('\r', ' ')
    # pandas DataFrameに変換
    df = pd.DataFrame(jobs)

    # Google APIを使用するための認証情報（jsonファイル）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './service.json',
        ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
                )

    # gspread clientの生成
    gc = gspread.authorize(credentials)

    # Google Spreadsheetを開く
    sh = gc.open_by_key('1cZrejQEevR8SF6y7hRSY02oUUaJpQRwgnQnIvLt0PI8')

    # ワークシートを選択（例では最初のワークシートを選択）
    worksheet = sh.worksheet("result")

    df = df.fillna("")  # NaN値を空文字（""）に置き換え

    # DataFrameをGoogle Spreadsheetに書き込む
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def get_sheet_a_data():
    # Google APIを使用するための認証情報（jsonファイル）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './credentials.json',
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )

    # gspread clientの生成
    gc = gspread.authorize(credentials)

    # Google Spreadsheetを開く
    sh = gc.open_by_key('1nSpTz2KpxIj11nxK4BOj6507HzcWJemXHQeclHTObCQ')

    # ワークシートを選択（例ではシート名が "Sheet1" のワークシートを選択）
    worksheet = sh.worksheet("hellowork")

    # A列のデータを全て取得
    col_values = worksheet.col_values(1)  # 1 corresponds to 'A' column

    # url格納用のlist
    urls = []

    # 確認のために取得したURLを表示
    for url in col_values:
        print(url)
        urls.append(url)

    return urls
