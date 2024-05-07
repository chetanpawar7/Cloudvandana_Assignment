from django.db import models
from django.contrib.auth.models import User
from master.models import CompanyMaster,DepoMaster


checklist_type_choice=(
        ('daily','daily'),
        ('pit','pit')
    )
     
class RoleMaster(models.Model):
    role_name=models.CharField(max_length=100)
    role_desc=models.CharField(max_length=200,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='depo_role_master'
        
class UserMaster(models.Model):
    user_code=models.CharField(unique=True,max_length=30,blank=True,null=True)
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    mobile_no=models.CharField(max_length=15,blank=True,null=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    city=models.CharField(max_length=20,null=True,blank=True)
    district=models.CharField(max_length=20,null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comapny=models.ForeignKey(CompanyMaster,on_delete=models.CASCADE)
    depo=models.ForeignKey(DepoMaster,on_delete=models.CASCADE)
    role=models.ForeignKey(RoleMaster,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='depo_user_master'

    