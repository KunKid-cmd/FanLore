# forms.py
from django import forms
from ..models import Content, ContentFile


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Enable multiple file selection


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if data is None:
            return []
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ContentUploadForm(forms.ModelForm):
    content_files = MultipleFileField(label='Upload Files', required=False)

    class Meta:
        model = Content
        fields = ['title', 'description', 'topic_img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # Add 'multiple' attribute to content_files field
        self.fields['content_files'].widget.attrs['multiple'] = True
