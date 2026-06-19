from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label='Фотография',
        help_text='Загрузите одну фотографию в JPG, PNG, GIF, BMP, TIFF или WebP.',
        widget=forms.ClearableFileInput(
            attrs={
                'accept': 'image/*',
                'class': 'file-input',
            }
        ),
    )
