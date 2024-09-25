from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from circuits.models import Provider
from dcim.models import Site

from sop_utils.models import VoiceMaintainerStatusChoice

from ..models import *


__all__ = (
    'VoiceDeliverySerializer',
    'NestedVoiceDeliverySerializer',
    'VoiceSdaSerializer',
    'NestedVoiceSdaSerializer',
    'SiteVoiceInfoSerializer',
    'NestedSiteVoiceInfoSerializer',
    'VoiceMaintainerSerializer',
    'NestedVoiceMaintainerSerializer'
)


#_______________________________
# Nested Briefs Serializers
# -> | for addditional infos
#    | without modifying original


class ProviderBriefSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:provider-detail')

    class Meta:
        model = Provider
        fields = [
            'id', 'url', 'name', 'slug', 'description'
        ]


class SiteBriefSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:site-detail')
    dids = serializers.SerializerMethodField()
    
    class Meta:
        model = Site
        fields = ('id', 'url', 'name', 'description', 'slug', 'dids')

    def get_dids(self, obj):
        voice_sda = VoiceSda.objects.filter(delivery__site=obj)
        dids = [sda for sda in voice_sda if sda]
        return NestedVoiceSdaSerializer(dids, many=True, context=self.context).data


#_______________________________
# Voice Maintainer


class VoiceMaintainerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicemaintainer-detail'
    )
    status = ChoiceField(
        choices=VoiceMaintainerStatusChoice
    )
    site = serializers.SerializerMethodField()

    class Meta:
        model = VoiceMaintainer
        fields = (
            'id', 'url', 'display', 'name', 'status', 'description', 'created', 'last_updated',
            'site',
        )
        brief_fields = ('id', 'url', 'name', 'description')

    def get_site(self, obj):
        site_voice_infos = SiteVoiceInfo.objects.filter(maintainer=obj).prefetch_related(
            Prefetch('site', queryset=Site.objects.all())
        )
        site = [svi.site for svi in site_voice_infos if svi.site]
        return SiteBriefSerializer(site, many=True, context=self.context).data


class NestedVoiceMaintainerSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicemaintainer-detail'
    )

    class Meta:
        model = VoiceMaintainer
        fields = ['id', 'url', 'display', 'name', 'description']


#_______________________________
# Site Voice Info (Informations)


class SiteVoiceInfoSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:sitevoiceinfo-detail'
    )
    site_name = serializers.SerializerMethodField()
    maintainer = serializers.SerializerMethodField()

    class Meta:
        model = SiteVoiceInfo
        fields = ('id', 'url', 'display', 'site', 'site_name', 'maintainer')

    def get_site_name(self, obj):
        return obj.site.name

    def get_maintainer(self, obj):
        maintainer_id = VoiceMaintainer.objects.filter(pk=obj.maintainer.id)
        return NestedVoiceMaintainerSerializer(maintainer_id, many=True, context=self.context).data


class NestedSiteVoiceInfoSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:sitevoiceinfo-detail'
    )

    class Meta:
        model = SiteVoiceInfo
        fields = ('id', 'url', 'site', 'maintainer')


#_______________________________
# Voice Sda (DIDs)


class VoiceSdaSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicesda-detail'
    )
    delivery = serializers.SerializerMethodField()

    class Meta:
        model = VoiceSda
        fields = ('id', 'url', 'delivery', 'start', 'end')

    def get_delivery(self, obj):
        deliv = VoiceDelivery.objects.filter(pk=obj.delivery.id)
        return NestedVoiceDeliverySerializer(deliv, many=True, context=self.context).data


class NestedVoiceSdaSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicesda-detail'
    )

    class Meta:
        model = VoiceSda
        fields = ('id', 'url', 'delivery', 'start', 'end')


#_______________________________
# Voice Delivery


class VoiceDeliverySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicedelivery-detail'
    )
    site_name = serializers.SerializerMethodField()
    provider = serializers.SerializerMethodField()
    dids = serializers.SerializerMethodField()

    class Meta:
        model = VoiceDelivery
        fields = ('id', 'url', 'display', 'delivery', 'provider', 'site', 'site_name',
            'channel_count', 'status', 'dids'
        )
        brief_fields = ('id', 'url', 'display', 'delivery', 'provider')

    def get_site_name(self, obj):
        return obj.site.name

    def get_provider(self, obj):
        prov = Provider.objects.filter(pk=obj.provider.id)
        return ProviderBriefSerializer(prov, many=True, context=self.context).data

    def get_dids(self, obj):
        sda = VoiceSda.objects.filter(delivery__id=obj.id)
        return NestedVoiceSdaSerializer(sda, many=True, context=self.context).data


class NestedVoiceDeliverySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicedelivery-detail'
    )
    provider = serializers.SerializerMethodField()

    class Meta:
        model = VoiceDelivery
        fields = ('id', 'url', 'delivery', 'display', 'provider')

    def get_provider(self, obj):
        prov = Provider.objects.filter(pk=obj.provider.id)
        return ProviderBriefSerializer(prov, many=True, context=self.context).data
