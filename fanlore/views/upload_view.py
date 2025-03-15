# views.py
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import cloudinary.uploader
from ..models import Content, ContentFile
from ..forms.upload_content_form import ContentUploadForm


class ContentUploadView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentUploadForm
    template_name = 'fanlore/upload_content.html'
    success_url = reverse_lazy('content_list')
    login_url = '/signin'

    def form_valid(self, form):
        # Save the Content instance
        content = form.save(commit=False)
        content.collaborator = self.request.user
        content.save()

        # Handle the topic_img upload to Cloudinary
        topic_img = self.request.FILES.get('topic_img')
        if topic_img:
            try:
                with topic_img.open('rb') as file:
                    uploaded_image = cloudinary.uploader.upload(
                        file,
                        folder="content_images/",
                        public_id=str(content.id),
                        overwrite=True,
                        resource_type="image"
                    )
                    content.topic_img = uploaded_image.get("secure_url")
            except Exception as e:
                print(f"Error uploading topic image: {e}")

        # Handle multiple file uploads for content_files
        content_files = self.request.FILES.getlist('content_files')
        for file in content_files:
            try:
                # Upload each file to Cloudinary
                with file.open('rb') as f:
                    uploaded_file = cloudinary.uploader.upload(
                        f,
                        folder="content_files/",
                        public_id=f"{content.id}_{file.name}",
                        overwrite=True,
                        resource_type="auto"
                    )
                    # Create a ContentFile instance for each uploaded file
                    ContentFile.objects.create(
                        content=content,
                        file=uploaded_file.get("secure_url")
                    )
            except Exception as e:
                print(f"Error uploading file {file.name}: {e}")

        content.save()  # Save the content after assigning the image URL
        return super().form_valid(form)
