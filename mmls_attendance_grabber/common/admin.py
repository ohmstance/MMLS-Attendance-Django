from django.contrib import admin

# Register your models here.

# Skips call to locked_by_pid which kills process_tasks in Windows
from background_task.admin import TaskAdmin, CompletedTaskAdmin
fields = ['task_name', 'task_params', 'run_at', 'priority', 'attempts', 'has_error', 'locked_by', ]
TaskAdmin.list_display = fields
CompletedTaskAdmin.list_display = fields