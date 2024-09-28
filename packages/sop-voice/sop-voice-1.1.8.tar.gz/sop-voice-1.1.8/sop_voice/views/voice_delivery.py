from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _

from utilities.views import GetRelatedModelsMixin
from netbox.views import generic

from ..forms.voice_delivery import *
from ..tables.voice_delivery import *
from ..tables.voice_sda import *
from ..filtersets import VoiceDeliveryFilterSet
from ..models import *
from ..utils import count_all_sda_list, format_number


__all__ =  (
    'VoiceDeliveryEditView',
    'VoiceDeliveryDetailView',
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
    form = VoiceDeliveryBulkEditForm
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
        if instance.ndi:
            context['ndi'] = format_number(instance.ndi)
        if instance.dto:
            context['dto'] = format_number(instance.dto)
        context['num_sda'] = temp[0]
        context['num_range'] = temp[1]
        context['related_models'] = self.get_related_models(
            request, instance,
        )
        return context


class VoiceDeliveryEditView(generic.ObjectEditView):
    '''
    creates anew Voice Delivery instance
    '''
    queryset = VoiceDelivery.objects.all()
    form = VoiceDeliveryForm


class VoiceDeliveryDeleteView(generic.ObjectDeleteView, PermissionRequiredMixin):
    '''
    deletes a Voice Delivery object
    '''
    queryset = VoiceDelivery.objects.all()
