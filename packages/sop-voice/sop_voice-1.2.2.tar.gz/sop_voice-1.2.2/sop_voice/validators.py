import phonenumbers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class VoiceValidator:

    @staticmethod
    def check_site(site) -> None:
        if site is None:
            raise ValidationError({
                'site': _("Site must be set.")
            })

    @staticmethod
    def check_delivery(delivery, site) -> None:
        if delivery and site and delivery.site != site:
            raise ValidationError({
                'delivery': _("Delivery must be set to the same site as the SDA List.")
            })

    @staticmethod
    def check_number(where:str, number:int) -> None:
        if number is None or number == 0 or number == '':
            raise ValidationError({
                f'{where}': _("Number must be set in E164 format.")
            })
        if not phonenumbers.parse(f'+{number}'):
            raise ValidationError({
                f'{where}': _("Number must be a valid phone number written in E164 format.")
            })

    @staticmethod
    def check_start_end(start:int, end:int) -> None:
        if start and end and start > end:
            raise ValidationError({
                'end': _("End number must be greater than or equal to the start number.")
            })
