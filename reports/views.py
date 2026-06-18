from django.shortcuts import render
from .forms import  ReportForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_reports import  create_report, get_reports

def report_list(request):
    reports = get_reports()
    context = {
        'report_list': reports
    }
    return render(request, 'Measurement/reports.html', context)

def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            create_report(form)
            messages.add_message(request, messages.SUCCESS, 'Report create successful')
            return HttpResponseRedirect(reverse('reportCreate'))
        else:
            print(form.errors)
    else:
        form = ReportForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/reportCreate.html', context)
