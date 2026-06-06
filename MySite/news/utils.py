class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, string):
        if isinstance(string, str):
            return string.upper()
        return string.title.upper()

class MetaTagsMixin(object):
    # Миксин для добавления SEO мета-тегов в контекст представлений (Views).
    meta_description = ''
    meta_keywords = ''
