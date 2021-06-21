from django import forms
import requests
import re
from .config import url_user_connexion, url_user_register_first_step

user={}

class SignInForm(forms.Form):
    email = forms.EmailField(error_messages={'required':'The email is required', 'invalid':'The email is not well formed'})
    password = forms.CharField(error_messages={'required':'The password is required'})

    def is_valid(self):
 
        # run the parent validation first
        valid = super(SignInForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        # so far so good, get this user based on the username or email
        try:
            return self.checkUser()
        except:
            self._errors['no_user'] = 'Email or Password incorrect'
            return False

    def checkUser(self):
        params={'email':self.cleaned_data['email'], 'password':self.cleaned_data['password']}
        response=requests.post(url=url_user_connexion, json=params).json()
        print(response)
        if response['status']==0:
            if response['errmsg']==0:
                self._errors['no_user']='User does not exist'
            elif response['errmsg']==1:
                self._errors['finish_registration'] = 'Please check your email to finish your registration'
            return False
        else:
            user['firstname']=response['datas']['name']
            user['id_user']=response['datas']['uid']
            return True
        """user['firstname'] = "Choco"
        user['id_user'] = "123456"
        return True"""


class SignUpFirstStep(forms.Form):
    firstname = forms.CharField(error_messages={'required':'The Firstname is required'})
    lastname = forms.CharField(error_messages={'required':'The Lastname is required'})
    email = forms.EmailField(error_messages={'required':'The email is required', 'invalid':'The email is not well formed'})
    phonenumber = forms.CharField(error_messages={'required':'The Phonenumber is required'})
    password = forms.CharField(error_messages={'required': 'The password is required'})
    confirmpassword = forms.CharField(error_messages={'required': 'The password confirmation is required'})
    economicstatus = forms.CharField(error_messages={'required': 'The Economic statut is required'})

    def is_valid(self):

        # run the parent validation first
        valid = super(SignUpFirstStep, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        pwd = self.cleaned_data['password']
        confirm_pwd = self.cleaned_data['confirmpassword']

        if len(pwd) <= 8 or len(pwd) >= 32:
            self._errors['invalid_password'] = 'Password should contain at least 8 characters'
            return False
        elif len(re.findall(r"[0-9@#$%^&+=]+", pwd)) == 0:
            self._errors['invalid_password'] = 'Password should contain at least one non alphabetic character'
            return False
        if pwd!=confirm_pwd:
            self._errors['invalid_password'] = 'The passwords do not match'
            return False

        tel = self.cleaned_data['phonenumber']
        if re.match(r"\d+$", tel) is None:
            self._errors['invalid_password'] = 'The phone number should contain only digits'
            return False
        # so far so good, get this user based on the username or email
        try:
            self.registerUser()
        except:
            self._errors['user_already_exists'] = 'This email already exists'
            return False
        # all good
        return True

    def registerUser(self):
        params = {'email': self.cleaned_data['email'], 'password': self.cleaned_data['password'], 'firstname': self.cleaned_data['firstname'],
                  'lastname':self.cleaned_data['lastname'], 'phonenumber':self.cleaned_data['phonenumber'], 'economicstatus':self.cleaned_data['economicstatus']}
        response = requests.post(url=url_user_register_first_step, json=params).json()
        if response['status'] == 0:
            raise Exception('bla bla car')
        else:
            return 0


class SearchForm(forms.Form):

    def is_valid(self):
        print("est valide")

    def makeSearch(self):
        print("searching")