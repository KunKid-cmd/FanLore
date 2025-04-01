from django import forms
from pagedown.widgets import PagedownWidget
from ..models import Content, Tag, Category


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


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
    description = forms.CharField(widget=PagedownWidget())  # keep PagedownWidget intact
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={"placeholder": "Enter tags separated by commas"})
    )
    category = forms.ChoiceField(
        choices=Category.choices,
        required=True,
        widget=forms.Select()
    )

    class Meta:
        model = Content
        fields = ['title', 'description', 'topic_img', 'category', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add 'form-control' class to fields except the markdown field
        for name, field in self.fields.items():
            if not isinstance(field.widget, PagedownWidget):
                field.widget.attrs['class'] = 'form-control'

        # Enable multiple file selection
        self.fields['content_files'].widget.attrs['multiple'] = True

    def save(self, commit=True):
        content = super().save(commit=False)
        if commit:
            content.save()

            # Handle tags
            tag_input = self.cleaned_data['tags']
            if tag_input:
                tag_names = {t.strip() for t in tag_input.split(",") if t.strip()}
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    content.tags.add(tag)

        return content
