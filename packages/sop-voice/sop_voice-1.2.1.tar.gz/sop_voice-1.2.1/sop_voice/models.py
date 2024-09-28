import sys
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from netbox.models import NetBoxModel
from circuits.models import Provider
from dcim.models import Site
from utilities.choices import ChoiceSet

from .validators import VoiceValidator


__all__ = (
    'VoiceSda',
    'VoiceDelivery',
    'SiteVoiceInfo',
    'VoiceMaintainer',
    'VoiceMaintainerStatusChoice',
    'VoiceDeliveryStatusChoices',
    'SopBoolChoices',
)


class VoiceMaintainerStatusChoice(ChoiceSet):

    CHOICES = (
        ('active', _('Active'), 'green'),
        ('retired', _('Retired'), 'red'),
        ('unknown', _('Unknown'), 'gray'),
    )


class VoiceDeliveryStatusChoices(ChoiceSet):

    CHOICES = (
        ('active', _('Active'), 'green'),
        ('planned', _('Planned'), 'cyan'),
        ('staging', _('Staging'), 'blue'),
        ('retired', _('Retired'), 'red'),
        ('unknown', _('Unknown'), 'gray'),
    )


class SopBoolChoices(ChoiceSet):

    CHOICES = (
        ('unknown', _('Unknown'), 'gray'),
        ('true', _('True'), 'green'),
        ('false', _('False'), 'red'),
    )


class VoiceMaintainer(NetBoxModel):
    name = models.CharField(
        verbose_name=_('Maintainer'),
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=100,
        unique=True,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        choices=VoiceMaintainerStatusChoice,
        default="Unknown",
        verbose_name=_('Status')
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=200,
        blank=True
    )
    comments = models.TextField(
        verbose_name=_('comments'),
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicemaintainer_detail', args=[self.pk])

    def get_status_color(self) -> str:
        return VoiceDeliveryStatusChoices.colors.get(self.status)

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Voice Maintainer')
        verbose_name_plural = _('Voice Maintainers')


class SiteVoiceInfo(NetBoxModel):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )
    maintainer = models.ForeignKey(
        VoiceMaintainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Maintainer'),
    )

    def __str__(self) -> str:
        return f'{self.site} voice maintainer'

    def get_absolute_url(self) -> str:
        if self.site:
            return f'/dcim/sites/{self.site.pk}/voice'
        return reverse('plugins:sop_voice:voicemaintainer_list')

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Information')
        verbose_name_plural = _('Informations')


class VoiceDelivery(NetBoxModel):
    delivery = models.CharField(
        verbose_name=_('Delivery'),
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='voice_delivery_provider',
        verbose_name=_('Provider')
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='voice_delivery_site',
        verbose_name=_('Site'),
    )
    channel_count = models.BigIntegerField(
        verbose_name=_('Channel Count'),
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        choices=VoiceDeliveryStatusChoices,
        verbose_name=_('Status'),
    )
    ndi = models.BigIntegerField(
        verbose_name=_('NDI'),
        null=True,
        blank=True,
    )
    dto = models.BigIntegerField(
        verbose_name=_('DTO'),
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=200,
        blank=True
    )
    comments = models.TextField(
        verbose_name=_('comments'),
        blank=True
    )

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicedelivery_detail', args=[self.pk])

    def get_status_color(self) -> str:
        return VoiceDeliveryStatusChoices.colors.get(self.status)

    def __str__(self) -> str:
        return f'{self.delivery} / {self.provider}'

    def clean(self):
        super().clean()
        if self.ndi:
            VoiceValidator.check_number('ndi', self.ndi)
        if self.dto:
            VoiceValidator.check_number('dto', self.dto)

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Voice Delivery')
        verbose_name_plural = _('Voice Deliveries')


class VoiceSda(NetBoxModel):
    delivery = models.ForeignKey(
        VoiceDelivery,
        on_delete=models.SET_NULL,
        verbose_name=_('Delivery'),
        blank=True,
        null=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
        null=True,
        blank=True,
    )
    start = models.BigIntegerField(
        unique=False,
        verbose_name=_('Start number'),
        null=True,
        blank=True,
    )
    end = models.BigIntegerField(
        unique=False,
        verbose_name=_('End number'),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f'"{self.start} >> {self.end}"'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicesda_detail', args=[self.pk])

    def clean(self):
        super().clean()
        VoiceValidator.check_site(self.site)
        VoiceValidator.check_number('start', self.start)
        if self.end:
            VoiceValidator.check_number('end', self.end)
        VoiceValidator.check_delivery(self.delivery, self.site)
        if self.end and self.start:
            VoiceValidator.check_start_end(self.start, self.end)

    def save(self, *args, **kwargs):
        if not self.end or self.end == 0:
            self.start = self.end
        super().save(*args, **kwargs)

    class Meta(NetBoxModel.Meta):
        ordering = ('start',)
        verbose_name = _('DID Range')
        verbose_name_plural = _('DIDs')
