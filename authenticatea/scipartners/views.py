from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordChangeForm, UserChangeForm
from .models import Project, Message, UserProfile, Notification, Feedback, User, UserProfile, ProjectTag, Skill, Interest, UserReview, UserProjectCollaboration
from .forms import UserProfileForm, ProjectCreationForm, MessageForm, FeedbackForm,PrivacySettingsForm, ProjectTagForm, ProjectEditForm, UserProjectCollaborationForm, UserReviewForm
from django.contrib import messages
from notifications.signals import notify
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import  update_session_auth_hash
from notifications.models import Notification

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')  # Redirect to the user's dashboard or desired page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created.')
            return redirect('dashboard')  # Redirect to the user's dashboard or desired page
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect back to the profile page
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'profile.html', {'user_profile_form': user_profile_form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Redirect to the login page after logging out

@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            return redirect('dashboard')  # Redirect to the user's dashboard
    else:
        form = ProjectCreationForm()
    
    return render(request, 'project/create.html', {'form': form})



@login_required
def send_message_view(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('message_thread', receiver_id=receiver_id)  # Redirect to message thread
    else:
        form = MessageForm()
    
    return render(request, 'messaging/send_message.html', {'form': form, 'receiver': receiver})



def user_profile_view(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    return render(request, 'profile/profile.html', {'user_profile': user_profile})



def list_projects(request):
    skills = Skill.objects.all()
    projects = Project.objects.all()
    
    selected_skill = request.GET.get('skill')
    if selected_skill:
        projects = projects.filter(required_skills__id=selected_skill)
    
    return render(request, 'project/list_projects.html', {'projects': projects, 'skills': skills})

def notification_view(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})


def feedback_view(request, project_id):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.project_id = project_id
            feedback.save()
            return redirect('project_details', project_id=project_id)  # Redirect to project details
    else:
        form = FeedbackForm()
    
    return render(request, 'project/feedback.html', {'form': form})

@login_required
def privacy_settings_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the user's profile
    else:
        form = PrivacySettingsForm(instance=user_profile)
    
    return render(request, 'profile/privacy_settings.html', {'form': form})

@login_required
def add_project_tag_view(request, project_id):
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = ProjectTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.project = project
            tag.save()
            return redirect('project_details', project_id=project_id)  # Redirect to project details
    else:
        form = ProjectTagForm()
    
    return render(request, 'project/add_tag.html', {'form': form, 'project': project})



def dashboard_view(request):
    user = request.user
    user_projects = Project.objects.filter(creator=user)
    user_notifications = Notification.objects.filter(user=user)
    user_messages = Message.objects.filter(receiver=user)
    
    return render(request, 'dashboard.html', {
        'user_projects': user_projects,
        'user_notifications': user_notifications,
        'user_messages': user_messages,
    })


def project_details_view(request, project_id):
    project = Project.objects.get(id=project_id)
    user_feedback = Feedback.objects.filter(user=request.user, project=project).first()
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=user_feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.project = project
            feedback.save()
            return redirect('project_details', project_id=project_id)
    else:
        form = FeedbackForm(instance=user_feedback)
    
    return render(request, 'project/details.html', {'project': project, 'form': form})



@login_required
def search_projects_view(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        interests = Interest.objects.all()
        selected_skill = request.GET.get('skill')
        selected_interest = request.GET.get('interest')

        if selected_skill and selected_interest:
            projects = Project.objects.filter(required_skill__id=selected_skill, interest__id=selected_interest)
        elif selected_skill:
            projects = Project.objects.filter(required_skill__id=selected_skill)
        elif selected_interest:
            projects = Project.objects.filter(interest__id=selected_interest)
        else:
            projects = Project.objects.all()

        return render(request, 'project/search.html', {'projects': projects, 'skills': skills, 'interests': interests})
    else:
        # Handle other HTTP methods as needed
        pass

@login_required
def inbox_view(request):
    user = request.user
    user_messages = Message.objects.filter(receiver=user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'user_messages': user_messages})

@login_required
def user_settings_view(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in after password change
            return redirect('user_settings')  # Redirect back to settings page
    else:
        user_form = UserChangeForm(instance=request.user)
    
    return render(request, 'profile/settings.html', {'user_form': user_form})



@login_required
def deactivate_account_view(request):
    if request.method == 'POST':
        # Handle account deactivation logic here
        # Optionally, you can ask the user to confirm their password before deactivation
        return redirect('account_deactivated')  # Redirect to a confirmation page
    else:
        return render(request, 'profile/deactivate_account.html')
    
@login_required
def account_deactivated_view(request):
    return render(request, 'profile/account_deactivated.html')


@login_required
def edit_project_view(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        # Handle the case where the project with the given ID doesn't exist
        return HttpResponse("Project not found", status=404)

    if request.user != project.creator:
        # If the user is not the project creator, return a forbidden response
        return HttpResponseForbidden("You do not have permission to edit this project.")

    if request.method == 'POST':
        form = ProjectEditForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_details', project_id=project_id)
    else:
        form = ProjectEditForm(instance=project)

    return render(request, 'project/edit.html', {'form': form, 'project': project})

@login_required
def collaborate_on_project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = UserProjectCollaborationForm(request.POST)
        if form.is_valid():
            collaboration = form.save(commit=False)
            collaboration.user = request.user
            collaboration.project = project
            collaboration.save()
            return redirect('project_details', project_id=project_id)
    else:
        form = UserProjectCollaborationForm()
    
    return render(request, 'project/collaborate.html', {'form': form, 'project': project})



@login_required
def deactivate_project_view(request, project_id):
    # Get the project or return a 404 response if it doesn't exist
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.creator:
        # If the user is not the project creator, return a forbidden response
        return HttpResponseForbidden("You do not have permission to deactivate this project.")

    if request.method == 'POST':
        # Handle project deactivation logic here
        # For example, set project.active = False or delete the project
        project.active = False
        project.save()
        return redirect('project_deactivated')  # Redirect to a confirmation page

    return render(request, 'project/deactivate.html', {'project': project})


@login_required
def collaborate_on_project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = UserProjectCollaborationForm(request.POST)
        if form.is_valid():
            collaboration = form.save(commit=False)
            collaboration.user = request.user
            collaboration.project = project
            collaboration.save()
            return redirect('project_details', project_id=project_id)
    else:
        form = UserProjectCollaborationForm()
    
    return render(request, 'project/collaborate.html', {'form': form, 'project': project})


def deactivate_project_view(request, project_id):
    # Get the project or return a 404 response if it doesn't exist
    project = get_object_or_404(Project, id=project_id)
    
    if request.user != project.creator:
        # Implement appropriate permissions and error handling for unauthorized users
        return redirect('project_details', project_id=project_id)
    
    if request.method == 'POST':
        # diplay a confirmation page with a form for the project creator
        return render(request, 'project/confirm_deactivation.html', {'project': project})
    
    return render(request, 'project/deactivate.html', {'project': project})
    


@login_required
def deactivate_account_view(request):
    if request.method == 'POST':
        # Verify the user's password for confirmation
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            return redirect('account_deactivated')  # Redirect to a confirmation page
    else:
        password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'profile/deactivate_account.html', {'password_form': password_form})


def new_project_opportunity(request):
    # ... logic to create a new project opportunity ...
    notify.send(request.user, recipient=request.user, verb='New project opportunity available!')

def new_message(request, recipient_user):
    # ... logic to create a new message ...
    recipient = User.objects.get(username=recipient_user)
    notify.send(request.user, recipient=recipient, verb='You have a new message!')


@login_required
def user_dashboard(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    user_profile = UserProfile.objects.get(user=request.user)
    
    return render(request, 'user_dashboard.html', {'user_notifications': user_notifications, 'user_profile': user_profile})