from werkzeug.routing import BaseConverter

class RegionConverter(BaseConverter):
    regex = "[A-Z]{2}"

    def to_url(self, value):
        return super().to_url(value.upper())