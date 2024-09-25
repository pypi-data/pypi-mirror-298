from netbox.api.routers import NetBoxRouter

from .views import *


router = NetBoxRouter()

router.register('voice-deliveries', VoiceDeliveryViewSet)
router.register('voice-sdas', VoiceSdaViewSet)
router.register('site-voice-infos', SiteVoiceInfoViewSet)
router.register('voice-maintainers', VoiceMaintainerViewSet)

urlpatterns = router.urls
