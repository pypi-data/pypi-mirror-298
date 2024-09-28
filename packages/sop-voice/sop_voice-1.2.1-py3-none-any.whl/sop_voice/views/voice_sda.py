from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from netbox.views import generic

from ..forms.voice_sda import *
from ..tables.voice_sda import *
from ..filtersets import VoiceSdaFilterSet
from ..models import *
from ..utils import count_all_sda_list, format_number


__all__ = (
    'VoiceSdaEditView',
    'VoiceSdaDeleteView',
    'VoiceSdaDetailView',
    'VoiceSdaBulkEditView',
    'VoiceSdaBulkDeleteView',
    'VoiceSdaListView',
    'VoiceSdaBulkImportView'
)


class VoiceSdaListView(generic.ObjectListView):
    '''
    all DIDs list
    '''
    queryset = VoiceSda.objects.all()
    table = VoiceSdaTable
    filterset_form = VoiceSdaFilterForm
    filterset = VoiceSdaFilterSet


class VoiceSdaBulkEditView(generic.BulkEditView):
    '''
    for the "edit selected" view
    '''
    queryset = VoiceSda.objects.all()
    table = VoiceSdaTable
    form = VoiceSdaBulkEditForm
    filterset = VoiceSdaFilterSet


class VoiceSdaBulkDeleteView(generic.BulkDeleteView):
    '''
    for the "delete selected" view
    '''
    queryset = VoiceSda.objects.all()
    table = VoiceSdaTable
    filterset = VoiceSdaFilterSet


class VoiceSdaEditView(generic.ObjectEditView):
    '''
    edits a SDA List instance
    '''
    queryset = VoiceSda.objects.all()
    form = VoiceSdaForm
    

class VoiceSdaDeleteView(generic.ObjectDeleteView):
    '''
    deletes a SDA List instance
    '''
    queryset = VoiceSda.objects.all()


class VoiceSdaDetailView(generic.ObjectView, PermissionRequiredMixin):
    '''
    returns the SDA List detial page with context
    '''
    queryset = VoiceSda.objects.all()

    def get_extra_context(self, request, instance):
        context: dict = {}

        try:
            context['start'] = format_number(instance.start)
            context['end'] = format_number(instance.end)
            context['num_sda'] = count_all_sda_list(instance).__int__()[0]
            context['maintainer'] = SiteVoiceInfo.objects.filter(site=instance.delivery.site).first()
        except:pass
        return context


class VoiceSdaBulkImportView(generic.BulkImportView):
    queryset = VoiceSda.objects.all()
    model_form = VoiceSdaBulkImportForm

    def save_object(self, object_form, request):
        instance = object_form.save()
        
        if not instance.end or instance.end == 0:
            instance.end = instance.start
            instance.save()

        return instance

    def post(self, request):
        '''
        post request handler
        if additionnal changes is needed
        '''
        response = super().post(request)
        return response
