from django.utils import timezone
from django.views.generic.detail import DetailView
from fanlore.models import Event, EventSubmission
from fanlore.forms.event_submission_form import EventSubmissionForm


class EventDetailView(DetailView):
    model = Event
    template_name = "fanlore/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user
        now = timezone.now()

        is_open = event.is_open()
        can_submit = is_open and (event.allow_text or event.allow_file)
        has_started = event.submission_start is None or event.submission_start <= now
        has_ended = event.submission_end is not None and event.submission_end < now
        is_creator = user.is_authenticated and user == event.creator

        user_submission = None
        if user.is_authenticated:
            user_submission = EventSubmission.objects.filter(event=event,
                                                             user=user).first()

        show_submissions = event.show_submissions or is_creator
        submissions = event.submissions.all() if show_submissions else []

        submission_form = None
        # views/event_detail_view.py

        if can_submit and user.is_authenticated:
            if user_submission:
                # Pass instance to pre-fill the form for editing
                submission_form = EventSubmissionForm(instance=user_submission,
                                                      event=event)
            else:
                # New submission
                submission_form = EventSubmissionForm(event=event)

        context.update({
            "is_open": is_open,
            "can_submit": can_submit,
            "has_started": has_started,
            "has_ended": has_ended,
            "is_creator": is_creator,
            "user_submission": user_submission,
            "submissions": submissions,
            "submission_form": submission_form,
            "show_submissions": show_submissions,
        })
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        show_sub = form.cleaned_data.get('show_submissions', False)
        form.instance.show_submissions = show_sub
        return super().form_valid(form)
