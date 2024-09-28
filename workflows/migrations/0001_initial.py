# Generated by Django 5.1.1 on 2024-09-26 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Initialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RevisionWorkflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StepAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StepControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StepParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowInbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_class', models.CharField(choices=[('CM', 'Contracts Management'), ('PM', 'Project Management')], max_length=30)),
                ('project', models.CharField(choices=[('ABC', 'Initial Test Project'), ('SK1', 'Second Test Project')], max_length=3)),
                ('workflow', models.CharField(max_length=100, verbose_name='workflow item name')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_workflow', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'WFL Item',
                'verbose_name_plural': 'WFL Items',
                'constraints': [models.UniqueConstraint(fields=('base_class', 'workflow'), name='base_class_wf_item_uniq'), models.UniqueConstraint(fields=('project', 'workflow'), name='project_wf_item_uniq')],
            },
        ),
        migrations.CreateModel(
            name='WorkflowSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_setups', to='workflows.workflowitem')),
            ],
            options={
                'verbose_name': 'WFL set-up',
                'verbose_name_plural': 'WFL set-ups',
            },
        ),
        migrations.CreateModel(
            name='WorkflowStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_nr', models.IntegerField()),
                ('completed_by', models.CharField(choices=[('all', 'all persons to commit'), ('one', 'one person enough to commit'), ('alr', 'all responsible to commit'), ('eng', 'one responsible to commit')], max_length=20)),
                ('is_multiple_persons', models.BooleanField(default=False)),
                ('reaction_time', models.IntegerField(blank=True, null=True)),
                ('status_code', models.CharField(choices=[('NEW', 'New'), ('OUT', 'Outstanding'), ('CLO', 'Closed'), ('REJ', 'Rejected')], max_length=30)),
                ('disable_comments', models.BooleanField(default=False)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_steps', to='workflows.workflowitem')),
                ('workflow_setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_setup_steps', to='workflows.workflowsetup')),
            ],
            options={
                'verbose_name': 'WFL step',
                'verbose_name_plural': 'WFL steps',
                'constraints': [models.UniqueConstraint(fields=('workflow_setup', 'sequence_nr'), name='wf_setup_sequence_nr_uniq')],
            },
        ),
    ]
