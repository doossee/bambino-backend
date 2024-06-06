import re
import io
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


def validate_hex_color(value):
    if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
        raise ValidationError(f"{value} is not a valid hex color code")


class ColorField(models.CharField):
    default_validators = [validate_hex_color]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 7
        super().__init__(*args, **kwargs)


class WebPField(models.ImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        if file and hasattr(file, "file"):
            image = Image.open(file.file)
            output = io.BytesIO()
            image.save(output, format="WEBP", quality=80)
            output.seek(0)
            file_name = file.name.rsplit(".", 1)[0] + ".webp"
            file.file = ContentFile(output.read())
            file.name = file_name
        return file
