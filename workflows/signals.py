from django.db.models.signals import post_save
from django.dispatch import receiver
from contract.models import Contract
from workflows.models import WorkflowStep, ContractWorkflowProgress


@receiver(post_save, sender=Contract)
def initialize_contract_workflow(sender, instance, created, **kwargs):
    if created and instance.workflow:
        # Get the initial step (lowest sequence number)
        initial_step = instance.workflow.steps.order_by('sequence').first()
        if initial_step:
            instance.current_step = initial_step
            instance.current_step.status = StepStatus.OPEN
            instance.current_step.save()
            instance.save()

            # Log the initial step
            ContractWorkflowProgress.objects.create(
                contract=instance,
                step=initial_step,
                status=StepStatus.OPEN,
                assigned_user=initial_step.assigned_user
            )
