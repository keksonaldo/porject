from django.shortcuts import render

from .forms import ImageUploadForm
from .services import ImageConversionError, convert_upload_to_webp


def upload_image(request):
    result = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                result = convert_upload_to_webp(form.cleaned_data['image'])
            except ImageConversionError as exc:
                form.add_error('image', str(exc))
    else:
        form = ImageUploadForm()

    return render(
        request,
        'converter/upload.html',
        {
            'form': form,
            'result': result,
        },
    )
