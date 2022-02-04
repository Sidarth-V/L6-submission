from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from tasks.models import Task


class GenericCompletedTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "completed_tasks.html"
    context_object_name = "tasks"
    paginate_by = 3

    def get_queryset(self):
        current_tasks = Task.objects.filter(
            deleted=False, completed=True, user=self.request.user
        )
        return current_tasks
