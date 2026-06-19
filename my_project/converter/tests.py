from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings
from PIL import Image

from .services import convert_upload_to_webp


def make_png_upload(name='sample.png'):
    buffer = BytesIO()
    Image.new('RGB', (64, 64), '#2358d8').save(buffer, format='PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


class ImageConversionTests(SimpleTestCase):
    def test_convert_upload_to_webp_returns_file_metadata(self):
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root, MEDIA_URL='/media/'):
                result = convert_upload_to_webp(make_png_upload())

        self.assertEqual(result.detected_format, 'PNG')
        self.assertEqual(result.original_mime_type, 'image/png')
        self.assertEqual(result.output_name.split('.')[-1], 'webp')
        self.assertGreater(result.original_size_bytes, result.output_size_bytes)

    def test_upload_view_converts_valid_image(self):
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root, MEDIA_URL='/media/'):
                response = self.client.post('/', {'image': make_png_upload()})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Готово')
        self.assertContains(response, 'PNG / image/png')

# Create your tests here.
