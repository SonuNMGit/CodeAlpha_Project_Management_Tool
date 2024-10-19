from django import forms
from .models import Task, Project

class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'team_members', 'deadline']
        widgets = {
            'team_members': forms.CheckboxSelectMultiple(),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}), 
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if project:
            self.fields['assigned_to'].queryset = project.team_members.all()

