from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView,UpdateView,CreateView,DeleteView,DetailView
from django.core.mail import send_mail
from main.models import Plant
from authentication.models import User
from django.shortcuts import render

class my_plants(ListView):
    model = Plant
    template_name = 'main/my_plants.html'
    fields = ['name', 'category', 'age', 'image', 'health']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = get_object_or_404(User, pk=request.session['user_id'])
        except:
            self.user = user = User.objects.get(name='Guest')
        Plant.objects.filter(owner=None).update(owner=self.user)
        return super(my_plants, self).dispatch(request, *args, **kwargs)

class add_plants(CreateView):
    model = Plant
    template_name = 'main/add_plants.html'
    fields = ['name', 'category', 'age', 'image', 'health']

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Plant.objects.order_by('id')
        return super(add_plants, self).get_context_data(**kwargs)


class delete_plants(DeleteView):
    model = Plant
    template_name = 'main/delete_plants.html'
    fields = ['name', 'category', 'age', 'image', 'health']
    success_url = reverse_lazy('main:my_plants')

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Plant.objects.order_by('id')
        return super(delete_plants, self).get_context_data(**kwargs)

class manage_plants(UpdateView):
    model = Plant
    template_name = 'main/manage_plants.html'
    fields = ['name', 'category', 'age', 'image', 'health']

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Plant.objects.order_by('id')
        return super(manage_plants, self).get_context_data(**kwargs)

class plants_care(ListView):
    model = Plant
    template_name = 'main/plant_care.html'
    fields = ['name', 'category', 'age', 'image', 'health']
    
    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Plant.objects.order_by('id')
        return super(plants_care, self).get_context_data(**kwargs)

def diagnoseView(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    plant.diagnose = True
    plant.save()
    send_mail(
        "Health Diagnosis",
        f"Hello, \n\nThe user:{plant.owner.name}({plant.owner.email}) has requested the health diagnosis for '{plant.name}',\nPlease check the detail at Smartplanting.net as admin.\n\nThank you!",
        "rundi.liu26@gmail.com",
        ["rundi.liu26@visionx.org"]
    )
    return HttpResponseRedirect(reverse('main:my_plants'))