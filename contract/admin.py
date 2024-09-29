from django.contrib import admin
from contract.models import Contract, Company, Project
from django.shortcuts import render, redirect
from django.urls import path
from contract.models import Contract

if admin.site.is_registered(Contract):
    admin.site.unregister(Contract)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'business_id']
    search_fields = ['code', 'name', 'business_id']
    # Optionally include other configurations


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'type', 'manager', 'budget']
    search_fields = ['name', 'code']
    list_filter = ['type']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'client', 'contractor', 'project', 'workflow', 'current_step', 'status']
    list_filter = ['workflow', 'status', 'project']
    search_fields = ['number', 'title', 'client', 'contractor', 'project__name']
    autocomplete_fields = ['workflow', 'current_step']
    readonly_fields = ['workflow', 'current_step']
    actions = ['transition_workflow']

    def transition_workflow(self, request, queryset):
        if 'apply' in request.POST:
            form = ReturnCodeForm(request.POST)
            if form.is_valid():
                return_code = form.cleaned_data['return_code']
                selected = request.POST.getlist('_selected_action')
                contracts = Contract.objects.filter(pk__in=selected)
                for contract in contracts:
                    try:
                        contract.transition_step(return_code, user=request.user)
                        self.message_user(request, f"Contract '{contract.number}' transitioned successfully.", messages.SUCCESS)
                    except Exception as e:
                        self.message_user(request, f"Error transitioning contract '{contract.number}': {str(e)}", messages.ERROR)
                return redirect(request.get_full_path())
        else:
            selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
            if not selected:
                self.message_user(request, "No contracts selected.", messages.WARNING)
                return redirect(request.get_full_path())
            form = ReturnCodeForm(initial={'_selected_action': selected})
        return render(request, 'admin/transition_workflow.html', {'contracts': queryset, 'form': form, 'title': 'Transition Workflow'})

    transition_workflow.short_description = "Transition selected contracts to next workflow step"

