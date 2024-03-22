from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from projects.models import Task
from .models import UserProfile
from .models import Invite
from .forms import RegistrationForm
from .forms import CompanyRegistrationForm
from .forms import ProfilePictureForm
from django.shortcuts import get_object_or_404, HttpResponse


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            user = form.save()
            created = True
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            context = {'created' : created}
            return render(request, 'register/reg_form.html', context)
        else:
            return render(request, 'register/reg_form.html', context)
    else:
        form = RegistrationForm()
        context = {
            'form' : form,
        }
        return render(request, 'register/reg_form.html', context)


def usersView(request):
    user = request.user
    user_profiles  = UserProfile.objects.all()
    tasks = Task.objects.filter(assign=user)
    total_tasks = tasks.count()
    completed_tasks = Task.objects.filter(assign=user, status='5').count()
    avg_projects = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    print(avg_projects)
    
    user_tasks = {}
    for user_profile in user_profiles:
        tasks = Task.objects.filter(assign=user_profile.user)
        print("Tasks: ", tasks)
        completedTasks = Task.objects.filter(assign=user_profile.user, status="5")
        print("Completed tasks: ", completedTasks)
        user_tasks[user_profile] = tasks
    context = {
         'user_profiles': user_profiles,
        'avg_projects': avg_projects,
    }
    return render(request, 'register/users.html', context)

def user_view(request, profile_id):
    user = UserProfile.objects.get(id=profile_id)
    context = {
        'user_view' : user,
    }
    return render(request, 'register/user.html', context)


def profile(request):
    if request.method == 'POST':
        img_form = ProfilePictureForm(request.POST, request.FILES)
        print('PRINT 1: ', img_form)
        context = {'img_form' : img_form }
        if img_form.is_valid():
            img_form.save(request)
            updated = True
            context = {'img_form' : img_form, 'updated' : updated }
            return render(request, 'register/profile.html', context)
        else:
            return render(request, 'register/profile.html', context)
    else:
        img_form = ProfilePictureForm()
        context = {'img_form' : img_form }
        return render(request, 'register/profile.html', context)


def newCompany(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            form.save()
            created = True
            form = CompanyRegistrationForm()
            context = {
                'created' : created,
                'form' : form,
                       }
            return render(request, 'register/new_company.html', context)
        else:
            return render(request, 'register/new_company.html', context)
    else:
        form = CompanyRegistrationForm()
        context = {
            'form' : form,
        }
        return render(request, 'register/new_company.html', context)


def invites(request):
    return render(request, 'register/invites.html')


def invite(request, profile_id):
    try:
        profile_to_invite = get_object_or_404(UserProfile, id=profile_id)
    except UserProfile.DoesNotExist:
        # Handle the case where UserProfile does not exist
        # For example, redirect the user to an error page or display a message
        return HttpResponse("User profile does not exist", status=404)
    
    logged_profile = get_active_profile(request)
    if not profile_to_invite in logged_profile.friends.all():
        logged_profile.invite(profile_to_invite)
    
    return redirect('core:index')


def deleteInvite(request, invite_id):
    logged_user = get_active_profile(request)
    logged_user.received_invites.get(id=invite_id).delete()
    return render(request, 'register/invites.html')


def acceptInvite(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    invite.accept()
    return redirect('register:invites')

def remove_friend(request, profile_id):
    user = get_active_profile(request)
    user.remove_friend(profile_id)
    return redirect('register:friends')


from django.http import Http404

def get_active_profile(request):
    user = request.user
  
    try:
        user_id = user.userprofile_set.values_list('id', flat=True).first()
        if user is not None:
            return UserProfile.objects.get(id=user.id)
        else:
            raise Http404("UserProfile does not exist for this ")
    except UserProfile.DoesNotExist:
        raise Http404("UserProfile does not exist for this ")


def friends(request):
    if request.user.is_authenticated:
        user = get_active_profile(request)
        friends = user.friends.all()
        context = {
            'friends' : friends,
        }
    else:
        users_prof = UserProfile.objects.all()
        context= {
            'users_prof' : users_prof,
        }
    return render(request, 'register/friends.html', context)