from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from tasks.models import Task


class GenericTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 3

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        current_tasks = Task.objects.filter(
            deleted=False, user=self.request.user
        ).order_by("completed", "priority")
        if search_term:
            current_tasks = current_tasks.filter(title__icontains=search_term)
        return current_tasks
    
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        completed = Task.objects.filter(
            deleted=False, user=self.request.user, completed=True
        ).count
        context["completed"] = completed
        return context
