from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class BlogAppHook(CMSApp):
    name = _('posts')
    app_name= "posts"
    
    def get_urls(self, page=None, language=None, **kwargs):
        return ["posts.urls"]


apphook_pool.register(BlogAppHook)