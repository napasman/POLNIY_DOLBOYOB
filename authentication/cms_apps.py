from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class AuthenticationAppHook(CMSApp):
    name = _('authentication')
    urls = ['authentication.urls']
    app_name= "authentication"

apphook_pool.register(AuthenticationAppHook)