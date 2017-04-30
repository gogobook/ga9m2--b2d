1. user帳號的管理主要使用customer下的abstract_models.py進行的，因此要研究這個檔案，以進行開發。
1. from django.contrib.auth import models as auth_models的BaseUserManager，被UserManager繼承，進行開發；而AbstractUser則繼承了AbstractBaseUser，並且使用了 `USERNAME_FIELD='email'`，override USERNAME\_FIELD，這應該是為什麼可以使用email做為使用者帳號的原因。
1. 根據wagtail的要求，


> User accounts

> Superuser accounts receive automatic access to the Wagtail admin interface; use ./manage.py createsuperuser if you don’t already have one. Custom user models are supported, with some restrictions; Wagtail uses an extension of Django’s permissions framework, so your user model must at minimum inherit from AbstractBaseUser and PermissionsMixin.
django-oscar應該是有符合要求。
1. 剩下的部份就是把wagtail整合進來了。
1. 要錄一個操作流程的影片。

