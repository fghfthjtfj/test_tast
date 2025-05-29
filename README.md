Платформа обмена вещами (бартерная система)

Инструкция по установке и запуску

1.Клонируйте репозиторий

git clone https://github.com/fghfthjtfj/test_tast.git

2.Создайте виртуальное окружение и активируйте его

На Windows: python -m venv venv .\venv\Scripts\activate

На Linux: python -m venv venv source venv/bin/activate

3.Установите зависимости:

pip install -r requirements.txt

4.Запуск приложения

Выполните миграции (при использовании нового файла db.sqlite) python manage.py migrate

Создайте суперпользователя или используйте существуюзего (admin 123456) python manage.py createsuperuser

Запустите сервер python manage.py runserver

Тестирование python manage.py test
