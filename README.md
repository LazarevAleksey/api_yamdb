### 1.Описание проекта:

Проект реализует API доступ к проекту YATUBE. При выполнении проекта использовался Django Rest Framework.

### 2.Примеры запросов к API:

Получить список всех жанров.
GET запрос:
```
http://127.0.0.1:8000/api/v1/genres/
```
Создать категорию.
POST запрос:
```
http://127.0.0.1:8000/api/v1/categories/
```
Тело запроса:
```
{
  "name": "string",
  "slug": "string"
}
```
### 3.Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:LazarevAleksey/api_yamdb.git
```

Cоздать виртуальное окружение:

```
python -m venv venv
```
Активировать виртуальное окружение:
```
source venv/Scripts/activate
```
Обновить установщик pip:
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
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

### 4.Контактная информация:
```Разработчик:```
Алексей Лазарев
```email:``` 
bins2504@gmail.com
