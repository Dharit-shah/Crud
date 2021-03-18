from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _


class Employee(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=15)
    class Meta:
        db_table = "employee"

    def __str__(self):
        return self.fname + ' ' + self.lname


class Product(models.Model):
    user_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="product", blank=True, null=True)
    name = models.CharField(max_length=100)
    categry = models.CharField(max_length=100)

    class Meta:
        db_table = "product"
    def __str__(self):
        return self.user_id

class Hello(CMSPlugin):
    guest_name = models.CharField(max_length=50, default='Guest')

class Employee_Custom_Plugin(CMSPlugin):
    items_per_page = models.PositiveIntegerField(
        verbose_name= _('Items per page'),
        null=False,
        blank=False,
        help_text= _('Show number of items per page'),
        default=0
    )
    def __str__(self):
        return str(self.items_per_page)


class Product_Custom_Plugin(CMSPlugin):
    items_per_page = models.PositiveIntegerField(
        verbose_name= _('Items per page'),
        null=False,
        blank=False,
        help_text= _('Show number of items per page'),
        default=0
    )
    def __str__(self):
        return str(self.items_per_page)


