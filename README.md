# Проект ИС для "Движение первых"

## Описание

Проект представляет готовое решение по автоматизации процессов и решением для формирования важных документов

## Начало работы

1. Клонируйте репозиторий или скачайте архив:

    ```
    git clone https://github.com/PolinaScrbbs/The-Movement-Of-The-First.git
    ```

2. Перейдите в каталог проекта

3. Создайте виртуальное окружение:

    ```
    py -m venv .venv
    ```

5. Активируйте виртуальное окружение:

    ```
    .venv/Scripts/Activate
    ```
> Если выдает ошибку, то сначала введите `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, а потом повторите прошлую команду
5. Установите необходимые зависимости:

    ```
    pip install -r requirements.txt
    ```

6. Создайте файл `.env` (Да, это файл без имени, только расширение) в корневой директории проекта и заполните его следующими данными:

    ```
    DB_USER = {Имя пользователя БД}
    DB_PASSWORD = {Пароль пользователя в БД}
    DB_NAME = {Название БД} #Не забудьте сначала в ручную в PgAdmin создать БД
    
    SECRET_KEY = {Секретный ключ для хеширования пароля} #Любая рандомная последовательность символов
    ```

## Использование

- `alembic upgrade head` - Примените миграции, после у вас в БД появятся все нужные таблицы.

- `python -m app.main` - Эта команда запускает ваше приложение.

## Ссылки

- [Документация SQLAlchemy](https://docs.sqlalchemy.org/)
- [Документация Alembic](https://alembic.sqlalchemy.org/)
