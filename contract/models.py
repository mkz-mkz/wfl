from django.db import models
from django.db.models import DO_NOTHING

from workflows.models import WorkflowInitialization, ContractWorkflowProgress, WorkflowTask


class StatusEnum(models.TextChoices):
    NEW = ("NEW", "New")
    DRAFT = ("DFT", "Draft")
    WIP = ("WIP", "Work in progress")
    CLOSED = ("CLO", "Closed")


class ProjectTypeEnum(models.TextChoices):
    INVEST = ("invest", "Investment")
    IT = ("IT", "Information Technology")
    CAPITAL = ("cap", "Capital Construction")
    EXP = ("exp", "Expenses")
    SERVICE = ("service", "Service")


class Company(models.Model):
    code = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    business_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.code}"


class Project(models.Model):
    code = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    type = models.CharField(max_length=30, choices=ProjectTypeEnum.choices, null=True, blank=True)
    manager = models.CharField(max_length=30, null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_finish = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.code}"


class Contract(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    number = models.CharField(max_length=300, null=True, blank=True)
    client = models.CharField(max_length=300, null=True, blank=True)
    contractor = models.CharField(max_length=300, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=DO_NOTHING, null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    scope = models.CharField(max_length=300, null=True, blank=True)
    sign_off_date = models.DateField(null=True, blank=True)
    lifecycle = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusEnum.choices, null=True, blank=True)
    manager = models.CharField(max_length=300, null=True, blank=True)
    department = models.CharField(max_length=300, null=True, blank=True)
    budget = models.CharField(max_length=300, null=True, blank=True)
    cost_code = models.CharField(max_length=30, null=True, blank=True)
    milestones = models.CharField(max_length=300, null=True, blank=True)
    addendum = models.CharField(max_length=300, null=True, blank=True)
    reference = models.CharField(max_length=300, null=True, blank=True)

    workflow = models.ForeignKey('workflows.Workflow', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="contracts", verbose_name="Workflow")  # Lazy reference
    current_step = models.ForeignKey('workflows.WorkflowStep', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="current_contracts",
                                     verbose_name="Current Workflow Step")  # Lazy reference

    def __str__(self):
        return f"{self.number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.initialize_workflow()

    def initialize_workflow(self):
        """
        Initialize the workflow if the contract meets the initialization criteria.
        """
        if not self.workflow or not self.current_step:
            initialization = WorkflowInitialization.objects.filter(workflow=self.workflow).first()
            if initialization and initialization.can_initialize(self):
                # Get the initial step (lowest sequence number)
                initial_step = self.workflow.steps.order_by('sequence').first()
                if initial_step:
                    self.current_step = initial_step
                    self.current_step.status = 'open'
                    self.save()

                    # Create ContractWorkflowProgress
                    ContractWorkflowProgress.objects.create(
                        contract=self,
                        step=initial_step,
                        status='open',
                        assigned_user=initial_step.assigned_user
                    )

                    # Create initial task for the first step
                    WorkflowTask.objects.create(
                        contract=self,
                        step=initial_step,
                        assigned_user=initial_step.assigned_user,
                        description=f"Complete the task for step {initial_step.name}"
                    )
