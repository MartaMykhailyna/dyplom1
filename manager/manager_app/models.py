from django.db import models
from enum import Enum
# from django.contrib.postgres.fields import ArrayField

class Order_status(Enum):
    accepted = 'Прийнято'
    paid = 'Оплачено'
    in_processing = 'В обробці'
    shipped = 'Відправлено'
    delivered = 'Доставлено'
    paid_to_dropper = 'Оплачено поставнику'  
    
class User_role(Enum):
    administartor = 'administartor'
    user = 'user'
       
# class ShoeSize(models.Model):
#     size = models.IntegerField()  
     
class Shoes(models.Model):
    id_shoes = models.AutoField(primary_key=True, unique=True)
    sh_name = models.CharField(max_length=255)
    sh_model = models.CharField(max_length=255)
    sh_size = models.IntegerField(null=False, default=38)
    sh_color = models.CharField(max_length=255)
    sh_manufacturer = models.CharField(max_length=255, blank=True, null=True)
    sh_count = models.IntegerField(null=False, default=1)
    sh_price = models.DecimalField(max_digits=10, decimal_places=2)
    sh_image = models.FileField(blank=False)  # Якщо використано bytea, можна використати BinaryField
    
    class Meta:
        db_table = 'shoes'
        managed = False

class ShoesImages(models.Model):
    item = models.ForeignKey(Shoes, related_name='images', on_delete=models.CASCADE)
    images = models.FileField(upload_to='images/')
    is_first = models.BooleanField(default=False)
    is_second = models.BooleanField(default=False)
    
    def __str__(self):
        return self.item.id_shoes
    
class Users(models.Model):
    id_user = models.IntegerField(primary_key=True)
    u_username = models.CharField(max_length=255)
    u_name = models.CharField(max_length=255)
    u_surname = models.CharField(max_length=255)
    u_email = models.CharField(max_length=255, blank=True, null=True)
    u_phone = models.CharField(max_length=13)
    u_status = models.BooleanField(default=False)
    u_role = models.CharField(max_length=45,default=User_role.user.name, choices=[(user_role.value, user_role.name) for user_role in User_role])
    
    class Meta:
        db_table = 'users'
    
class Orders(models.Model):
    id_order = models.AutoField(primary_key=True)
    o_shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, db_column='o_shoes')
    o_count = models.IntegerField(null=False, default=1)
    o_sum = models.DecimalField(max_digits=10, decimal_places=2)
    o_recipient = models.CharField(max_length=45, null=False, default='Name,Surname')
    o_address = models.CharField(max_length=100, null=False, default='Address')
    o_comment=models.CharField(max_length=100, null=True)
    o_status = models.CharField(max_length=45, default=Order_status.accepted.value, choices=[(status.value, status.name) for status in Order_status])    
    o_user = models.ForeignKey(Users, on_delete=models.CASCADE, null = True, db_column='o_user')
    
    class Meta:
        db_table = 'orders'
       
       
class Reservations(models.Model):
    id_reservation = models.AutoField(primary_key=True)
    r_shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, db_column='r_shoes')
    r_count = models.IntegerField(null=False, default=1)
    r_start_date = models.DateTimeField(auto_now_add=True)
    r_end_date = models.DateTimeField()
    r_user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='r_user')
    
    class Meta:
        db_table = 'reservations'
        
        