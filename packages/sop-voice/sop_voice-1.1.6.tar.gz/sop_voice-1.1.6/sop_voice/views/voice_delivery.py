from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _

from utilities.views import GetRelatedModelsMixin
from netbox.views import generic
from circuits.models import Provider

from sop_utils.utils import *

from ..forms.voice_delivery import *
from ..tables.voice_delivery import *
from ..tables.voice_sda import *
from ..filtersets import VoiceDeliveryFilterSet
from ..models import *


__all__ =  (
    'VoiceDeliveryDetailView',
    'VoiceDeliveryEditView',
    'VoiceDeliveryDeleteView',
    'VoiceDeliveryBulkEditView',
    'VoiceDeliveryDeleteView',
    'VoiceDeliveryListView',
)


class VoiceDeliveryListView(generic.ObjectListView):
    queryset = VoiceDelivery.objects.all()
    table = VoiceDeliveryTable
    filterset = VoiceDeliveryFilterSet
    filterset_form = VoiceDeliveryFilterForm


class VoiceDeliveryBulkEditView(generic.BulkEditView):
    queryset = VoiceDelivery.objects.all()
    table = VoiceDeliveryTable
    form = VoiceDeliveryForm
    filterset = VoiceDeliveryFilterSet


class VoiceDeliveryBulkDeleteView(generic.BulkDeleteView):
    queryset = VoiceDelivery.objects.all()
    table = VoiceDeliveryTable
    filterset = VoiceDeliveryFilterSet


class VoiceDeliveryDetailView(generic.ObjectView, PermissionRequiredMixin, GetRelatedModelsMixin):
    '''
    returns the Voice Delivery detail page with context
    '''
    queryset = VoiceDelivery.objects.all()

    def get_extra_context(self, request, instance) -> dict:
        context: dict = {}

        sda_list = VoiceSda.objects.filter(delivery=instance)
        temp: tuple[int, int] = count_all_sda_list(sda_list).__int__()

        try:
            site_info = SiteVoiceInfo.objects.filter(site=instance.site.id)
            context['maintainer'] = site_info.first().maintainer
        except:pass
        context['num_sda'] = temp[0]
        context['num_range'] = temp[1]
        context['related_models'] = self.get_related_models(
            request, instance,
        )
        return context


class VoiceDeliveryAddView(CustomAddView):
    '''
    creates anew Voice Delivery instance
    '''
    template_name: str = 'sop_utils/tools/form.html'
    model = VoiceDelivery
    form = VoiceDeliveryForm

    def get_return_url(self, request, pk=None):
        if pk is not None:
            return f'/dcim/sites/{pk}/voice/'
        return '/dcim/sites/'

    def check_errors(self, request, pk=None) -> bool:
        if not Provider.objects.all().exists():
            messages.warning(request, _('No provider found, pease create one first.'))
            return False
        return False


class VoiceDeliveryEditView(CustomEditView):
    template_name: str = 'sop_utils/tools/form.html'
    model = VoiceDelivery
    form = VoiceDeliveryForm

    def get_return_url(self, request, pk=None) -> str:
        try:
            obj = VoiceDelivery.objects.filter(pk=pk).first().site.id
            if pk is not None:
                return f'/dcim/sites/{obj}/voice'
        except:pass
        return '/dcim/sites/'

    def check_errors(self, request, pk=None) -> bool:
        if not Provider.objects.all().exists():
            messages.warning(request, _('No provider found, please create one first.'))
            return False
        return False
        


class VoiceDeliveryDeleteView(generic.ObjectDeleteView, PermissionRequiredMixin):
    '''
    deletes a Voice Delivery object
    '''
    queryset = VoiceDelivery.objects.all()
