from django.shortcuts import render, redirect
from .models import *
from django.views import generic
from datetime import datetime as dt
from datetime import time as ti
from .utils import *
from django.utils.safestring import mark_safe

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors)>0 :
        for key,value in errors.items():
            messages.error(request, value, extra_tags="signup")
        return redirect("/")
    
    is_in_db = User.objects.filter(email = request.POST['email']).first()
    if is_in_db:
        return redirect("/")
    hashed_password = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()
    
    new_user = User.objects.create(
        first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        email = request.POST['email'],
        password = hashed_password
    )

    request.session['user_id'] = new_user.id

    return redirect('/success')

def update(request, id):
    uid = request.session.get('user_id')
    if(uid==None):
        return redirect("/")
    errors = Event.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/calendar/edit/{id}")

    event_from_db = Event.objects.get(id=id)
    event_from_db.title = request.POST['title']
    event_from_db.description = request.POST['description']
    event_from_db.start = dt.strptime(request.POST['start'], "%Y-%m-%d")
    event_from_db.end = dt.strptime(request.POST['end'], "%Y-%m-%d")
    event_from_db.urgent = request.POST['urgent']
    event_from_db.time_start = request.POST['start_time']
    event_from_db.time_end = request.POST['time_end']
    event_from_db.save()
    return redirect(f"/calendar/edit/{id}")


def create(request):
    uid = request.session.get('user_id')
    if(uid==None):
        return redirect("/")
    errors = Event.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/success")
    user_logged = User.objects.get(id = request.session.get('user_id'))
    Event.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        start = request.POST['start'],
        end = request.POST['end'],
        urgent = request.POST['urgent'],
        user = user_logged,
        time_start = request.POST['start_time'],
        time_end = request.POST['end_time']
    )
    return redirect('/success')

def success(request):
    uid = request.session.get('user_id')
    if(uid==None):
        return redirect("/")
    user_from_db = User.objects.get(id = uid)
    context = {
        "user": user_from_db
    }

    return render(request, 'dash.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    found_user = User.objects.filter(email=request.POST['email'])
    if len(found_user)>0:
        user_from_db = found_user[0]
        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(),
            user_from_db.password.encode()
        )
        if is_pw_correct:
            request.session['user_id'] = user_from_db.id
            return redirect('/success')

    messages.error(request, 'Invalid cradential', extra_tags="login")
    return redirect('/')

def view(request, id):
    uid = request.session.get('user_id')
    if(uid==None):
        return redirect("/")
    event_from_db = Event.objects.get(id=id)
    context = {'event':event_from_db}
    print('$'*100)
    print(event_from_db)
    return render(request, 'view.html', context)

def delete_event(request, id):
    uid = request.session.get('user_id')
    if(uid==None):
        return redirect("/")
    event_from_db = Event.objects.get(id = id)
    event_from_db.delete()
    return redirect("/success")

def edit(request, id):
    uid = request.session.get('user_id')
    if(uid==None):
        return redirect("/")
    event_from_db = Event.objects.get(id = id)
    context = {'event':event_from_db}
    return render(request, 'view.html', context)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.session['user_id']
        user = User.objects.get(id=id)
        d = dt.today()

        cal = MyCalendar(d.year, d.month)

        html_cal = cal.formatmonth(user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

