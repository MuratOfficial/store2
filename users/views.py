from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.custom import TitleMixin
from products.models import Basket

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class LoginUserView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    title = 'Store - Авторизация'
    form_class = UserLoginForm

# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         "title": "Store - Авторизация",
#         "form": form,
#     }
#     return render(request, 'users/login.html', context)


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = "Store - Регистрация"
    success_message = 'Аккаунт создан успешно!'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    title = "Store - Профиль"

    def get_success_url(self):
        success_url = reverse_lazy('users:profile', args=(self.object.id,))
        return success_url

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user)
        context['total_quantity'] = sum(basket.quantity for basket in context["baskets"])
        context['total_sum'] = sum(basket.sum() for basket in context["baskets"])
        return context

# @login_required
# def profile(request):
#     user = request.user
#     if request.method == "POST":
#         form = UserProfileForm(data=request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     baskets = Basket.objects.filter(user=user)
#     total_quantity = sum(basket.quantity for basket in baskets)
#     total_sum = sum(basket.sum() for basket in baskets)
#     context = {
#         "title": "Профиль",
#         "form": form,
#         "baskets": baskets,
#         "total_quantity": total_quantity,
#         "total_sum": total_sum,
#     }
#     return render(request, 'users/profile.html', context)

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Email Verification'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# Create your views here.
