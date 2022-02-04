from pydoc import Helper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.forms import ModelForm
from django.forms import ModelForm, ValidationError
from django.http import HttpResponseRedirect
from tasks.models import Task


class TaskCreateForm(LoginRequiredMixin, ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"]
        return title

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "completed"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get("title").widget.attrs[
            "class"
        ] = "appearance-none rounded-md w-full py-2 px-3 leading-tight bg-[#F1F5F9]"
        self.fields.get("description").widget.attrs[
            "class"
        ] = "appearance-none rounded-md w-full py-2 px-3 leading-tight bg-[#F1F5F9]"
        self.fields.get("priority").widget.attrs[
            "class"
        ] = "appearance-none rounded-md w-full py-2 px-3 leading-tight bg-[#F1F5F9]"
        self.fields.get("completed").widget.attrs[
            "class"
        ] = "appearance-none checked:bg-blue-500 rounded-md py-3 px-3 mr-4 leading-tight bg-[#F1F5F9]"


class GenericTaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = "/tasks"

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.helper(int(form.cleaned_data.get("priority")))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def helper(self, priority):
        if Task.objects.filter(
            deleted=False, user=self.request.user, priority=priority
        ).exists():
            old_task = Task.objects.filter(
                deleted=False, user=self.request.user, priority=priority
            )
            self.helper(priority + 1)
            priority = priority + 1
            old_task.update(priority=priority)
            return
