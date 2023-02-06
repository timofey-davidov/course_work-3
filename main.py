# блок импорта
from utils import get_data_base, get_filtered_data, get_last_values, get_formatted_data

# блок констант и переменных
IGNORE_INCOMPLETE_TRANSACTIONS = True   # булева переменная для учета неполных транзакций (присутсвтие/отсутсвие данных from)
URL = "https://jsonkeeper.com/b/46IM"   # ссылка на БД в формате json
VALUES_COUNT = 5                        # количество операций для вывода

# основной блок программы
def main():
    # получаем БД, проверяем на ошибки
    data, info = get_data_base(URL)
    if not data:
        exit(info)
    else:
        print(info)

    # фильтруем полученную БД
    data = get_filtered_data(data, ignore_incomplete_transactions = IGNORE_INCOMPLETE_TRANSACTIONS)

    # сокращаем БД до нужного количества транзакций
    data = get_last_values(data, VALUES_COUNT)

    # формируем данные в отформатированном формате
    data = get_formatted_data(data)

    # выводим данные
    print("INFO: Вывод данных:")
    for transaction in data:
        print(transaction, end="\n")

# вызов основной функции main
if __name__ == "__main__":
    main()