from data.config.models import Config
from .base import DataMixin


class ConfigMixin(DataMixin):

    schema = {
        'config': {
            'model': Config,
            'provider': True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['02_config'] = self._config


    def parse_config_value(self, optional = False, help_text = 'environment configuration value'):
        self.parse_variable('config_value', optional, str, help_text,
            value_label = 'VALUE'
        )

    @property
    def config_value(self):
        return self.options.get('config_value', None)


    def parse_config_value_type(self, optional = '--type', help_text = 'environment configuration type (default str)'):
        self.parse_variable('config_value_type', optional, str, help_text,
            value_label = 'TYPE'
        )

    @property
    def config_value_type(self):
        return self.options.get('config_value_type', None)


    def get_config(self, name, default = None, required = False):
        if not name:
            return default

        config = self.get_instance(self._config, name, required = required)
        if config is None:
            return default

        return config.value