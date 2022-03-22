from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from . models import Task
from . forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

#class based views/generic views
#to list on first page
class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'task'

class TaskDetailView(DetailView):
    model=Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get__success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')#name from url
# function base views here.
def list(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        name=request.POST.get('task','')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')

        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request,'index.html',{'task':tasks})

def delete(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task = Task.objects.get(id=id)
    f=TodoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')

    return render(request,'edit.html',{'f':f,'task':task})