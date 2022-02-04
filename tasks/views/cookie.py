from django.http import HttpResponse


def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views + 1
    return HttpResponse(f"Total views is {total_views} and the user is {request.user}")


# def completed_tasks_view(request):
#     completed_tasks = Task.objects.filter(completed=True)
#     return render(request, "completed.html", {"tasks": completed_tasks})


# def complete_task_view(request, index):
#     Task.objects.filter(id=index).update(completed=True)
#     return HttpResponseRedirect("/tasks")


# def all_tasks_view(request):
#     current_tasks = Task.objects.filter(deleted=False).filter(completed=False)
#     completed_tasks = Task.objects.filter(completed=True)
#     return render(
#         request,
#         "all_tasks.html",
#         {"current": current_tasks, "completed": completed_tasks},
#     )
