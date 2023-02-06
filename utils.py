import requests, datetime


def get_data_base(URL):
    """
    Функция для получения базы данных из указанного URL
    :param URL: str – ссылка на БД
    :return:
        при возникновении ошибки – None, Тип ошибки
        без ошибки – dict (словарь, переведенный из JSON), str (Сообщение об успешном выводе)
    """
    try:
        transactions = requests.request("GET", URL, verify=False)
        # проверка на обработку доступа (2** - доступ присутствует)
        if transactions.status_code == 200:
            return transactions.json(), "INFO: данные получены успешно\n"
        # проверка на обработку доступа (4** - ошибка клиента, 5** - ошибка на стороне сервера)
        return None, f"ERROR: status code {transactions.status_code}\n"
    # проверка на потерю соединения
    except requests.exceptions.ConnectionError:
        return None, "ERROR: requests.exceptions.ConnectionError\n"
    # проверка на невозможность декодирования формата JSON
    except requests.exceptions.JSONDecodeError:
        return None, "ERROR: requests.exceptions.JSONDecodeError\n"

def get_filtered_data(data, ignore_incomplete_transactions = False):
    """
    Функция, которая принимает БД в виде словаря и возвращает отфильтрованную БД в виде словаря по наличию state, условию state == EXECUTED, а также наличию state
    :param data: dict – БД в виде словаря
    :param ignore_incomplete_transactions: bool – аргумент наличия/отсутствия проверки на наличие атрибута state в словаре
    :return: data: dict – БД в виде словаря
    """
    data = [item for item in data if "state" in item and item["state"] == "EXECUTED"]
    if ignore_incomplete_transactions == True:
        data = [item for item in data if "from" in item]
    return data

def get_last_values(data, values_count):
    """
    Функция, которая принимает БД в виде словаря и возвращает его урезаную до указанного количества транзакций версию
    :param data: dict – БД в виде словаря
    :param values_count: int – количество транзакций
    :return: data: dict – БД в виде словаря
    """
    data = sorted(data, key = lambda item: item["date"], reverse=True)
    data = data[:values_count]
    return data

def get_formatted_data(data):
    """
    Функция, которая принимает БД в виде словаря, а возвращает отформатированный список из транзакций
    :param data: dict – БД в виде словаря
    :return: formatted_data: list – список транзакций
    """
    formatted_data = list()
    for transaction in data:
        date = datetime.datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = transaction["description"]
        from_info, from_bill = "", ""
        if "from" in transaction:
            sender = transaction["from"].split()
            from_bill = sender.pop(-1)
            if "счет" in sender[0].lower():
                from_bill = f"**{from_bill[-4:]}"
            else:
                from_bill = f"{from_bill[:4]} {from_bill[4:6]}** **** {from_bill[-4:]}"
            from_info = " ".join(sender)
        to = f"{transaction['to'].split()[0]} **{transaction['to'][-4:]}"
        operation_amount = f"{transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}"

        formatted_data.append(f"""\
{date} {description}
{from_info} {from_bill} -> {to}
{operation_amount}\n""")
    return formatted_data


