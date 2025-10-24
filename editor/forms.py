from django import forms


class UploadForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)
    image = forms.ImageField()
    brightness = forms.FloatField(initial=1.0, min_value=0.0, max_value=3.0,
                                   widget=forms.NumberInput(attrs={
                                       'type': 'range', 'min': '0', 'max': '3', 'step': '0.01', 'class': 'range-input'
                                   }))
    contrast = forms.FloatField(initial=1.0, min_value=0.0, max_value=3.0,
                                widget=forms.NumberInput(attrs={
                                    'type': 'range', 'min': '0', 'max': '3', 'step': '0.01', 'class': 'range-input'
                                }))
    saturation = forms.FloatField(initial=1.0, min_value=0.0, max_value=3.0,
                                  widget=forms.NumberInput(attrs={
                                      'type': 'range', 'min': '0', 'max': '3', 'step': '0.01', 'class': 'range-input'
                                  }))


class ObjectRemovalForm(forms.Form):
    # Allow either selecting an existing asset by id or uploading a new image to process.
    asset_id = forms.IntegerField(required=False)
    image = forms.ImageField(required=False)
    mask = forms.ImageField(help_text='Upload a black/white mask where white = area to remove')
