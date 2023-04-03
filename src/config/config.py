import click

class Config(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            instance = super(Config, cls).__new__(cls)
            instance._values = dict()
            cls.instance = instance
        return cls.instance
    
    def get_value(self, key):
        return self._values.get(key)
    
    def set_value(self, key, value):
        click.echo(f"Setting {key} as {value}")
        self._values[key] = value
