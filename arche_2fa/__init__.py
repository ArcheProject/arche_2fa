from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('arche_2fa')

DEFAULT_SETTINGS = {'arche_2fa.maxtokens': '3'}


def includeme(config):
    config.commit()
    config.include('.models')
    config.include('.schemas')
    config.include('.views')
    config.add_translation_dirs('arche_2fa:locale/')
    settings = config.registry.settings
    for key, value in DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)
    settings['arche_2fa.maxtokens'] = int(settings['arche_2fa.maxtokens'])
