from netbox.plugins import PluginConfig


class SopVoiceConfig(PluginConfig):
    name = "sop_voice"
    verbose_name = "SOP Voice"
    description = "Manage voice informations of each site."
    version = "1.1.5"
    author = "Leorevoir"
    author_email = "leoquinzler@epitech.eu"
    base_url = "sop-voice"

config = SopVoiceConfig
