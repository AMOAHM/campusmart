from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import SystemLog


@login_required
@require_http_methods(["GET"])
def logs_view(request):
    if request.user.role != 'admin':
        return render(request, 'errors/403.html', status=403)
    
    logs = SystemLog.objects.all()[:100]
    context = {'logs': logs}
    return render(request, 'logs/logs.html', context)
