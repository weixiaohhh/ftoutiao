# coding:utf-8
from django import forms
from django.forms import ModelForm
from app.models import Article
from account.models import Subject


class ShareForm(ModelForm):
	def __init__(self, user, *args, **kwargs):  
		super(ShareForm, self).__init__(*args, **kwargs) 
		self.fields['subject'] = forms.ModelChoiceField(  
			queryset = Subject.objects.filter(user=user),  
			required = True,  
			label = "独立号",   
			error_messages = {'required': "以下是必填项"},  
			empty_label = None,   
            ) 
        
	subject = forms.ModelChoiceField(queryset = Subject.objects.none())
	title = forms.CharField(label='标题', max_length=100,widget=forms.TextInput(attrs={'class':'form-control',}))
	link = forms.URLField(label='链接',widget=forms.URLInput(attrs={'class':'form-control'}))
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	
	class Meta:
		model = Article
		fields = ('subject','title','link','views')


class SubjectForm(ModelForm):

	class Meta:
		model = Subject
		fields = ['title']
	

