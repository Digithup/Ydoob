from ckeditor_uploader.fields import RichTextUploadingField
from currencies.models import Currency
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User, AbstractUser, Permission, Group
from django.db.models.manager import EmptyManager
from django.utils.safestring import mark_safe
from django.utils.text import slugify

Type = (
    ('1', 'Home'),
    ('2', 'Business'),

)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None, is_active=True, is_staff=False
                    , is_seller=False,
                    is_admin=False, is_customer=True, ):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user_obj.set_password(password)
        user_obj.customer = is_customer
        user_obj.seller = is_seller
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_customer(self, email, first_name=None, last_name=None, password=None):
        return self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,

        )

    def create_seller(self, email, first_name=None, last_name=None, password=None, ):
        return self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_seller=True,
            is_staff=True,
        )

    def create_staff_user(self, email, first_name=None, last_name=None, password=None):
        return self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
        )

    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        return self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )


class User(AbstractBaseUser):
    """
    Description:This is going to be the main User Model
    """
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=20)
    image = models.ImageField(upload_to='images/Users/%y/%m',
                              default='images/dashboard-bases/man.png')
    facebook = models.URLField(blank=True, max_length=50)
    instagram = models.URLField(blank=True, max_length=50)
    twitter = models.URLField(blank=True, max_length=50)
    youtube = models.URLField(blank=True, max_length=50)
    about = RichTextUploadingField(blank=True)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    customer = models.BooleanField(default=True)
    seller = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group,blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.email)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address or full name
        if self.first_name:
            return self.first_name
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission?
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_customer(self):
        # "Is the user a member of staff?"
        return self.customer

    @property
    def is_seller(self):
        # "Is the user a member of staff?"
        return self.seller

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        # "Is the user an admin member?"
        return self.admin

    # @property
    # def is_active(self):
    #     "Is the user active?"
    #     return self.active

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


class UserAddress(models.Model):
    address_title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(blank=True, null=True, max_length=150)
    governorate = models.CharField(blank=True, null=True, max_length=150)
    city = models.CharField(blank=True, null=True, max_length=20)
    area = models.CharField(blank=True, null=True, max_length=50)
    street_name = models.CharField(blank=True, null=True, max_length=150)
    location_type = models.CharField(max_length=10, choices=Type)
    phone = models.CharField(blank=True, null=True, max_length=150)
    country = models.CharField(blank=True, null=True, max_length=50)
    shipping_note = models.CharField(blank=True, null=True, max_length=255)
    building_name = models.CharField(blank=True, null=True, max_length=255)
    floor_no = models.CharField(blank=True, null=True, max_length=255)
    apartment_no = models.CharField(blank=True, null=True, max_length=255)
    nearest_landmark = models.CharField(blank=True, null=True, max_length=255)
    postal_code = models.CharField(blank=True, null=True, max_length=50)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]
        verbose_name_plural = "Shipping Address"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.address_title)
        super(UserAddress, self).save(*args, **kwargs)

    def __str__(self):
        return self.address_title


class GuestEmail(models.Model):
    '''
    Description:Hold the details of a guest user.\n
    '''
    email = models.EmailField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Guest User'
        verbose_name_plural = 'Guest Users'
        ordering = ['-timestamp']
