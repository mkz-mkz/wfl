from django.contrib import admin
from workflows import (
    models
)


class WorkflowItemAdmin(admin.ModelAdmin):
    list_display = (
        "base_class",
        "project",
        "workflow",
        "description",
        "is_workflow",
        "active",
    )


class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = (
        "get_workflow",
        "get_workflow_setup",
        "sequence_nr",
        "completed_by",
        "reaction_time",
        "status_code",
        "disable_comments"
    )

    @admin.display(description="Workflow Step")
    def get_workflow(self, obj):
        return obj.workflow.workflow

    @admin.display(description="Workflow Step")
    def get_workflow_setup(self, obj):
        return obj.workflow_setup.workflow.workflow


class WorkflowStepInline(admin.StackedInline):
    model = models.WorkflowStep
    extra = 0
    show_change_link = True

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "workflow",
                "workflow_setup__workflow",
                # "status_code"
            )
        )


class WorkflowSetupAdmin(admin.ModelAdmin):
    list_display = (
        "get_workflow",
    )
    inlines = [WorkflowStepInline]

    @admin.display(description="Workflow Setup")
    def get_workflow(self, obj):
        return obj.workflow.workflow


admin.site.register(models.WorkflowItem, WorkflowItemAdmin)
admin.site.register(models.WorkflowStep, WorkflowStepAdmin)
admin.site.register(models.WorkflowSetup, WorkflowSetupAdmin)
