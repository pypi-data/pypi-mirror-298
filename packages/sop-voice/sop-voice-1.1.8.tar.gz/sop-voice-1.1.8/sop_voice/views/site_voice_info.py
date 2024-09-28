from django.utils.translation import gettext_lazy as _

from netbox.views import generic

from ..forms.site_voice_info import *
from ..models import SiteVoiceInfo


__all__ = (
    'SiteVoiceInfoEditView',
    'SiteVoiceInfoDeleteView'
)


class SiteVoiceInfoEditView(generic.ObjectEditView):
    queryset = SiteVoiceInfo.objects.all()
    form = SiteVoiceInfoForm

    def get_return_url(self, request, obj=None):
        try:
            return '/dcim/sites/' + str(obj.site.pk) + '/voice/'
        except:
            return '/dcim/sites/'


class SiteVoiceInfoDeleteView(generic.ObjectDeleteView):
    queryset = SiteVoiceInfo.objects.all()

    def get_return_url(self, request, obj=None) -> str:
        try:
            if obj is None:
                raise Exception
            return f'/dcim/sites/{obj.site.pk}/voice'
        except:
            return '/dcim/sites/'
