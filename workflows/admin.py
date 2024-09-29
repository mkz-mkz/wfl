from django.contrib import admin
from .models import (
    Workflow, WorkflowStep, WorkflowStepReturnCode,
    ContractWorkflowProgress, WorkflowInitialization, WorkflowTask
)

class WorkflowStepReturnCodeInline(admin.TabularInline):
    model = WorkflowStepReturnCode
    fk_name = 'step'
    extra = 1
    autocomplete_fields = ['next_step']

class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'name', 'sequence', 'assigned_user', 'status']
    inlines = [WorkflowStepReturnCodeInline]
    search_fields = ['name', 'assigned_user__username']
    list_filter = ['workflow', 'status']

class WorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
    search_fields = ['name']

class ContractWorkflowProgressAdmin(admin.ModelAdmin):
    list_display = ['contract', 'step', 'status', 'return_code', 'timestamp', 'assigned_user']
    list_filter = ['status', 'return_code']
    search_fields = ['contract__number', 'step__name', 'assigned_user__username']

class WorkflowInitializationAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'required_project_type', 'required_contract_status']
    list_filter = ['workflow', 'required_project_type', 'required_contract_status']
    search_fields = ['workflow__name']

class WorkflowTaskAdmin(admin.ModelAdmin):
    list_display = ['contract', 'step', 'assigned_user', 'description', 'completed']
    list_filter = ['step', 'assigned_user', 'completed']
    search_fields = ['contract__number', 'step__name', 'assigned_user__username']

# Register the models with the admin
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowStep, WorkflowStepAdmin)
admin.site.register(ContractWorkflowProgress, ContractWorkflowProgressAdmin)
admin.site.register(WorkflowInitialization, WorkflowInitializationAdmin)
admin.site.register(WorkflowTask, WorkflowTaskAdmin)
