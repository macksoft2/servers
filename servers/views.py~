# Create your views here.
from django.http import HttpResponse
from servers.models import Server
from django.template import Context, loader, RequestContext
from django.forms import ModelForm
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
class ServerForm (ModelForm):
    class Meta:
        model = Server
def index(request):
    list_servers = Server.objects.all()
    t = loader.get_template('index.html')
    c = Context({
        'list_servers': list_servers,
    })
    return HttpResponse(t.render(c))

def add(request):
    if request.method=='POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            list_servers = Server.objects.all()
            return render_to_response('index.html', {'list_servers' : list_servers})
    else:
        server_form = ServerForm()
        return render_to_response('server.html', {'server_form' : server_form},context_instance=RequestContext(request))

def update(request, Server_id):
    
    return HttpResponse(" %s." % Server_id)

def delete(request, Server_id):
    s = Server.objects.get(pk=Server_id)
    s.delete();
    list_servers = Server.objects.all()
    return render_to_response('index.html', {'list_servers' : list_servers})
def default(request):
    return HttpResponseRedirect('accounts/login/')
