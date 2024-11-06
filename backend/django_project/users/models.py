import copy
import secrets

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import GAMESTATE_INTEGRATION_TEMPLATE, PATH_TO_CFG_FILE


User = get_user_model()


class GSIToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='gsi_token',
        verbose_name='Пользователь',
        )
    value = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Значение',
        )

    class Meta:
        verbose_name = 'GSI Токен'
        verbose_name_plural = 'GSI Токены'

    def __str__(self):
        return self.value


@receiver(post_save, sender=User)
def set_token_for_new_user(sender, instance, created, **kwargs):
    if created:
        token = GSIToken()
        token.user = instance
        token.value = secrets.token_urlsafe(12)
        token.save()


def get_cfg_file(self) -> tuple[str]:
    """
    Generate GSI cfg file.\n
    Return required path in local dota client and content of file in string.
    """
    cfg = copy.deepcopy(GAMESTATE_INTEGRATION_TEMPLATE)
    cfg['Gamestate Integration Script']['auth']['token'] = self.gsi_token.value

    content = []
    for key, value in cfg.items():
        content.append(f'"{key}"\n')
        content.append('{\n')
        for k, v in value.items():
            if isinstance(v, dict):
                content.append(f'  "{k}"\n')
                content.append('  {\n')
                for kk, vv in v.items():
                    content.append(f'    "{kk}" "{vv}"\n')
                content.append('  }\n')
            else:
                content.append(f'  "{k}" "{v}"\n')
        content.append('}\n')

    return (PATH_TO_CFG_FILE, ''.join(content))


User.add_to_class('get_cfg_file', get_cfg_file)
