from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

COVER_WIDTH = 1600
COVER_HEIGHT = 900
COVER_SIZE = (COVER_WIDTH, COVER_HEIGHT)
INLINE_MAX_WIDTH = 1600
JPEG_QUALITY = 86
PAPER = (250, 247, 241)


class ImageProcessingError(Exception):
    pass


def normalize_cover(uploaded):
    image = _open_image(uploaded)
    image = ImageOps.fit(
        image,
        COVER_SIZE,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    return _jpeg_file(image, uploaded, suffix='-cover')


def constrain_inline_image(uploaded):
    image = _open_image(uploaded)
    if image.width > INLINE_MAX_WIDTH:
        ratio = INLINE_MAX_WIDTH / image.width
        image = image.resize(
            (INLINE_MAX_WIDTH, max(1, round(image.height * ratio))),
            Image.Resampling.LANCZOS,
        )
    return _jpeg_file(image, uploaded, suffix='')


def _open_image(uploaded):
    try:
        uploaded.seek(0)
        image = Image.open(uploaded)
        image.load()
    except Exception as exc:
        raise ImageProcessingError('Fajl nije važeća slika.') from exc
    image = ImageOps.exif_transpose(image) or image
    return _to_rgb(image)


def _to_rgb(image):
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        rgba = image.convert('RGBA')
        background = Image.new('RGB', rgba.size, PAPER)
        background.paste(rgba, mask=rgba.split()[-1])
        return background
    if image.mode != 'RGB':
        return image.convert('RGB')
    return image


def _jpeg_file(image, uploaded, suffix):
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    stem = Path(getattr(uploaded, 'name', 'slika') or 'slika').stem or 'slika'
    name = f'{stem}{suffix}.jpg'
    return ContentFile(buffer.getvalue(), name=name)
