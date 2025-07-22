from django.db import models
from django.contrib.auth.models import User

class Departments(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    ADM = 'ADM'
    TECH = 'TECH'
    POSTS = [
        (ADM, 'Администратор'), (TECH, 'Техник')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    post = models.CharField(max_length=50, choices=POSTS, null=True, blank=True, default=TECH)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True, blank=True)

    def get_department_name(self):
        return self.department.name

class Cartridge_Models(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

class Cartridges(models.Model):
    model = models.ForeignKey(Cartridge_Models, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Departments, related_name='Cartridges_department_id', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_of_last_location = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model.name} (ID_{self.pk})"

class Cartridges_History(models.Model):
    cartridge = models.ForeignKey(Cartridges, related_name='Cartridges_history_cartridge_id', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='Cartridges_history_user_id', null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, related_name='Cartridges_history_department_id', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cartridge.model.name} (ID_{self.cartridge.primary_key})"

class Printers(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name

class Cartridges_Printers(models.Model):
    cartridge_model = models.ForeignKey(Cartridge_Models, related_name='Cartridges_Printers_cartridge_model_id', on_delete=models.SET_NULL, null=True, blank=True)
    printer = models.ForeignKey(Printers, related_name='Cartridges_Printers_printer_id', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.cartridge.model.name