from ..models import Reports 

def get_reports():
    queryset = Reports.objects.all().order_by('-created_at')[:10]
    return (queryset)

def create_report(form):
    report = form.save()
    report.save()
    return () 
