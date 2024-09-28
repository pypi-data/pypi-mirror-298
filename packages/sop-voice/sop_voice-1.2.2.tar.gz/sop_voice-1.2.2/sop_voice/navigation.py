from django.utils.translation import gettext_lazy as _

from netbox.registry import registry
from netbox.navigation import *
from netbox.navigation.menu import MENUS


VOICE = Menu(
    label=_('Voice'),
    icon_class="mdi mdi-phone",
    groups=(
        MenuGroup(
            label=_('Maintainers'),
            items=(
                MenuItem(
                    link=f'plugins:sop_voice:voicemaintainer_list',
                    link_text=_('Voice Maintainers'),
                    permissions=[f'sop_voice.view_voicemaintainer'],
                    buttons=(
                        MenuItemButton(
                            link=f'plugins:sop_voice:voicemaintainer_add',
                            title='Add',
                            icon_class='mdi mdi-plus-thick',
                            permissions=[f'sop_voice.add_voicemaintainer'],
                        ),
                        MenuItemButton(
                            link=f'plugins:sop_voice:voicemaintainer_import',
                            title='Import',
                            icon_class='mdi mdi-upload',
                            permissions=[f'sop_voice.add_voicemaintainer'],
                        ),
                    ),
                ),
            ),
        ),
        MenuGroup(
            label=_('DIDs'),
            items=(
                MenuItem(
                    link=f'plugins:sop_voice:voicesda_list',
                    link_text=_('DIDs List'),
                    permissions=[f'sop_voice.view_voicesda'],
                    buttons=(
                        MenuItemButton(
                            link=f'plugins:sop_voice:voicesda_add',
                            title='Add',
                            icon_class='mdi mdi-plus-thick',
                            permissions=[f'sop_voice.add_voicesda'],
                        ),
                        MenuItemButton(
                            link=f'plugins:sop_voice:voicesda_import',
                            title='Import',
                            icon_class='mdi mdi-upload',
                            permissions=[f'sop_voice.add_voicesda'],
                        ),
                    ),
                ),
            ),
        ),
        MenuGroup(
            label=_('Deliveries'),
            items=(
                MenuItem(
                    link=f'plugins:sop_voice:voicedelivery_list',
                    link_text=_('Deliveries List'),
                    permissions=[f'sop_voice.view_voicedelivery'],
                    buttons=(
                        MenuItemButton(
                            link=f'plugins:sop_voice:voicedelivery_add',
                            title='Add',
                            icon_class='mdi mdi-plus-thick',
                            permissions=[f'sop_voice.add_voicedelivery'],
                        ),
                    ),
                ),
            ),
        ),
    ),
)

MENUS.append(VOICE)
