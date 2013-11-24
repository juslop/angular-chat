from django import forms
from chat.models import UserExtra

class AccountForm(forms.ModelForm):
    pw1 = forms.CharField(label="Change Password", widget=forms.PasswordInput,
                          required=False)
    pw2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput,
                          required=False)
    
    class Meta:
        model = UserExtra
        exclude = ('user', 'thumbnail',)
    
    def clean_pw1(self):
        self.pw1 = None
        pw1 = self.cleaned_data.get('pw1', '')
        self.pw1 = pw1
        return pw1

    def clean_pw2(self):
        pw1 = self.cleaned_data.get('pw1', '')
        pw2 = self.cleaned_data.get('pw2', '')
        if pw1 and pw1 != pw2:
            raise forms.ValidationError, _('The two passwords did not match')
        return pw2

    def save(self, commit=True):
        print self.instance.user
        if self.pw1:
            self.instance.user.set_password(self.pw1)
            self.instance.user.save()
        return super(AccountForm, self).save(commit=commit)
