from lin.exception import Duplicated, Failed, NotFound


class BookNotFound(NotFound):
    message = "书籍不存在"
    _config = False


class BookDuplicated(Duplicated):
    code = 419
    message = "图书已存在"
    _config = False


class RefreshFailed(Failed):
    message = "令牌刷新失败"
    message_code = 10052
    _config = False


class CatalogueNotFound(NotFound):
    message = "分类不存在"
    _config = False


class AppNotFound(NotFound):
    message = "App不存在"
    _config = False


class AppRelNotFound(NotFound):
    message = "App发行版不存在"
    _config = False


class IconNotFound(NotFound):
    message = "图标不存在"
    _config = False


class IconpackNotFound(NotFound):
    message = "图标包不存在"
    _config = False
