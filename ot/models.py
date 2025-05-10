from django.db import models


# Create your models here.

class Employee(models.Model):
    firstname = models.CharField(verbose_name='Имя', max_length=255)
    lastname = models.CharField(verbose_name='Фамилия', max_length=255)
    middlename = models.CharField(verbose_name='Отчество', max_length=255, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=255)
    snils = models.CharField(verbose_name='СНИЛС', max_length=11, blank=True)
    birth = models.DateField(verbose_name='Дата рождения')
    serial = models.CharField(verbose_name='Серия паспорта', max_length=20, blank=True)
    number = models.CharField(verbose_name='Номер паспорта', max_length=20, blank=True)
    by = models.CharField(verbose_name='Кем выдан', max_length=255, blank=True)
    when = models.DateField(verbose_name='Дата выдачи', blank=True)
    reg_address = models.CharField(verbose_name='Адрес регистрации', max_length=255, blank=True)
    home_address = models.CharField(verbose_name='Адрес проживания', max_length=255, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20, blank=True)

    def __str__(self): 
            return f'{self.firstname} {self.lastname} {self.middlename}'


class Company(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    short_title = models.CharField(verbose_name='Сокращенное название', max_length=255)
    inn = models.CharField(verbose_name='ИНН', max_length=12)

    def __str__(self): 
            return f'{self.title}'
    
class Program(models.Model):
    title = models.CharField(verbose_name='Название программы', max_length=255)
    short_title = models.CharField(verbose_name='Краткое название программы', max_length=10)
    system_id = models.CharField(verbose_name='Системное ID', max_length=12)
    
    def __str__(self): 
            return f'{self.title}'


class Decree(models.Model):
    date = models.DateField(verbose_name='Дата', blank=True)
    number = models.CharField(verbose_name='Номер', max_length=255)
    main = models.ForeignKey(Employee, related_name="main_person", verbose_name='Председатель', on_delete=models.DO_NOTHING)
    second = models.ForeignKey(Employee,related_name="second_person", verbose_name='Второй', on_delete=models.DO_NOTHING)
    third = models.ForeignKey(Employee,related_name="third_person", verbose_name='Третий', on_delete=models.DO_NOTHING)
    
    def __str__(self): 
            return f'Приказ № {self.number} от {self.date}'