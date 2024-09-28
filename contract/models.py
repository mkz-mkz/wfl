from django.db import models
from django.db.models import DO_NOTHING


class StatusEnum(models.TextChoices):
    NEW = (
        "NEW", "New"
    )
    DRAFT = (
        "DFT", "Draft"
    )
    WIP = (
        "WIP", "Work in progress"
    )
    CLOSED = (
        "CLO", "Closed"
    )


class ProjectTypeEnum(models.TextChoices):
    INVEST = (
        "invest", "Investment"
    )
    IT = (
        "IT", "Information Technology"
    )
    CAPITAL = (
        "cap", "Capital Construction"
    )
    EXP = (
        "exp", "Expenses"
    )
    SERVICE = (
        "service", "Service"
    )


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

    def __str__(self):
        return f"{self.number}"
