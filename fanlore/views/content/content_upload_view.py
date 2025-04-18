import logging
import os

import cloudinary.uploader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from fanlore.forms.upload_content_form import ContentUploadForm
from fanlore.models import Content, ContentFile

logger = logging.getLogger(__name__)


class ContentUploadView(LoginRequiredMixin, CreateView):
    """
    View for uploading new content.
    Only authenticated users can access this page.
    """
    model = Content
    form_class = ContentUploadForm
    template_name = 'fanlore/content_upload.html'
    success_url = reverse_lazy('content_list')
    login_url = '/signin'

    def get_form_kwargs(self):
        """
        Inject the current user into the form's kwargs.
        Useful for filtering available collaborators or tags based on user.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass current user to the form
        return kwargs

    def form_valid(self, form):
        """
        Process the form if valid:
        - Assign creator
        - Upload optional topic image
        - Upload optional attached files
        """
        content = form.save(commit=False)
        content.creator = self.request.user  # Assign current user as creator
        content.save()
        form.save_m2m()  # Save collaborators and tags

        # Handle topic_img upload
        topic_img = self.request.FILES.get('topic_img')
        if topic_img:
            try:
                uploaded_image = cloudinary.uploader.upload(
                    topic_img.read(),
                    folder="content_images/",
                    public_id=str(content.id),
                    overwrite=True,
                    resource_type="image"
                )
                content.topic_img = uploaded_image.get("secure_url")
                content.save()
            except Exception as e:
                logger.error(f"Error uploading topic image: {e}")

        # Handle content_files upload
        content_files = self.request.FILES.getlist('content_files')
        for file in content_files:
            try:
                filename, _ = os.path.splitext(file.name)
                public_id = f"{content.id}_{filename}"

                uploaded_file = cloudinary.uploader.upload(
                    file.read(),
                    folder="content_files/",
                    public_id=public_id,
                    overwrite=True,
                    resource_type="auto"
                )
                ContentFile.objects.create(
                    content=content,
                    file=uploaded_file.get("secure_url")
                )
            except Exception as e:
                logger.error(f"Error uploading file {file.name}: {e}")

        return super().form_valid(form)
