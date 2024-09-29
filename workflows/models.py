from django.db import models
from django.contrib.auth.models import User


class Workflow(models.Model):
    name = models.CharField(max_length=255, verbose_name="Workflow Name")
    description = models.TextField(null=True, blank=True, verbose_name="Workflow Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="steps")
    name = models.CharField(max_length=255, verbose_name="Step Name")
    description = models.TextField(null=True, blank=True, verbose_name="Step Description")
    sequence = models.PositiveIntegerField(verbose_name="Step Sequence Number")
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Assigned User")
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='open', verbose_name="Step Status")

    def __str__(self):
        return f"{self.workflow.name} - {self.name}"


class WorkflowStepReturnCode(models.Model):
    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name="return_codes")
    code = models.CharField(max_length=10, verbose_name="Return Code")
    description = models.TextField(null=True, blank=True, verbose_name="Return Code Description")
    next_step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, blank=True, related_name="previous_return_codes", verbose_name="Next Step")

    def __str__(self):
        return f"{self.code} - {self.step.name} -> {self.next_step.name if self.next_step else 'End'}"


class WorkflowInitialization(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="initializations")
    required_project_type = models.CharField(max_length=50, choices=[('IT', 'Information Technology'), ('CAP', 'Capital Construction')], verbose_name="Required Project Type")
    required_contract_status = models.CharField(max_length=50, choices=[('NEW', 'New'), ('WIP', 'Work in progress'), ('CLO', 'Closed')], verbose_name="Required Contract Status")

    def __str__(self):
        return f"Initialization for {self.workflow.name}"

    def can_initialize(self, contract):
        return contract.project.type == self.required_project_type and contract.status == self.required_contract_status


class ContractWorkflowProgress(models.Model):
    contract = models.ForeignKey('contract.Contract', on_delete=models.CASCADE, related_name="workflow_progress")  # Lazy reference
    step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, blank=True, related_name="contract_progress")
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
    return_code = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="workflow_progress_steps")

    def __str__(self):
        return f"{self.contract.number} - {self.step.name if self.step else 'No Step'} - {self.status}"


class WorkflowTask(models.Model):
    contract = models.ForeignKey('contract.Contract', on_delete=models.CASCADE, related_name="workflow_tasks")  # Lazy reference
    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name="tasks")
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workflow_tasks")
    description = models.TextField(verbose_name="Task Description")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task for {self.assigned_user.username} - {self.step.name} - {self.contract.number}"
