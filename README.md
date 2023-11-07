# API Yatube

## REST API социальной сети Yatube.

В проекте используется JWT-аутентификация.

Неаутентифицированные пользователи могут просматривать группы, посты и комментарии к ним.

Аутентифицированные пользователи могут создавать, редактировать, удалять свои посты и комментарии, а так же подписываться на авторов постов.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Artem-Barsukov/api_final_yatube.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Примеры запросов.
Пример POST-запроса с токеном Admin. Создание нового поста.

POST /api/v1/posts/
```
{
    "text": "Новый пост",
    "group": 1
}
```
Пример ответа:
```
{
    "id": 1,
    "author": "Admin",
    "text": "Новый пост",
    "pub_date": "2023-11-24T14:15:22Z",    
    "image": null,
    "group": 1,    
} 
```
Пример POST-запроса с токеном Admin. Создаем комментарий к посту с id=2.

POST /api/v1/posts/2/comments/
```
{
    "text": "Новый комментарий."
} 
```
Пример ответа:
```
{
    "id": 1,
    "author": "Admin",
    "text": "Новый комментарий.",      
    "created": "2023-11-24T14:15:22Z",
    "post": 2
} 
```
