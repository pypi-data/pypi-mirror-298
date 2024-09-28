from utilities.views import GetRelatedModelsMixin
from netbox.views import generic
from dcim.models import Site

from ..models import VoiceMaintainer, SiteVoiceInfo, VoiceSda
from ..forms.voice_maintainer import *
from ..tables.voice_maintainer import *
from ..filtersets import VoiceMaintainerFilterSet
from ..utils import count_all_sda_list


__all__ = (
    'VoiceMaintainerDetailView',
    'VoiceMaintainerEditView',
    'VoiceMaintainerDeleteView',
    'VoiceMaintainerBulkDeleteView',
    'VoiceMaintainerBulkEditView',
    'VoiceMaintainerBulkImportView',
)


class VoiceMaintainerListView(generic.ObjectListView):
    queryset = VoiceMaintainer.objects.all()
    table = VoiceMaintainerTable
    filterset = VoiceMaintainerFilterSet
    filterset_form = VoiceMaintainerFilterForm


class VoiceMaintainerDetailView(generic.ObjectView, GetRelatedModelsMixin):
    queryset = VoiceMaintainer.objects.all()

    def count_sda(self, sites) -> tuple[int, int]:
        '''
        num_count = count of all numbers
        range_count = count of all ranges
        '''
        num_count: int = 0
        range_count: int = 0

        for instance in sites:
            temp = count_all_sda_list(VoiceSda.objects.filter(delivery__site=instance.site))
            num_count += temp.__int__()[0]
            range_count += temp.__int__()[1]

        return num_count, range_count
        
    def get_extra_context(self, request, instance):
        '''
        additionnal context for the related models/objects
        as they are not directly related
        '''
        context: dict = {}

        sites = SiteVoiceInfo.objects.filter(maintainer=instance)
        site_ids = (SiteVoiceInfo.objects.filter(maintainer=instance).values('site__id'))

        tmp: tuple[int, int] = self.count_sda(sites)
        context['num_sda'] = tmp[0]
        context['num_range'] = tmp[1]

        context['site_ids'] = site_ids
        context['related_models'] = self.get_related_models(
            request, 
            instance, 
            extra=(
                (Site.objects.filter(
                    pk__in=(SiteVoiceInfo.objects.filter(maintainer=instance).values('site__id'))
                ), 'id'),
                (VoiceSda.objects.filter(
                    delivery__site__in=SiteVoiceInfo.objects.filter(maintainer=instance).values('site_id')
                ), 'maintainer_id')
            )
        )
        return context


class VoiceMaintainerEditView(generic.ObjectEditView):
    '''
    edits a maintainer instance
    '''
    queryset = VoiceMaintainer.objects.all()
    form = VoiceMaintainerForm


class VoiceMaintainerDeleteView(generic.ObjectDeleteView):
    '''
    deletes a maintainer instance
    '''
    queryset = VoiceMaintainer.objects.all()


class VoiceMaintainerBulkDeleteView(generic.BulkDeleteView):
    '''
    deletes multipel voice maintainers instances
    '''
    queryset = VoiceMaintainer.objects.all()
    table = VoiceMaintainerTable
    filterset = VoiceMaintainerFilterSet


class VoiceMaintainerBulkEditView(generic.BulkEditView):
    '''
    edits multiple voice maintainer instances
    '''
    queryset = VoiceMaintainer.objects.all()
    table = VoiceMaintainerTable
    form = VoiceMaintainerBulkEditForm
    filterset = VoiceMaintainerFilterSet


class VoiceMaintainerBulkImportView(generic.BulkImportView):
    queryset = VoiceMaintainer.objects.all()
    model_form = VoiceMaintainerBulkImportForm

    def save_object(self, object_form, request):
        instance = object_form.save()
        return instance

    def post(self, request):
        '''
        post request handler
        if additionnal changes is needed
        '''
        response = super().post(request)
        return response
