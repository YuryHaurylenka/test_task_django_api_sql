# Django API Project - Test Task

**This project was developed as part of a test task.** The full description of the technical requirements can be
found [here](https://github.com/YuryHaurylenka/test_task_django_api_sql/blob/main/test_task_eng.md).
This project is a Django-based API designed for managing users, links, and collections, with
capabilities for fetching
Open Graph metadata and categorizing links. The system supports user registration, authentication using JWT tokens, and
features for creating and managing collections of various link types (e.g., music, book, article, video). Additionally,
the project includes an **SQL task** for identifying the top 10 users who have saved the most links.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#example-env-file)
    - [Explanation of variables](#explanation-of-environment-variables)
    - [Instruction for email password](#detailed-instructions-for-email_host_password)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Generating Sample Data](#generating-sample-data)
- [SQL Task](#sql-task)
- [Admin Panel and Email Setup](#admin-panel)
- [License](#license)

---

## Features

- User registration, login, and authentication using JWT tokens.
- Password reset functionality with verification code (code expires after 30 minutes, a new request invalidates the
  previous one).
- Fetches and stores Open Graph metadata from provided URLs.
- Categorizes links into various types (e.g., music, book, article, video).
- Create, view, and manage collections of links.
- Admin panel for managing users, links, and collections.
- CSV file generation for the top 10 users with the most links.
- Swagger UI for interactive API documentation and testing.

## Requirements

- Python 3.12
- Django 5.0
- Django REST Framework
- Djoser for authentication
- Django REST Framework SimpleJWT
- drf-yasg for API documentation
- Docker & Docker Compose
- PostgreSQL

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YuryHaurylenka/test_task_django_api_sql.git
   cd test_task_django_api_sql
   ```

2. **Create a `.env` file**:
   Copy the contents of `.env.example` to a new `.env` file and adjust the environment variables as needed.

## Example `.env` File

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=db_test
POSTGRES_USER=user_test
POSTGRES_PASSWORD=password_test
DB_HOST=db
DB_PORT=5432
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app_specific_password
SECURE_SSL_REDIRECT=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
```

### Explanation of Environment Variables

- **`SECRET_KEY`**: A unique secret key used by Django for cryptographic signing. Keep this secure.
- **`DEBUG`**: Enables or disables debug mode. Set to `True` for development and `False` for production.
- **`ALLOWED_HOSTS`**: A comma-separated list of domains or IP addresses that the application can serve.  
  Example: `localhost,127.0.0.1`.
- **`POSTGRES_DB`**: Name of your PostgreSQL database.
- **`POSTGRES_USER`**: Username for connecting to your PostgreSQL database.
- **`POSTGRES_PASSWORD`**: Password for the PostgreSQL user.
- **`DB_HOST`**: Hostname where your PostgreSQL database is running (use `db` if running in Docker).
- **`DB_PORT`**: Port for your PostgreSQL database (default is `5432`).
- **`ACCESS_TOKEN_LIFETIME_MINUTES`**: Lifetime of the JWT access token in minutes.
- **`REFRESH_TOKEN_LIFETIME_DAYS`**: Lifetime of the JWT refresh token in days.
- **`EMAIL_HOST_USER`**: The email address used to send emails (e.g., password reset emails).
- **`EMAIL_HOST_PASSWORD`** [Instruction](#detailed-instructions-for-email_host_password).
- **`SECURE_SSL_REDIRECT`**: If set to `True`, all HTTP requests will be redirected to HTTPS.
- **`CSRF_COOKIE_SECURE`** & **`SESSION_COOKIE_SECURE`**: Ensures that cookies are only sent over HTTPS. Set to `False`
  in development.

---

### Detailed Instructions for `EMAIL_HOST_PASSWORD`

To securely use Gmail for sending emails (such as password resets), you need to generate an **app-specific password**
instead of using your regular Gmail password. Google enforces this for security, especially if 2-Step Verification is
enabled.

#### How to Generate an App-Specific Password:

1. **Enable 2-Step Verification** on your Google account (if not already enabled).
   Visit [Google Account Security](https://myaccount.google.com/security) to set it up.

2. **Generate an App Password**:
    - Go to [Google Account Security](https://myaccount.google.com/security).
    - Find **App passwords** and click on it.
    - You might need to log in again for security.
    - Select **Other (Custom name)**, enter a name (e.g., "Django App"), and click **Generate**.
    - Copy the 16-character password that is generated and paste it to .

## Running the Project

1. **Build and run the containers**:
   ```bash
   docker-compose up --build -d
   ```

2. **Access the application**:
    - App: [http://localhost:8000](http://localhost:8000)
    - Admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)
    - Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### Admin Panel

To access the admin panel, visit `/admin`.

Upon build, a superuser is automatically created with the following credentials:

- **Email**: `admin@example.com`
- **Password**: `adminpassword`

## API Endpoints

Below are the most important API endpoints available in this project. Note that all operations related to **links** and
**collections** are only accessible to authenticated users.

### **User Registration**

- **Endpoint**: `POST /auth/register/`  
  Allows new users to register using an email and password.

### **User Login**

- **Endpoint**: `POST /auth/login/`  
  Authenticates users and returns a JWT token.

### **Password Reset Request**

- **Endpoint**: `POST /auth/users/reset_password/`  
  Sends a password reset code to the user's email. If a new code is requested, the previous one is invalidated.

### **Password Reset Confirmation**

- **Endpoint**: `POST /auth/users/reset_password_confirm/`  
  Confirms the reset code and allows the user to set a new password.

### **Create a New Link**

- **Endpoint**: `POST /api/links/`  
  Creates a new link using a provided URL, automatically fetching Open Graph metadata. Available only to authenticated
  users.

### **View User's Links**

- **Endpoint**: `GET /api/links/`  
  Retrieves a list of all links created by the authenticated user.

### **Create a New Collection**

- **Endpoint**: `POST /api/collections/`  
  Allows the user to create a new collection with a title and optional description. Available only to authenticated
  users.

## Generating Sample Data

To generate test users and links, use the script:

```bash
docker-compose exec web python generate_data.py
```

## SQL Task

There is an API endpoint available at `/api/users/top-users/` that executes the SQL script located in the root directory
under the filename `top_users.sql`. Before testing, you can generate sample users and links using
the [script](#generating-sample-data)

### How it works:

- The SQL script finds the **top 10 users** with the most saved links.
- If multiple users have the same number of links, it prioritizes users by their registration date (earlier
  registrations come first).
- The query also counts the different types of links saved by each user (e.g., website, book, article, music, video).

The endpoint performs the following:

1. Executes the SQL query from the `top_users.sql` file.
2. Fetches the data and returns the results through the API.
3. Additionally, the results are saved in a CSV file named `top_users_output.csv` located in the project's root
   directory.

## License

This project is licensed under
the [MIT License](https://github.com/YuryHaurylenka/test_task_django_api_sql/blob/main/LICENSE).


---

### Author

[Yury Haurylenka](https://github.com/YuryHaurylenka)

---

# RU

**Этот проект является тестовым заданием.** Полное описание Технического Задания (ТЗ)
доступно [здесь](https://github.com/YuryHaurylenka/test_task_django_api_sql/blob/main/test_task_ru.md).
Этот проект представляет собой API на основе Django для управления пользователями, ссылками и коллекциями с возможностью
получения метаданных Open Graph и категоризации ссылок. Система поддерживает регистрацию пользователей, аутентификацию с
использованием JWT токенов и включает функции для создания и управления коллекциями различных типов ссылок (например,
музыка, книги, статьи, видео). Также дополнительно, проект содержит **SQL задание** для определения топ-10
пользователей, которые сохранили наибольшее количество ссылок.

## Содержание

- [Функциональность](#функциональность)
- [Требования](#стек)
- [Установка](#установка)
- [Переменные окружения](#пример-файла-env)
    - [Объяснение переменных окружения](#объяснение-переменных-окружения)
    - [Инструкция по настройке email](#инструкция-по-настройке-email_host_password)
- [Запуск проекта](#запуск-проекта)
- [API эндпоинты](#api-эндпоинты)
- [Генерация тестовых данных](#генерация-тестовых-данных)
- [SQL задача](#sql-задание)
- [Админка и настройка Email](#админка)
- [Лицензия](#лицензия)

## Функциональность

- Регистрация пользователей, вход и аутентификация через JWT токены.
- Сброс пароля с использованием кода подтверждения (код истекает через 30 минут; новый запрос аннулирует предыдущий
  код).
- Получение и сохранение метаданных Open Graph из предоставленных URL.
- Категоризация ссылок по типам (например, музыка, книга, статья, видео).
- Создание, просмотр и управление коллекциями ссылок.
- Админка для управления пользователями, ссылками и коллекциями.
- Генерация CSV файла для топ-10 пользователей с наибольшим количеством ссылок.
- Swagger UI для интерактивного тестирования и документации API.

## Стек

- Python 3.12
- Django 5.0
- Django REST Framework
- Djoser для аутентификации
- Django REST Framework SimpleJWT
- drf-yasg для документации
- Docker и Docker Compose
- PostgreSQL

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/YuryHaurylenka/test_task_django_api_sql.git
   cd test_task_django_api_sql
   ```

2. **Создайте файл `.env`**:
   Скопируйте содержимое `.env.example` в новый файл `.env` и настройте переменные окружения.

## Пример файла `.env`

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=db_test
POSTGRES_USER=user_test
POSTGRES_PASSWORD=password_test
DB_HOST=db
DB_PORT=5432
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app_specific_password
SECURE_SSL_REDIRECT=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
```

### Объяснение переменных окружения

- **`SECRET_KEY`**: Уникальный секретный ключ, используемый Django.
- **`DEBUG`**: Включает или отключает режим отладки. Установите `True` для разработки.
- **`ALLOWED_HOSTS`**: Список доменов или IP-адресов, которым разрешено обращаться к приложению.  
  Пример: `localhost,127.0.0.1`.
- **`POSTGRES_DB`**: Название базы данных PostgreSQL.
- **`POSTGRES_USER`**: Имя пользователя для подключения к базе данных PostgreSQL.
- **`POSTGRES_PASSWORD`**: Пароль для пользователя базы данных PostgreSQL.
- **`DB_HOST`**: Имя хоста, где запущена база данных PostgreSQL (используйте `db` для Docker).
- **`DB_PORT`**: Порт для базы данных PostgreSQL (по умолчанию `5432`).
- **`ACCESS_TOKEN_LIFETIME_MINUTES`**: Время жизни JWT access токена в минутах.
- **`REFRESH_TOKEN_LIFETIME_DAYS`**: Время жизни JWT refresh токена в днях.
- **`EMAIL_HOST_USER`**: Email-адрес, используемый для отправки писем (для сброса пароля).
- **`EMAIL_HOST_PASSWORD`** [Инструкция](#инструкция-по-настройке-email_host_password).
- **`SECURE_SSL_REDIRECT`**: Ставим `False`. Если установлено в `True`, все HTTP-запросы будут перенаправляться на
  HTTPS).
- **`CSRF_COOKIE_SECURE`** и **`SESSION_COOKIE_SECURE`**: Обеспечивает отправку cookie только по HTTPS.
  Установите `False` в режиме разработки.

### Инструкция по настройке `EMAIL_HOST_PASSWORD`

1. **Включите двухэтапную аутентификацию** на вашем аккаунте Google. Перейдите
   по [ссылке](https://myaccount.google.com/security).

2. **Создайте пароль приложения**:
    - Перейдите на страницу [безопасности аккаунта](https://myaccount.google.com/security).
    - Найдите раздел **Пароли приложений**.
    - Выберите **Другое (настраиваемое имя)**, введите "Django App" и нажмите **Создать**.
    - Скопируйте сгенерированный 16-значный пароль и добавьте его в `.env` файл в EMAIL_HOST_PASSWORD.

## Запуск проекта

1. **Соберите и запустите контейнеры**:
   ```bash
   docker-compose up --build -d
   ```

2. **Доступ к приложению**:
    - Приложение: [http://localhost:8000](http://localhost:8000)
    - Админка: [http://localhost:8000/admin](http://localhost:8000/admin)
    - Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### Админка

Для доступа к админ-панели используйте `/admin`.

При сборке автоматически создаётся суперпользователь со следующими данными:

- **Email**: `admin@example.com`
- **Пароль**: `adminpassword`

## API эндпоинты

### **Регистрация пользователя**

- **Endpoint**: `POST /auth/register/`

### **Вход пользователя**

- **Endpoint**: `POST /auth/login/`

### **Запрос на сброс пароля**

- **Endpoint**: `POST /auth/users/reset_password/`

### **Подтверждение сброса пароля**

- **Endpoint**: `POST /auth/users/reset_password_confirm/`

### **Создание новой ссылки**

- **Endpoint**: `POST /api/links/`

### **Просмотр ссылок пользователя**

- **Endpoint**: `GET /api/links/`

### **Создание новой коллекции**

- **Endpoint**: `POST /api/collections/`

## Генерация тестовых данных

Используйте скрипт для генерации тестовых данных:

```bash
docker-compose exec web python generate_data.py
```

## SQL Задание

Доступен API эндпоинт `/api/users/top-users/`, который выполняет SQL скрипт, расположенный в корневой директории под
названием `top_users.sql`. Перед использованием, вы можете сгенерировать тестовых пользователей и ссылки с
помощью [скрипта](#генерация-тестовых-данных).

### Как это работает:

- SQL скрипт находит **топ-10 пользователей** с наибольшим количеством сохранённых ссылок.
- Если у нескольких пользователей одинаковое количество ссылок, приоритет отдаётся более ранней дате регистрации.
- Запрос также подсчитывает количество различных типов сохранённых ссылок (например, сайт, книга, статья, музыка,
  видео).

Эндпоинт выполняет следующие действия:

1. Выполняет SQL запрос из файла `top_users.sql`.
2. Извлекает данные и возвращает результаты через API.
3. Дополнительно сохраняет результаты в CSV файл под названием `top_users_output.csv`, который находится в корневой
   директории проекта.

## Лицензия

Проект лицензирован под [MIT Лицензией](https://github.com/YuryHaurylenka/test_task_django_api_sql/blob/main/LICENSE)..

### Автор

[Yury Haurylenka](https://github.com/YuryHaurylenka)
