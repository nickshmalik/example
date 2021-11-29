# Install
Сохранить проект, создать виртуально окружение.

В settings.py настроить databases 


	pip install -r requirements.txt
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver


# Settings
Отправка почты:
В файле sendmail.py изменить

		server = 'SMTP'
		user = 'login'
		password = 'passwoer'
