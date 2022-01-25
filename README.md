## Сервис учёта инвестиционных активов пользователя

### Ключевые возможности

* Регистрация / логин пользователей.
* Возможности пользователя:
    - Добавлять актив из списка (используя название компании или ticker).
    - Редактировать актив (количество).
    - Удалять актив.
    - Импортировать активы из файла(из выгрузки брокера или csv).
    - Кнопка `Обновить курсы активов` (принять во внимание, что имеются [ограничения](https://tinkoff.github.io/investAPI/limits/) API).

Проект реализован с использованием [investAPI от Тинькофф](https://github.com/Tinkoff/investAPI). Это более новое и функциональное API, чем [invest-openapi](https://github.com/Tinkoff/invest-openapi).


### Установка приложения

* Активировать виртуальное окружение
```sh
python3 -m venv env
source ./env/bin/activate
```

* Создать конфигурационный файл, `SECRET_KEY` - длинная строка случайных символов:
```sh
cp webapp/template_config.py webapp/config.py
```
* Получить [токен](https://tinkoff.github.io/investAPI/token/) для песочницы с [сайта Tinkoff](https://www.tinkoff.ru/invest/) и добавить его в `webapp/config.py` как константу `API_TOKEN`

* Установить зависимости:
```sh
pip install -r requirements.txt
```

* Запустить скрипты создания базы и наполнения данными:
```sh
./initdb.sh
python create_data.py
python create_admin.py
```

* Запустить приложение в отладочном режиме:
```sh
./run.sh
```
* Проверить доступность на [localhost:5000](http://localhost:5000/)
