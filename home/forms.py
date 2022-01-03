from django import forms
from .models import Task, Friends


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title','finish_date','detail','reminder')


        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'}),
                'finish_date': forms.DateTimeInput(attrs={'class': 'form-control','type':"datetime-local"}),
                'detail': forms.Textarea(attrs={'class':'form-control','placeholder':'Description','cols':30,'rows':10}),
                'reminder': forms.CheckboxInput(attrs={'class':'form-check-input','id':'flexCheckDefault'})
            }


class ShareFriendForm(forms.ModelForm):

    class Meta:
        model = Friends
        fields = ('is_edit',)
        exclude =('friends','task')

        widgets = {
                'friend': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Friend email'}),
                'is_edit': forms.CheckboxInput(attrs={'class':'form-check-input','id':'flexCheckDefault'}),
             
            } 