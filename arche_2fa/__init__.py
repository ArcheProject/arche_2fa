from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('arche_2fa')


def includeme(config):
    config.commit()
    config.include('.models')
    config.include('.schemas')
    config.include('.views')
