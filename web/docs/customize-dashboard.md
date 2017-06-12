## 資料
主要依頼官方文件，另github可以找到Django Oscar Wagtail的一個開發文件，當然source code 也一資料來源。

## 源頭

```python
class Application(object):
    """
    Base application class.

    This is subclassed by each app to provide a customisable container for an
    app's views and permissions.
    """
```
位於oscar.core.application 的 `class Application` 是oscar application的總線頭，包括`DashboardApplication`；  
做為總線頭，`Application` 非常的像抽象類別，並沒有定義太多具體屬性與方法，僅是名稱。
**屬性**
```python
    #: Namespace name
    name = None

    login_url = None

    #: A name that allows the functionality within this app to be disabled
    hidable_feature_name = None

    #: Maps view names to lists of permissions. We expect tuples of
    #: lists as dictionary values. A list is a set of permissions that all
    #: needto be fulfilled (AND). Only one set of permissions has to be
    #: fulfilled (OR).
    #: If there's only one set of permissions, as a shortcut, you can also
    #: just define one list.
    permissions_map = {}

    #: Default permission for any view not in permissions_map
    default_permissions = None
```
**方法**
```python
    def __init__(self, app_name=None, **kwargs): # 建構子
    def get_urls(self):                          # 取得urls
    def post_process_urls(self, urlpatterns):    # urls後處理
    def get_permissions(self, url):              # 權限管理
    def get_url_decorator(self, pattern):        # url 裝飾器

    @property
    def urls(self):
        # We set the application and instance namespace here
        # 最主要的產出就是urls, 而這也是一個Web application的主體。因此這非常棒\且明確\且聰明。
        return self.get_urls(), self.app_name, self.name
```
## app and apps
`Application` 子類化的程式碼主要放於app.py，而原來的django apps.py則改名為config.py

## src/oscar/__init__.py
這是整個 oscar 專案的總出口，定義二個東西。
1. `OSCAR_CORE_APPS=['所有的oscar_apps']`  # 這裡放著所有的oscar apps 的字串，給`def get_core_apps(overrides=None):`用
2. `def get_core_apps(overrides=None):`   # 這個給`INSTALL_APPS` 用，並且作為override app的載入點。

## 動態載入 
在`oscar\core\loading` 中的`def get_classes()`。  

## partner
~~看來只讓user 的partner=True即可讓一般使用者能夠使用dashboard的功能了。~~  
~~我們必須子類化`AbstractPartner`，然後override，根據官方文件`docs/source/internals/getting_started.rst`~~
預設在dashboard中可以產生partner的實例。  
`AbstractPartner`與 `Users`是一個多對多的關係，當然這種多對多關係是不用在Users端定義什麼，一切由`AbstractPartner`說了算。  
在看過`oscar\apps\dashboard\`中的程式碼，`dashboard`的確可以獨立處理`partner`的問題，但這得用手工將使用者處理成供貨商，  
我們得要自動化，在程式碼就把這整件事處理好。
目前我們要試客製化的partner，讓partner與user的關係是1對1，而不是多對多，然後在建user時就把partner建好。  
另外還有一些細節要注意，供貨商可能需統編\客戶管理\消費\票卷或儲值

測試:將user加入
```python
    class Meta:
        permissions = (('partner.dashboard_access', 'Can access dashboard'), )
      
```
~~這樣就應該可以讓普通使用者，可以上架商品。~~ -> 不行，我們必須使用`partner`。我們勢必得仔細思考供貨商的角色，  
特別是現在我們得子類化`AbstractPartner`
```
Controlling visibility per user
By setting 'access_fn' for a node, you can specify a function that will get called with the current user. The node will only be displayed if that function returns True. If no 'access_fn' is specified, OSCAR_DASHBOARD_DEFAULT_ACCESS_FUNCTION is used.
```

```
Creating product classes and fulfillment partners
=================================================

Every Oscar deployment needs at least one
:class:`product class <oscar.apps.catalogue.abstract_models.AbstractProductClass>`
and one
:class:`fulfillment partner <oscar.apps.partner.abstract_models.AbstractPartner>`.
These aren't created automatically as they're highly specific to the shop you
want to build.

When managing your catalogue you should always use the Oscar dashboard, which provides the necessary functionality. Use your Django superuser email and password to login to: http://127.0.0.1:8000/dashboard/ and create instances of both there.



```
