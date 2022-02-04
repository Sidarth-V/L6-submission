from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from tasks.models import Task


class GenericPendingTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "pending_tasks.html"
    context_object_name = "tasks"
    paginate_by = 3

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        current_tasks = Task.objects.filter(
            deleted=False, completed=False, user=self.request.user
        ).order_by("priority")
        if search_term:
            current_tasks = current_tasks.filter(title__icontains=search_term)
        return current_tasks
