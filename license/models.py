from django.db import models

# Create your models here.


class Customer(models.Model):

	company = models.CharField("Компания:", max_length=50)
	firstname = models.CharField("Имя:", max_length=50)
	lastname = models.CharField("Фамилия:", max_length=50)
	email = models.CharField("e-mail:", max_length=50)
	
	class Meta:
		verbose_name = "Заказчик"
		verbose_name_plural = "Заказчики"
    
	def __str__(self):  
		return self.company

class License(models.Model):

	customer = models.ForeignKey(Customer, verbose_name="Заказчик", on_delete=models.SET_NULL, blank=True, null=True)
	license = models.CharField("Закуплно:", max_length=6)
	red = models.CharField("Ошибки:", max_length=6)
	green = models.CharField("Работает:", max_length=6)
	grey = models.CharField("Серые:", max_length=6)
	date = models.DateField("Дата:", blank=True, null=True)


	class Meta:
		verbose_name = "Сервис"
		verbose_name_plural = "Сервисы"
		#ordering = ['customer']

	def __str__(self):
		return str(self.customer)
		
