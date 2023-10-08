# forms.py
from django import forms
from .models import Project, UserProfile, Message, Feedback, UserProfile, ProjectTag, UserProjectCollaboration, UserReview



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'skills', 'profile_image', 'interests']
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
            
        }

    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something about yourself...'}))



class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'required_skills', 'interests', 'scope']

    # custom fields
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter project description...'})
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Type your message here...'})
    )



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide your feedback here...'})
    )



class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['is_public', 'show_location', 'show_skills', 'show_interests']

    is_public = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False  # This makes the field optional
    )


class ProjectTagForm(forms.ModelForm):
    class Meta:
        model = ProjectTag
        fields = ['tag']

    tag = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter project tag...'})
    )


class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'required_skills', 'interests', 'scope']

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter project description...'})
    )






class UserProjectCollaborationForm(forms.ModelForm):
    class Meta:
        model = UserProjectCollaboration
        fields = ['message']

    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your collaboration message...'})
    )


class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['rating', 'comment']

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide your review here...'})
    )







# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description']

# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'goals', 'required_skills', 'expected_scope']


# class UserReviewForm(forms.ModelForm):
#     class Meta:
#         model = UserReview
#         fields = ['rating', 'comment']