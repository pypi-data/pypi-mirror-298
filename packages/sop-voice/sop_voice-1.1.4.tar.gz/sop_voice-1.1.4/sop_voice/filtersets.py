import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _ 

from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Site

from sop_utils.models import VoiceDeliveryStatusChoices, VoiceMaintainerStatusChoice

from .models import VoiceSda, VoiceDelivery, VoiceMaintainer, SiteVoiceInfo


__all__ = (
    'VoiceDeliveryFilterSet',
    'SiteVoiceInfoFilterSet',
    'VoiceMaintainerFilterSet',
    'VoiceSdaFilterSet',
)


class VoiceDeliveryFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=VoiceDeliveryStatusChoices,
        null_value=None
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site',
        label=_('Site (ID)')
    )
    site_name = django_filters.CharFilter(
        field_name='site__name',
        label=_('Site (name)')
    )

    class Meta:
        model = VoiceDelivery
        fields = ('id', 'delivery', 'provider', 'status')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(delivery__icontains=value) |
            Q(start__icontains=value) |
            Q(end__icontains=value)
        )


class SiteVoiceInfoFilterSet(NetBoxModelFilterSet):

    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site__id',
        method='search_site_id',
        label=_('Site (ID)')
    )
    site_name = django_filters.CharFilter(
        method='search_site_name',
        label=_('Site (name)')
    )

    class Meta:
        model = SiteVoiceInfo
        fields = ('id', 'site', 'site_id', 'site_name', 'maintainer',)

    def search_site_id(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(site__in=value)

    def search_site_name(self, queryset, name, value):
        if not value:
            return queryset
        try:
            site = Site.objects.filter(name__in=value)
            return queryset.filter(site__in=site)
        except:return queryset


class VoiceMaintainerFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=VoiceMaintainerStatusChoice,
        null_value=None
    )
    site_name = django_filters.CharFilter(
        method='search_site_name',
        label=_('Site (name)')
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        method='search_site_id',
        label=_('Site (ID)')
    )

    class Meta:
        model = VoiceMaintainer
        fields = ('id', 'name', 'status')

    def search_site_name(self, queryset, name, value):
        print(value)
        if not value:
            return queryset
        try:
            maintainer_id = SiteVoiceInfo.objects.filter(site__in=Site.objects.filter(name=value)).values_list('maintainer_id', flat=True)
            return queryset.filter(pk__in=maintainer_id)
        except:return queryset

    def search_site_id(self, queryset, name, value):
        if not value:
            return queryset
        try:
            maintainer_id = SiteVoiceInfo.objects.filter(site__in=value).values_list('maintainer_id', flat=True)
            return queryset.filter(pk__in=maintainer_id)
        except:return queryset

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


class VoiceSdaFilterSet(NetBoxModelFilterSet):
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='delivery__site',
        label=_('Site (ID)')
    )
    maintainer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VoiceMaintainer.objects.all(),
        field_name='delivery__site',
        method='sda_maintainer_filter',
        label=_('Maintainer (ID)')
    )
    delivery_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VoiceDelivery.objects.all(),
        field_name='delivery_id',
        label=_('Delivery (ID)')
    )

    class Meta:
        model = VoiceSda
        fields = ('id', 'start', 'end', 'delivery_id')

    def sda_maintainer_filter(self, queryset, name, value):
        if not value:
            return queryset
        try:
            site_ids = SiteVoiceInfo.objects.filter(maintainer__in=value).values_list('site_id', flat=True)
            return queryset.filter(delivery__site_id__in=site_ids)
        except:return queryset

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(delivery__icontains=value) |
            Q(start__icontains=value) |
            Q(end__icontains=value)
        )
