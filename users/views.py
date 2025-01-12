from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    # reverse_lazy Формирует маршрут только тогда, когда пользователю надо отдать страницу
    # success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    # form_valid этот метод отработает после того, как пройдет форму валидацию и проверит
    # есть ли такой пользователь в системе
    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()
        if user:
            auth.login(self.request, user)

            if session_key:
                # Удалить предыдущую корзину от известной сессии
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # Авторизация нового пользователя от новой сессии
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")

            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context


# CreateView не только для создания нового пользователя, а для любого внесения изменений в БД
class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    # функция для валидности пользователя и регистрации
    def form_valid(self, form):
        # забираем сессионный ключ
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы!")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'
        context['orders'] = (Order.objects.filter(
            user=self.request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related("product"),)).order_by("-id"))
        return context


# для отдельной кнопки корзины в основной странице
class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'


# Остается как функция, потому что при использовании Django 4-5 есть такой класс как LogoutView.
# Есть такая особенность этого класса, чтобы он отработал необходимо отсылать на него POST запрос (не GET)
# с CSRF токеном, сделать скрытый input кнопки. В этом проекте так не стали делать
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))

# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#
#             session_key = request.session.session_key
#
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, Вы вошли в аккаунт")
#
#                 if session_key:
#                     # Удалить предыдущую корзину от известной сессии
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # Авторизация нового пользователя от новой сессии
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#
#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))
#
#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Home - Авторизация',
#         'form': form,
#     }
#
#     return render(request, 'users/login.html', context)


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#
#             session_key = request.session.session_key
#
#             user = form.instance
#             auth.login(request, user)
#
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
#
#             messages.success(request, f"{user.username}, Вы успешно зарегистрированы!")
#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'title': 'Home - Регистрация',
#         'form': form,
#     }
#
#     return render(request, 'users/registration.html', context)


# @login_required  # этот декоратор проверяет авторизован ли пользователь, если не авторизован то page_not_found
# страница
# def profile(request):
#   if request.method == "POST":
#       form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#           if form.is_valid():
#               form.save()
#               messages.success(request, "Профайл успешно обновлен")
#           return HttpResponseRedirect(reverse('user:profile'))
#           else:
#           form = ProfileForm(instance=request.user)
#
#     orders = (Order.objects.filter(user=request.user).prefetch_related(Prefetch(
#         'orderitem_set', queryset=OrderItem.objects.select_related("product"),
#     )).order_by("-id"))
#
#     context = {
#         'title': 'Home - Кабинет',
#         'form': form,
#         'orders': orders,
#     }
#
#     return render(request, 'users/profile.html', context)

