from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from PIL import Image, UnidentifiedImageError


WEBP_QUALITY = 82


@dataclass(frozen=True)
class ConversionResult:
    original_name: str
    original_mime_type: str
    detected_format: str
    original_size_bytes: int
    output_size_bytes: int
    output_name: str
    output_url: str

    @property
    def original_size_label(self) -> str:
        return format_file_size(self.original_size_bytes)

    @property
    def output_size_label(self) -> str:
        return format_file_size(self.output_size_bytes)

    @property
    def savings_percent(self) -> int:
        if self.original_size_bytes <= 0:
            return 0

        saved = self.original_size_bytes - self.output_size_bytes
        return round(saved / self.original_size_bytes * 100)


class ImageConversionError(ValueError):
    pass


def convert_upload_to_webp(uploaded_file: UploadedFile) -> ConversionResult:
    try:
        image = Image.open(uploaded_file)
        image.load()
    except UnidentifiedImageError as exc:
        raise ImageConversionError('Не получилось распознать файл как изображение.') from exc

    detected_format = image.format or 'unknown'
    original_mime_type = image.get_format_mimetype() or uploaded_file.content_type or 'unknown'

    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')

    output_name = f'{Path(uploaded_file.name).stem or "image"}-{uuid4().hex[:10]}.webp'
    output_dir = Path(settings.MEDIA_ROOT) / 'converted'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_name

    try:
        image.save(output_path, 'WEBP', quality=WEBP_QUALITY, method=6)
    except OSError as exc:
        raise ImageConversionError('Не получилось сохранить изображение в WebP.') from exc

    return ConversionResult(
        original_name=uploaded_file.name,
        original_mime_type=original_mime_type,
        detected_format=detected_format,
        original_size_bytes=uploaded_file.size,
        output_size_bytes=output_path.stat().st_size,
        output_name=output_name,
        output_url=f'{settings.MEDIA_URL}converted/{output_name}',
    )


def format_file_size(size_bytes: int) -> str:
    size = float(size_bytes)
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size < 1024 or unit == 'GB':
            if unit == 'B':
                return f'{int(size)} {unit}'
            return f'{size:.1f} {unit}'
        size /= 1024

    return f'{size_bytes} B'
