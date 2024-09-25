from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View

from dcim.models import Site
from netbox.views import generic

from sop_utils.utils import *

from ..forms.site_voice_info import *
from ..models import SiteVoiceInfo, VoiceMaintainer


__all__ = (
    'SiteVoiceInfoEditView',
    'SiteVoiceInfoAddView',
    'SiteVoiceInfoRedirectView',
    'SiteVoiceInfoDeleteView'
)


class SiteVoiceInfoRedirectView(View):
    '''
    redirects to the site voice info page
    '''
    def get(self, request, pk=None):
        return redirect('/dcim/sites/')


class SiteVoiceInfoAddView(CustomAddView):
    template_name = 'sop_utils/tools/form.html'
    model = SiteVoiceInfo
    form = SiteVoiceInfoForm

    def get_return_url(self, request, pk=None) -> str:
        try:
            return '/dcim/sites/' + str(pk) + '/voice/'
        except:
            return '/dcim/sites'

    def get_error_url(self, request, pk=None) -> str:
        return f'/plugins/sop-voice/voicemaintainer/add'

    def check_errors(self, request, pk=None) -> bool:
        if not VoiceMaintainer.objects.all().exists():
            messages.warning(request, f'No maintainer found, please add one first.')
            return True
        return False

    def get_extra_context(self, request, pk=None) -> dict:
        try:site = Site.objects.filter(pk=pk).first().name
        except:site = 'site'
        form = self.form
        return_url = self.get_return_url(request, pk)
        return {
            'object': self.model, 'form': form, 'model': self.model._meta.verbose_name.title(),
            'return_url': return_url, 'title': f'Add {site} voice maintainer'
        }


class SiteVoiceInfoEditView(generic.ObjectEditView):
    queryset = SiteVoiceInfo.objects.all()
    form = SiteVoiceInfoForm
    template_name = 'sop_utils/tools/form.html'

    def get_extra_context(self, request, instance):
        return {'object': instance, 'form': self.form,
            'model': self.queryset.model._meta.verbose_name.title(),
            'title': f'Editing {instance.site.name} voice maintainer'
        }

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
            return f'/dcim/sites/{obj.site.pk}'
        except:
            return '/dcim/sites/'
