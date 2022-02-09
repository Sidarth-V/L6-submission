from pydoc import Helper

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
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
        helper(self.request.user, int(form.cleaned_data.get("priority")), form)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def helper(user, priority, form):
    if Task.objects.filter(
        deleted=False, user=user, priority=priority, completed=False
    ).exists():
        old_tasks = (
            Task.objects.filter(
                deleted=False,
                user=user,
                priority__gte=priority,
                completed=False,
            )
            .exclude(pk=form.instance.id)
            .order_by("priority")
            .select_for_update()
        )

        changes = []
        flag = priority
        for task in old_tasks:
            if flag != task.priority:
                break
            task.priority = task.priority + 1
            flag = flag + 1
            changes.append(task)

        with transaction.atomic():
            if changes:
                Task.objects.bulk_update(changes, ["priority"], batch_size=100)

        return
