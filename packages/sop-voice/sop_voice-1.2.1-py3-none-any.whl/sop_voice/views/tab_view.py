from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View

from utilities.permissions import get_permission_for_model
from utilities.views import register_model_view, ViewTab
from netbox.views.generic.mixins import ActionsMixin
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from dcim.models import Site

from ..tables.voice_delivery import *
from ..tables.voice_sda import *
from ..models import *
from ..utils import count_all_sda_list, get_object_or_create


'''
accessed for "Voice" site tab View
'''


__all__ = (
    'VoiceSiteTabView',
)


@register_model_view(Site, name="voice")
class VoiceSiteTabView(View, ActionsMixin, PermissionRequiredMixin, AccessMixin):
    '''
    creates a "voice" tab on the site page
    '''
    tab = ViewTab(
        label="Voice",
        badge=lambda obj: count_all_sda_list(VoiceSda.objects.filter(delivery__site=obj)).__int__()[0]
    )
    template_name = "sop_voice/tab/tab.html"

    def get_table(self, table, qs, request):
        table = table(qs, user=request.user)
        if 'pk' in table.base_columns:
            table.columns.show('pk')
        table.configure(request)
        return table

    def get_extra_context(self, request, pk) -> dict:
        '''
        returns all the models and tables needed for the tab
        '''
        context: dict = {}
    
        site = get_object_or_404(Site, pk=pk)
        context['site_info'] = get_object_or_create(SiteVoiceInfo, site)
        context['sda'] = VoiceSda
        context['sda_table'] = self.get_table(VoiceSdaTable, VoiceSda.objects.filter(delivery__site=site), request)
        context['delivery'] = VoiceDelivery
        context['delivery_table'] = self.get_table(VoiceDeliveryTable, VoiceDelivery.objects.filter(site=site), request)
        context['context'] = context
        context['actions'] = DEFAULT_ACTION_PERMISSIONS

        '''
        change the devices with the filter you want
        '''
        # context['devices'] = Device.objects.filter(site=site)

        return {'object': site, 'context': context}

    def get(self, request, pk):
        if not request.user.has_perm(get_permission_for_model(VoiceSda, 'view')):
            return self.handle_no_permission()
        return render(request, self.template_name,
            self.get_extra_context(request, pk))
