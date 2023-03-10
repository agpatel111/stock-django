from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager, MyAccountManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

Buy_status = (
    ('BUY', 'BUY'),
    ('SELL', 'SELL'),
    ('empty', 'empty'),
    )

final_status = (
    ('PROFIT', 'PROFIT'),
    ('LOSS', 'LOSS'),
    ('NA', 'NA'),
    )

call_or_put = (
    ('CALL', 'CALL'),
    ('PUT', 'PUT'),
    ('NA', 'NA'),
    )

# Create your models here.


class nse_setting(models.Model):

    option = models.CharField(max_length=50)
    profit_percentage = models.IntegerField()
    loss_percentage = models.IntegerField()
    set_pcr = models.FloatField()
    baseprice_plus = models.IntegerField()
    quantity_bn = models.FloatField(default= 1 ,null=True)

    def __str__(self):
        return self.option


    
class stock_detail(models.Model):
    
    base_strike_price = models.FloatField()
    live_Strike_price = models.FloatField()
    buy_price = models.FloatField()
    percentage = models.ForeignKey(nse_setting, on_delete=models.CASCADE)
    sell_price = models.FloatField()
    stop_loseprice = models.FloatField()
    live_brid_price = models.FloatField()
    exit_price = models.FloatField(null=True)
    buy_time = models.DateTimeField(auto_now_add= True)
    sell_buy_time = models.DateTimeField( null=True)
    status = models.CharField(max_length=50, choices=Buy_status, default='empty', blank=True)
    final_status = models.CharField(max_length=50, choices=final_status, default='NA', blank=True )
    admin_call = models.BooleanField(default=False)
    call_put = models.CharField(max_length=50, blank=True, choices=call_or_put)
    stock_name = models.TextField(null=True, blank=True)
    squareoff = models.FloatField(null=True , blank=True)
    stoploss =  models.FloatField(null=True , blank=True)
    orderid = models.FloatField(null= True)
    buy_pcr = models.FloatField(null= True)
    sell_pcr = models.FloatField(null= True)


class pcr_stock_name(models.Model):
    name = models.CharField(max_length = 100)
    pcr = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True , null=True)
    PE_CE_diffrent = models.BooleanField(default=False)
    


class live(models.Model):
    set = models.FloatField(default=0)

class dropdown_stock_name(models.Model):
    name = models.CharField(max_length = 100 )
    pcr = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True , null=True)
    PE_CE_diffrent = models.BooleanField(default=False)


class dropdown_stock_name_put(models.Model):
    name = models.CharField(max_length = 100 )
    pcr = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True , null=True)
    PE_CE_diffrent = models.BooleanField(default=False)


# class User(AbstractBaseUser):
# 	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
# 	username 				= models.CharField(max_length=30, unique=True)
# 	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
# 	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
# 	is_admin				= models.BooleanField(default=True)
# 	is_active				= models.BooleanField(default=True)
# 	is_staff				= models.BooleanField(default=False)
# 	is_superuser			= models.BooleanField(default=False)


# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['username']

# 	objects = MyAccountManager()

# 	def __str__(self):
# 		return self.email

# 	# For checking permissions. to keep it simple all admin have ALL permissons
# 	def has_perm(self, perm, obj=None):
# 		return self.is_admin

# 	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
# 	def has_module_perms(self, app_label):
# 		return True



# class User(AbstractUser):
#     username = models.CharField(max_length=30, unique=True)

#     email = models.EmailField(_('email address'), unique=True)
#     date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = = models.DateTimeField(verbose_name='last login', auto_now=True)
	
#     is_super = models.BooleanField(default=False)
#     is_owner = models.BooleanField(default=False)
#     status = models.BooleanField(default=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         return self.first_name + ' ' + self.last_name
