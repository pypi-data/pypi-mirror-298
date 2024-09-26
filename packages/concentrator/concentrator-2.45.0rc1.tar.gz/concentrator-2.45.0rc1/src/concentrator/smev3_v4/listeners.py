from concentrator.smev3_v4.forms import DeclarationEditWindowExtender
from concentrator.smev3_v4.forms import DelegateEditWinExtender
from educommon.m3.extensions import BaseEditWinListener
from educommon.m3.extensions import BaseSaveListener

from kinder.controllers import obs


class EditDeclarationListener(BaseEditWinListener):
    """Добавляет в окно редактирования заявления чек-боксы:

    * Согласие на группу сокращенного дня
    * Согласие на группу продленного дня
    * Согласие на обучение по адаптированной образовательной программе
    """

    ui_extender_cls = DeclarationEditWindowExtender
    listen = [
        'kinder.core.declaration/DeclarationPack/DeclarationEditAction',
        'kinder.core.declaration/DeclarationPack/DeclarationAddAction',
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclarationEditAction',
        'kinder.core.queue_module.declaration'
        '/QueueDeclarationPack/DeclarationAddAction',
    ]
    parent_model_field = 'id'

    def _get_id(self, context):
        return getattr(context, self.action.parent.id_param_name, None)


class DeclarationSaveListener(BaseSaveListener):
    """Сохранение дополнительных видов согласия для заявления"""

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/DeclarationSaveAction'
    ]

    ui_extender_cls = DeclarationEditWindowExtender
    parent_model_field = 'id'

    def _declare_additional_context(self):
        return {
            "abbreviated_group_consent": {
                "type": 'js_checkbox',
                'default': False
            },
            "extended_group_consent": {
                "type": 'js_checkbox',
                'default': False
            },
            "adapted_program_consent": {
                "type": 'js_checkbox',
                'default': False
            },

        }

    def post_save(self, arguments):
        parent_model_instance, context = arguments
        super().post_save((parent_model_instance.declaration.id, context))

        return parent_model_instance, context


class DelegateEditWindowListener(BaseEditWinListener):
    """Добавляет в окно создания/редактирования карточки родителя чек-бокс
    Документ о праве нахождения в РФ
    """

    ui_extender_cls = DelegateEditWinExtender
    parent_model_field = 'id'

    listen = [
        'kinder.core.children/DelegateActionPack/DelegateEditAction',
        'kinder.core.children/'
        'DelegateForChildrenPack/CustomEditWindowAction',
        'kinder.core.children/'
        'DelegateForChildrenPack/DelegateNewAction',
        'kinder.core.children/'
        'DelegateForDeclarationPack/CustomEditWindowAction',
        'kinder.core.children/'
        'ForSelectWindowDelegatePack/DelegateSelectOrCreateWindowAction',
        'kinder.core.children/ForSelectWindowDelegatePack/DelegateNewAction',
        '.*/LipetskDelegateForDeclarationPack/CustomEditWindowAction',
        '.*/LipetskDelegateForDeclarationPack/ShowDataAction',
        '.*/DelegateForDeclarationPack/ShowDataAction',
    ]

    def _get_id(self, context):
        return getattr(context, self.action.parent.id_param_name, None)


class DelegateSaveActionListener(BaseSaveListener):
    """Выполняет сохранение карточки родителя с данными чек-бокса
    Документ о праве нахождения в РФ
    """

    ui_extender_cls = DelegateEditWinExtender
    parent_model_field = 'id'

    listen = [
        'kinder.core.children/DelegateActionPack/DelegateSaveAction',
        'kinder.core.children/DelegateForChildrenPack/DelegateSaveAction',
        'kinder.core.children/DelegateForDeclarationPack/DelegateSaveAction',
        'kinder.core.children/ForSelectWindowDelegatePack/DelegateSaveAction',
        '.*/LipetskDelegateForDeclarationPack/DelegateSaveAction',
        'kinder.core.children/DelegateForDeclarationPack/'
        'ContingentDelegateSaveAction',
    ]

    def _declare_additional_context(self):
        return {
            "confirming_rights_located_rf": {
                "type": 'js_checkbox',
                'default': False
            }
        }

    def _get_instance(self, parent_model_instance, context):
        """Модель не расширяется какой-либо другой моделью, поэтому возвращаем
        модель Delegate
        """
        return parent_model_instance


def register_listeners():
    obs.subscribe(EditDeclarationListener)
    obs.subscribe(DeclarationSaveListener)
    obs.subscribe(DelegateEditWindowListener)
    obs.subscribe(DelegateSaveActionListener)
