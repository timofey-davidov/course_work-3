import pytest

from utils import get_data_base, get_filtered_data, get_last_values, get_formatted_data

def test_get_data_base(test_url):
    # проверка на получение данных
    assert len(get_data_base(test_url)[0]) > 0
    # проверка на подключение к несуществующему сайту
    assert get_data_base("https://wrong.url.com/")[0] is None
    # проверка на подключение к существующему сайту, но не получение JSON-реализуемого объекта
    assert get_data_base("https://github.com/timofey-davidov/-timofey-davidov-homework_12-2_project-3.git")[0] is None
    # проверка на ошибку доступа (4** - ошибка клиента, 5** - ошибка на стороне сервера)
    assert get_data_base("https://github.com/timofey-davidov/-timofey-davidov-homework_12-2_project-9.git")[0] is None

def test_get_filtered_data(test_data):
    # проверка на фильтрацию данных по полю state
    assert len(get_filtered_data(test_data)) == 4
    # проверка на фильтрацию данных по полю state и полю from
    assert len(get_filtered_data(test_data, ignore_incomplete_transactions=True)) == 2

def test_get_last_values(test_data):
    data = get_last_values(test_data, 4)
    # проверка на количество транзакций
    assert len(data) == 4
    # проверка на фильтрацию по времени
    assert data[0]["date"] == "2023-07-03T18:35:29.512364"

def test_get_formatted_data(test_data):
    data = get_formatted_data(test_data)
    print(data)
    assert data == ['26.08.2019 Перевод организации\nMaestro 1596 83** **** 5199 -> Счет **9589\n31957.58 руб.\n', '03.07.2023 Перевод организации\nMasterCard 7158 30** **** 6758 -> Счет **5560\n8221.37 USD\n', '30.06.2018 Перевод организации\nСчет **6952 -> Счет **6702\n9824.07 USD\n', '23.03.2018 Открытие вклада\n  -> Счет **2431\n48223.05 руб.\n', '04.04.2019 Перевод со счета на счет\n  -> Счет **4188\n79114.93 USD\n']
