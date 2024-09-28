from django.urls import path

from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from .views import voice_maintainer as vm
from .views import voice_delivery as vd
from .views import voice_sda as sda
from .views import site_voice_info as svi

'''🡣 DO NOT REMOVE 🡣'''
from .views import tab_view
'''🡩 DO NOT REMOVE 🡩'''

from .models import *


app_name = 'sop_voice'


urlpatterns = [

    # voice maintainer
    path('voicemaintainer/', vm.VoiceMaintainerListView.as_view(), name='voicemaintainer_list'),
    path('voicemaintainer/<int:pk>', vm.VoiceMaintainerDetailView.as_view(), name='voicemaintainer_detail'),
    path('voicemaintainer/add', vm.VoiceMaintainerEditView.as_view(), name='voicemaintainer_add'),
    path('voicemaintainer/edit', vm.VoiceMaintainerBulkEditView.as_view(), name='voicemaintainer_bulk_edit'),
    path('voicemaintainer/import', vm.VoiceMaintainerBulkImportView.as_view(), name='voicemaintainer_import'),
    path('voicemaintainer/delete/', vm.VoiceMaintainerBulkDeleteView.as_view(), name='voicemaintainer_bulk_delete'),
    path('voicemaintainer/edit/<int:pk>', vm.VoiceMaintainerEditView.as_view(), name='voicemaintainer_edit'),
    path('voicemaintainer/delete/<int:pk>', vm.VoiceMaintainerDeleteView.as_view(), name='voicemaintainer_delete'),
    path('voicemaintainer/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='voicemaintainer_changelog', kwargs={'model': VoiceMaintainer}),
    path('voicemaintainer/journal/<int:pk>', ObjectJournalView.as_view(), name='voicemaintainer_journal', kwargs={'model': VoiceMaintainer}),

    # voice delivery
    path('voice-delivery/', vd.VoiceDeliveryListView.as_view(), name='voicedelivery_list'),
    path('voice-delivery/<int:pk>', vd.VoiceDeliveryDetailView.as_view(), name='voicedelivery_detail'),
    path('voice-delivery/add', vd.VoiceDeliveryEditView.as_view(), name='voicedelivery_add'),
    path('voice-delivery/edit', vd.VoiceDeliveryBulkEditView.as_view(), name='voicedelivery_bulk_edit'),
    path('voice-delivery/delete', vd.VoiceDeliveryBulkDeleteView.as_view(), name='voicedelivery_bulk_delete'),
    path('voice-delivery/edit/<int:pk>', vd.VoiceDeliveryEditView.as_view(), name='voicedelivery_edit'),
    path('voice-delivery/delete/<int:pk>', vd.VoiceDeliveryDeleteView.as_view(), name='voicedelivery_delete'),
    path('voice-delivery/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='voicedelivery_changelog', kwargs={'model': VoiceDelivery}),
    path('voice-delivery/journal/<int:pk>', ObjectJournalView.as_view(), name='voicedelivery_journal', kwargs={'model': VoiceDelivery}),

    # sda list
    path('sda-list/', sda.VoiceSdaListView.as_view(), name='voicesda_list'),
    path('sda-list/<int:pk>', sda.VoiceSdaDetailView.as_view(), name='voicesda_detail'),
    path('sda-list/add', sda.VoiceSdaEditView.as_view(), name='voicesda_add'),
    path('sda-list/edit/', sda.VoiceSdaBulkEditView.as_view(),  name='voicesda_bulk_edit'),
    path('sda-list/import/', sda.VoiceSdaBulkImportView.as_view(), name='voicesda_import'),
    path('sda-list/delete/', sda.VoiceSdaBulkDeleteView.as_view(), name='voicesda_bulk_delete'),
    path('sda-list/edit/<int:pk>', sda.VoiceSdaEditView.as_view(), name='voicesda_edit'),
    path('sda-list/delete/<int:pk>', sda.VoiceSdaDeleteView.as_view(), name='voicesda_delete'),
    path('sda-list/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='voicesda_changelog', kwargs={'model': VoiceSda}),
    path('sda-list/journal/<int:pk>', ObjectJournalView.as_view(), name='voicesda_journal', kwargs={'model': VoiceSda}),
 
    # site voice info
    path('site-voice-info/edit/<int:pk>', svi.SiteVoiceInfoEditView.as_view(), name='sitevoiceinfo_edit'),
    path('site-voice-info/delete/<int:pk>', svi.SiteVoiceInfoDeleteView.as_view(), name='sitevoiceinfo_delete'),
    
]
