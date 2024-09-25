from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse

from utilities.permissions import get_permission_for_model
from utilities.views import GetRelatedModelsMixin
from netbox.views import generic
from dcim.models import Site

from  sop_utils.utils import count_all_sda_list, CheckJSONMaintainerImport, CustomEditView

from ..models import VoiceMaintainer, SiteVoiceInfo, VoiceSda
from ..forms.voice_maintainer import *
from ..tables.voice_maintainer import *
from ..filtersets import VoiceMaintainerFilterSet


__all__ = (
    'VoiceMaintainerDetailView',
    'VoiceMaintainerEditView',
    'VoiceMaintainerDeleteView',
    'VoiceMaintainerBulkDeleteView',
    'VoiceMaintainerImportForm',
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


class VoiceMaintainerImportForm(View, AccessMixin):
    model = VoiceMaintainer
    template_name: str = "sop_utils/tools/form.html"
    form = VoiceMaintainerImportForm
    return_url: str = "/plugins/sop-voice/voicemaintainer/"

    def get_extra_context(self) -> dict:
        form = self.form
        return {'form': form, 'object': self.model, 'model': self.model._meta.verbose_name.title(),
            'return_url': self.return_url, 'title': f'Import new Voice Maintainers'}

    def get(self, request):
        if not request.user.has_perm(get_permission_for_model(VoiceMaintainer, 'add')):
            return self.handle_no_permission()
        return render(request, self.template_name, self.get_extra_context())

    def save_form(self, request, form):
        obj = CheckJSONMaintainerImport(form.cleaned_data['json_import'])
        checked:list[str]|None = obj.check_format()
        
        if checked is None:
            return False
        try:
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            comments = form.cleaned_data['comments']
            [
                VoiceMaintainer(
                    name=data,
                    status=status,
                    description=description,
                    comments=comments).save()
                for data in checked
            ]
            return True
        except:
            messages.error(request, _('Error importing Voice Maintainer'))
            return False
            
            
    def post(self, request):
        if not request.user.has_perm(get_permission_for_model(VoiceMaintainer, 'add')):
            return self.handle_no_permission()
        form = self.form(request.POST)
        if form.is_valid() and self.save_form(request, form):
            return redirect(self.return_url)
        messages.error(request, _('Invalid JSON'))
        return render(request, self.template_name, self.get_extra_context())


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
    delete selected view
    '''
    queryset = VoiceMaintainer.objects.all()
    table = VoiceMaintainerTable
