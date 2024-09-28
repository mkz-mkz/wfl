from xml.dom import ValidationErr

from django.db import models
# from django.contrib.auth.models import Group
# from django.core.exceptions import ValidationError
"""Minimal additional imports"""
# from accounts.models import Company
# from number_composition import SubClass
# from project.models import Project
# from systems.models import ApprovalCode, BaseClass, Discipline, StatusCode, TransmittalCode, TypeCode
# from users.model import User


class BaseClassEnum(models.TextChoices):
    CM = (
        "CM", "Contracts Management"
    )
    PM = "PM", "Project Management"


class ProjectEnum(models.TextChoices):
    ABC = (
        "ABC", "Initial Test Project"
    )
    SK1 = (
        "SK1", "Second Test Project"
    )


class CompletedByEnum(models.TextChoices):
    ALL = (
        "all", "all persons to commit"
    )
    ONE = (
        "one", "one person enough to commit"
    )
    ALR = (
        "alr", "all responsible to commit"
    )
    ENG = (
        "eng", "one responsible to commit"
    )


class WorkflowRole(models.TextChoices):
    APPROVAL = (
        "APPROVAL", "Approval"
    )
    CHECKER = (
        "CHECKER", "Checker"
    )
    CREATOR = (
        "CREATOR", "Creator"
    )
    REVIEWER = (
        "REVIEWER", "Reviewer"
    )


class StepStatusEnum(models.TextChoices):
    IN_PROGRESS = (
        "WIP", "Work in Progress"
    )
    IS_FINISHED = (
        "FIN", "Finished"
    )


class StatusCodeEnum(models.TextChoices):
    NEW = (
        "NEW", "New"
    )
    OUT = (
        "OUT", "Outstanding"
    )
    CLOSED = (
        "CLO", "Closed"
    )
    REJECTED = (
        "REJ", "Rejected"
    )


class WorkflowItem(models.Model):
    class Meta:
        verbose_name = "WFL Item"
        verbose_name_plural = "WFL Items"
        constraints = [
            models.UniqueConstraint(
                fields=["base_class", "workflow"],
                name="base_class_wf_item_uniq",
            ),
            models.UniqueConstraint(
                fields=["project", "workflow"],
                name="project_wf_item_uniq",
            )
        ]
    base_class = models.CharField(max_length=30, choices=BaseClassEnum.choices)
    project = models.CharField(max_length=3, choices=ProjectEnum.choices)
    workflow = models.CharField(max_length=100, verbose_name="workflow item name")
    description = models.TextField(null=True, blank=True)
    is_workflow = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.workflow}"


class WorkflowSetup(models.Model):
    class Meta:
        verbose_name = "WFL set-up"
        verbose_name_plural = "WFL set-ups"

    workflow = models.ForeignKey(WorkflowItem, on_delete=models.CASCADE, related_name="wf_setups")

    def __str__(self):
        return f"{self.workflow}"

    # def save(self, **kwargs):
    #     self.clean()
    #     super().save(**kwargs)
    #
    # def clean(self):
    #     super().clean()
    #     self.workflow: WorkflowItem
    #
    #     self.workflow.is_workflow = True
    #     self.workflow.save()




class WorkflowStep(models.Model):
    class Meta:
        verbose_name = "WFL step"
        verbose_name_plural = "WFL steps"
        constraints = [
            models.UniqueConstraint(
                fields=["workflow_setup", "sequence_nr"],
                name="wf_setup_sequence_nr_uniq",
            )
        ]

    workflow = models.ForeignKey(WorkflowItem, on_delete=models.CASCADE, related_name="wf_steps")
    workflow_setup = models.ForeignKey(WorkflowSetup, on_delete=models.CASCADE, related_name="wf_setup_steps")
    sequence_nr = models.IntegerField()
    completed_by = models.CharField(max_length=20, choices=CompletedByEnum.choices)
    is_multiple_persons = models.BooleanField(default=False)
    reaction_time = models.IntegerField(blank=True, null=True)
    status_code = models.CharField(max_length=30, choices=StatusCodeEnum.choices)
    disable_comments = models.BooleanField(default=False)

    # def save(self, **kwargs):
    #     self.clean()
    #     super().save(**kwargs)
    #
    # def clean(self):
    #     super().clean()
    #     workflow_item = WorkflowItem.objects.select_related(
    #         "base_class", "project"
    #     ).get(pk=self.workflow.pk)
    #     workflow_setup_item = WorkflowItem.objects.select_related(
    #         "base_class", "project"
    #     ).get(pk=self.workflow_setup.workflow.pk)
    #
    #     if workflow_item.project != workflow_setup_item.project:
    #         raise ValidationErr("Step workflow and Setup Workflow must be unique")

    def __str__(self):
        return f"{self.workflow}"


class StepParameter(models.Model):
    pass


class StepAction(models.Model):
    pass


class StepControl(models.Model):
    pass


class WorkflowInbox(models.Model):
    pass


class Initialization(models.Model):
    pass


class RevisionWorkflow(models.Model):
    pass

