# FastAPI Trading Results Service

FastAPI-приложение для просмотра биржевых торговых результатов (`TradeResult`) с возможностью фильтрации по разным параметрам.

---

## Возможности

- Получение динамики и истории торгов по фильтрам (ID нефти, тип доставки, база, диапазон дат)
- Удобные текстовые ответы для интеграций и мониторинга
- Асинхронный доступ к базе через SQLAlchemy

---

## Установка

1. **Клонировать репозиторий**  
```
   git clone https://github.com/ridleq/spimex_fastapi.git;
   cd simpex_fastapi
```
2. **Создать и активировать виртуальное окружение**
```
    python -m venv venv
    source venv/scrtipt/activate
```
3. **Установить зависимости**
```
    pip install -r requirements.txt
```
4. **Настроить переменные окружения**
```
    Файл .env_example поможет
```
5. **Запустить приложение**
```
    uvicorn main:app --reload
```
---

## Описание модели
**TradeResult** — главная таблица, содержит следующие поля:

- `id`
- `exchange_product_id`
- `exchange_product_name`
- `oil_id`
- `delivery_basis_name`
- `delivery_type_id`
- `volume`
- `total`
- `count`
- `date`

---
## Описание эндпоинтов

```
    GET /last-dates - список дат последних торговых дней.
    Фильтрация по кол-ву последних торговых дней /last-dates?count=4.
```
```
    GET /get-dynamics - список торгов за заданный период.

    Параметры запроса (все опциональны):
     - oil_id: str — фильтр по ID нефти
     - delivery_type_id: str — фильтр по типу доставки
     - delivery_basis_id: str — фильтр по базе поставки
     - start_date: str — фильтр по дате старта диапазона (формат: YYYY-MM-DD)
     - end_date: str — фильтр по дате конца диапазона (формат: YYYY-MM-DD)
```
```
    GET /get_trading_results - список последних торгов.
    Параметры запроса:
     - oil_id: str — фильтр по ID нефти
     - delivery_type_id: str — фильтр по типу доставки
     - delivery_basis_id: str — фильтр по базе
     - limit: int — ограничение количества записей (по умолчанию 10, максимум 100)
```
---
## Пример ответа
```
ID: 1
Product ID: A100STI060F
Product Name: Бензин (АИ-100-К5), ст. Стенькино II (ст. отправления)
Oil ID: A100
Delivery Basis: ст. Стенькино II
Volume: 120.0
Total: 8297280.0
Count: 2
Date: 2025-05-20 00:00:00
----

======================
```


## Authors

[@ridleq](https://github.com/ridleq)

