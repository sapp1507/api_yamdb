
[![Typing SVG](https://readme-typing-svg.herokuapp.com?center=true&multiline=true&lines=%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%BD%D1%8B%D0%B9+%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82+%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%82%D0%BE%D0%B2+;%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81+%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC%D0%B0+(29+%D0%BA%D0%BE%D0%B3%D0%BE%D1%80%D1%82%D0%B0))](https://git.io/typing-svg)
## Это <span style="color:darkred">Ya</span>mdb. Данный портал собирает отзывы пользователей на различные книги, фильмы и музыку.
###Как запустить проект на своей машине:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:sapp1507/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Как работать с порталом:
Аутентификация происходит следующим образом:

> Отправляем POST запрос на эндпоинт ***/api/v1/auth/signup/*** в виде JSON свои логин и email.
Пример:
```
    {
        "username": "username",
        "email": "email@yamdb.com"
    }
```
- На указанную почту придет ответ с кодом подтверждения
- После получения кода необходимо отправить POST запрос в виде JSON на эндпоинт ***/api/v1/auth/token/*** с указанием логина и кода подтверждения. Пример:
```
    {
        "username": "username",
        "confirmation_code": "6g3 2208352adff8cbc627b0"
    }
```
- Токен вернётся в поле access.
- Если ваш токен утрачен, украден или каким-то иным образом скомпрометирован, вам необходимо повторить процедуру получения нового токена.
- Этот токен также надо будет передавать в заголовке каждого запроса, в поле Authorization. Перед самим токеном должно стоять ключевое слово Bearer и пробел.

### Примеры запросов:
```
Получить список произведений: GET запрос на эндпоинт 
/api/v1/titles/
```
```
Посмотреть отзывы к произведению: GET запрос на эндпоинт 
/api/v1/titles/{title_id}/reviews/
```
```
Посмотреть комментарии к отзыву: GET запрос на эндпоинт 
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
Оставить отзыв к произведению: POST запрос с обязательными полями 
"text"(текст отзыва) и "score"(оценка произведения от 1 до 10)(не забываем про токен) на эндпоинт 
/api/v1/titles/{title_id}/reviews/
```
####Полный функционал API и примеры запросов можно посмотреть в браузере в документации по адресу http://127.0.0.1:8000/redoc/

---
***Выполнили [Никита Ильин](https://github.com/ilinne), [Алексей Лагунов](https://github.com/sapp1507/) и [Потапов Яков](https://github.com/potapovjakov) при поддержке [Яндекс Практикума](https://practicum.yandex.ru/)***
