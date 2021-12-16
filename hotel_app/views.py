from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking
from .forms import AvailabilityForm, LoginForm, UserRegistrationForm,
from hotel_app.booking_functions.availability import check_availability
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('hotel_app:RoomDetailView', kwargs={'category': room_category})
        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    print(room_list)
    return render(request, 'room_list_view.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Wybrany rodzaj pokoju nie istnieje')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            available_rooms = []
            for room in room_list:
                if check_availability(room, data['check_in'], data['check_out']):
                    available_rooms.append(room)

            if len(available_rooms) > 0:
                room = available_rooms[0]
                booking = Booking.objects.create(
                    user=self.request.user,
                    room=room,
                    check_in=data['check_in'],
                    check_out=data['check_out']
                )
                booking.save()
                return HttpResponse(booking)
        else:
            return HttpResponse('Wszystkie pokoje z tej kategorii są już zajęte! Spróbuj wybrać inną.')

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel_app:BookingListView')

#--------

class ListUsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'hotel_app/users.html', {'users': users})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'hotel_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        form.is_valid()
        user = authenticate(username=form.cleaned_data['login'],
                            password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return reverse('/')
        else:
            return render(request, 'hotel_app/login.html', {'form': form, 'message': 'Błędny login lub hasło'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return reverse('/')

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'hotel_app/user_registration_form.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            User.objects.create_user(username=login, email=email, password=password, first_name=name, last_name=surname)
            return HttpResponse('Stworzono użytkownika')
        else:
            return render(request, 'hotel_app/reset.html', {'form': form})
