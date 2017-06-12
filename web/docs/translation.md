Translation
===========

All Oscar translation work is done on Transifex_. If you'd like to contribute,
just apply for a language and go ahead!
The source strings in Transifex are updated after every commit on Oscar's
master branch on GitHub. We only pull the translation strings back into Oscar's
repository when preparing for a release. That means your most recent
translations will always be on Transifex, not in the repo!

.. _Transifex: https://www.transifex.com/projects/p/django-oscar/


Translating Oscar within your project
-------------------------------------

If Oscar does not provide translations for your language, or if you want to
provide your own, do the following.

Within your project, create a locale folder and a symlink to Oscar so that
``./manage.py makemessages`` finds Oscar's translatable strings::

    mkdir locale i18n
    ln -s $PATH_TO_OSCAR i18n/oscar
    ./manage.py makemessages --symlinks --locale=de

This will create the message files that you can now translate.

### 以下為放在settings/base.py的程式碼
```python
# Includes all languages that have >50% coverage in Transifex
# Taken from Django's default setting for LANGUAGES
gettext_noop = lambda s: s
LANGUAGES = (
    # ('ar', gettext_noop('Arabic')),
    # ('ca', gettext_noop('Catalan')),
    # ('cs', gettext_noop('Czech')),
    # ('da', gettext_noop('Danish')),
    # ('de', gettext_noop('German')),
    ('en-gb', gettext_noop('British English')),
    # ('el', gettext_noop('Greek')),
    # ('es', gettext_noop('Spanish')),
    # ('fi', gettext_noop('Finnish')),
    # ('fr', gettext_noop('French')),
    # ('it', gettext_noop('Italian')),
    # ('ko', gettext_noop('Korean')),
    # ('nl', gettext_noop('Dutch')),
    # ('pl', gettext_noop('Polish')),
    # ('pt', gettext_noop('Portuguese')),
    # ('pt-br', gettext_noop('Brazilian Portuguese')),
    # ('ro', gettext_noop('Romanian')),
    # ('ru', gettext_noop('Russian')),
    # ('sk', gettext_noop('Slovak')),
    # ('uk', gettext_noop('Ukrainian')),
    ('zh-hant', gettext_noop('中文 (繁體)')),
    # ('zh-cn', gettext_noop('Simplified Chinese')),

)
# 翻譯檔放在專案的目錄下的locale/zh_Hant/
# 重點是要使用zh_Hant，翻譯部份已完成。
LOCALE_PATHS = [
    './locale',

]
```