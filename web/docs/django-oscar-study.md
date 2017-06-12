1. user帳號的管理主要使用customer下的abstract_models.py進行的，因此要研究這個檔案，以進行開發。
1. from django.contrib.auth import models as auth_models的BaseUserManager，被UserManager繼承，進行開發；而AbstractUser則繼承了AbstractBaseUser，並且使用了 `USERNAME_FIELD='email'`，override USERNAME\_FIELD，這應該是為什麼可以使用email做為使用者帳號的原因。
1. 根據wagtail的要求，


> User accounts

> Superuser accounts receive automatic access to the Wagtail admin interface; use ./manage.py createsuperuser if you don’t already have one. Custom user models are supported, with some restrictions; Wagtail uses an extension of Django’s permissions framework, so your user model must at minimum inherit from AbstractBaseUser and PermissionsMixin.
django-oscar應該是有符合要求。
1. ~~剩下的部份就是把wagtail整合進來了。~~ 由於oscar有附一個簡單的CMS 模組，可能暫時不需要，但會有一個markdown載進來。
1. 
1. 要錄一個操作流程的影片。

## dashboard source code study
### 1 文件 位於 docs/source/ref/apps/dashboard.rst
### 2 source code 位於 oscar/apps/dashboard/
**dashboard** 內沒有models, 也沒有abstract models。這還滿容易理解的，dashboard不用儲存資料，dashboard的資料都是來自於其的各個類，所以dashboard內有最多的動態載入的class。似乎也是因為dashboard 的資料都是來自於其他地方，這造成了如果要客製dashboard 會有些因難。  
dashboard最主要的功能就是讓人們看資料，而看資料依賴的是views.py，以下是views.py的一部份。  

```python
from oscar.core.loading import get_model

ConditionalOffer = get_model('offer', 'ConditionalOffer')
Voucher = get_model('voucher', 'Voucher')
Basket = get_model('basket', 'Basket')
StockAlert = get_model('partner', 'StockAlert')
Product = get_model('catalogue', 'Product')
Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
User = get_user_model()
```
可以看到使用get_model大量的被使用，這就是動態載入，而且可以看到，這裡是使用字串，你甚到不需要`import`；  
同時我們也看到get\_user\_model(), 而這也是動態載入，是django自帶的動態載入。  
其中非常有趣的是`def get_number_of_promotions(self, abstract_base=AbstractPromotion)`，這裡使用抽象類別做為參數，但在程式中，使用`.__subclass__`以指向其子類。

```python
def get_number_of_promotions(self, abstract_base=AbstractPromotion):
    """
    Get the number of promotions for all promotions derived from
    *abstract_base*. All subclasses of *abstract_base* are queried
    and if another abstract base class is found this method is executed
    recursively.
    """
    total = 0
    for cls in abstract_base.__subclasses__():
        if cls._meta.abstract:
            total += self.get_number_of_promotions(cls)
        else:
            total += cls.objects.count()
    return total
```
另外`def get_hourly_report(self, hours=24, segments=10)`則是因為要繪出圖形，所以有較多的程式碼。

```python
def get_hourly_report(self, hours=24, segments=10):
    """
    Get report of order revenue split up in hourly chunks. A report is
    generated for the last *hours* (default=24) from the current time.
    The report provides ``max_revenue`` of the hourly order revenue sum,
    ``y-range`` as the labeling for the y-axis in a template and
    ``order_total_hourly``, a list of properties for hourly chunks.
    *segments* defines the number of labeling segments used for the y-axis
    when generating the y-axis labels (default=10).
    """
    # Get datetime for 24 hours agao
```
## How to customise models
### 1 文件 位於 docs/source/howto\how\_to\_customise\_models.rst
### source code 位於oscar\core\loading
### 剛剛發現有一堆code 寫在 __init__.py，搞不清楚狀況，有些受驚
### 找一下網路資料，看到這二個
在程式碼的一開始首先定義`MOVED_ITEMS = {}`，