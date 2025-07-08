# BarterMarket
## Описание
BarterMarket проект, позволяющий пользователям обмениваться вещами.

## Руководство по запуску
Клонируйте репозиторий
```
git clone git@github.com:V0yager01/barterMarket.git
```

### Подготовка виртуального окружения
Создаем окружениe для проекта
```
python -m venv venv
```
Устанавливаем зависимости
```
pip install -r requirements.txt
```
### Подготовка django
Переходим в директорию проекта
```
cd BarterApp/
```
Выполняем миграции
```
python manage.py migrate
```
Создаем суперпользователя
```
python manage.py createsuperuser
```
Запускаем сервер
```
python manage.py runserver
```
Заходим в админ-панель и по адрему http://127.0.0.1:8000/admin/ads/category/add/ добавляем категории для объявлений.

![image](https://github.com/user-attachments/assets/c848a553-923b-4522-916d-00cd6cb49016)
![image](https://github.com/user-attachments/assets/6b270c5e-36f9-4800-88f5-0d71a539d0d2)


