from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from tasks.models import Task
from tasks.views.createTask import TaskCreateForm, helper


class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)


class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "task_detail.html"


class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_update.html"
    success_url = "/tasks"

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        helper(self.request.user, int(form.cleaned_data.get("priority")), form)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = "/tasks"


class GenericTaskCompleteView(AuthorisedTaskManager, UpdateView):
    model = Task
    fields = ["completed"]
    template_name = "task_complete.html"
    success_url = "/tasks"
