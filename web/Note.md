## 這裡記錄著開發django 時做過的蠢事，寫下來以免再犯。

1. 無論如何，第三方套件的UserProfile 應該不需要override! 因為基本上都是OneToOneField(settings.settings.AUTH_USER_MODEL,...)，如果override會造成整個測試都是錯的。
2. 同時使用二個複雜套件，應該主要要處理的是功能上的整合。UserProfile 雖然算是主要功能但應該不用被處理。
