from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from myapp.forms import *


class NoteListViewNotLogin(ListView):
    model = Note
    template_name = 'NotLog.html'
    paginate_by = 5
    ordering = ['-id']


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'


class Register(CreateView):
    form_class = UserCreation
    template_name = 'register.html'
    success_url = '/accounts/profile/'
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_staff = True
        obj.save()
        return super().form_valid(form=form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class NoteListViewForLogin(LoginRequiredMixin, NoteListViewNotLogin):

    def get(self, *args, **kwargs):

        if self.request.user.is_superuser:
            self.template_name='AdminIndex.html'
            self.extra_context={'create_form': NoteCreateForm(),
                                'returns': ReturnBuy.objects.count()}

        else:
            self.template_name='index.html'
            self.extra_context={'create_form':TovarForm(),
                                'object': NoteListViewForLogin(),
                                'User': User.objects.get(username=self.request.user)}
        return super(NoteListViewForLogin, self).get(*args, **kwargs)



class NoteCreateView(LoginRequiredMixin, CreateView):
    login_url = 'adminindex/'
    http_method_names = ['post']
    form_class = NoteCreateForm
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form=form)

class TovarBuy(LoginRequiredMixin,CreateView):
    form_class = TovarForm
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        obj=form.save(commit=False)
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj.buy = self.get_object(pk)
        if obj.buy.instock<obj.quantity:
            return HttpResponse('No this quantity instock')
        obj.author = User.objects.get(username=self.request.user)
        obj2=Note.objects.get(id=pk)
        obj2.instock-=obj.quantity
        obj.author.money -= obj.quantity*obj2.price
        if obj.author.money<0:
            return HttpResponse('No money')

        obj.author.save()
        obj2.save()
        obj.save()
        return super(TovarBuy, self).form_valid(form=form)

    def get_object(self, queryset=None):
        return Note.objects.get(id=queryset)


class UpdateNote(LoginRequiredMixin,UpdateView):
    model = Note
    fields = ['title','text','instock','price']
    template_name = 'Update.html'
    extra_context = {'Note':NoteCreateForm()}
    success_url = '/accounts/profile/'


def gettime():
       allbue=Buy.objects.all()
       for i in allbue:
           if datetime.datetime.now()-i.timeOfBuy - datetime.timedelta(minutes=3)>\
                   datetime.timedelta(minutes=0):
               i.canReturn=False
               i.save()


class MyBuyView(LoginRequiredMixin,ListView):

    template_name = 'YouBuy.html'
    form_class = TovarReturn
    model = Buy

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            gettime()
            self.extra_context = {'form': TovarReturn(),
                     'User': User.objects.get(username=self.request.user)}
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)



class ReturnOneBuy(LoginRequiredMixin,DeleteView):
    model = Buy
    success_url = '/mybuy/'

    def objcreate(self):
        self.object = self.get_object()
        self.model = ReturnBuy
        obj = self.model()
        obj.author = User.objects.get(username=self.request.user)
        obj.returnBuy = self.object
        obj2=Buy.objects.get(id=obj.returnBuy_id)
        obj2.canReturn=False
        obj2.save()
        print(obj.returnBuy)
        print(obj.author)
        obj.save()


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.objcreate()
        return HttpResponseRedirect(success_url)


class ReturnCheck(LoginRequiredMixin, ListView):
    model = ReturnBuy
    template_name = 'ReturnCheck.html'

class NotReturn(LoginRequiredMixin,DeleteView):
    model = ReturnBuy
    success_url = '/returncheck'
    def get_success_url(self):
        if ReturnBuy.objects.count() == 1:
            self.success_url='/accounts/profile/'
        return super(NotReturn, self).get_success_url()


class AcceptReturn(LoginRequiredMixin,DeleteView):
    model = ReturnBuy
    success_url = '/returncheck'
    def get_success_url(self):
        if ReturnBuy.objects.count() == 1:
            self.success_url = '/accounts/profile/'
        return super(AcceptReturn, self).get_success_url()


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        objUser=User.objects.get(id=self.object.author_id)
        objBuy = Buy.objects.get(id=self.object.returnBuy_id)
        objTovar=Note.objects.get(id=objBuy.buy_id)
        objTovar.instock+=objBuy.quantity
        objUser.money+=objBuy.quantity*objTovar.price


        objTovar.save()
        objUser.save()
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.get(self,request,*args,**kwargs)

        self.object.delete()
        Buy.objects.get(id=self.object.returnBuy_id).delete()
        return HttpResponseRedirect(success_url)


