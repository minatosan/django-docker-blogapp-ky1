from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from mysite.forms import UserCreationForm,ProfileForm
from blog.models import Article
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
import os
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
  #-は降順
  ranks=Article.objects.order_by('-count')[:2]
  objs = Article.objects.all()[:3]
  context={
    'title':'really Site',
    'articles': objs,
    'ranks':ranks,
  }
  return render(request,'mysites/index.html',context)

class Login(LoginView):
  template_name = 'mysites/auth.html'

  def form_valid(self,form):
    messages.success(self.request,'ログイン完了しました。')
    return super().form_valid(form)

  def form_invalid(self,form):
    messages.error(self.request,'エラーが発生しました')
    return super().form_invalid(form)


def signup(request):
  context={}
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      #user.is_active = False
      user.save()
      login(request,user)
      messages.success(request,'登録完了しました。')
      return redirect('/')
  return render(request,'mysites/auth.html',context)



class MypageView(LoginRequiredMixin,View):
  context={}

  def get(self,request):
    return render(request,'mysites/mypage.html',self.context)

  def post(self,request):
    form = ProfileForm(request.POST,request.FILES)
    if form.is_valid():
      profile=form.save(commit=False)
      profile.user= request.user
      profile.save()
      messages.success(request,'登録完了しました。')
      return redirect('/')
    return render(request,'mysites/mypage.html',self.context)

@login_required
def mypage(request):
  context={}
  if request.method=="POST":
    form = ProfileForm(request.POST)
    if form.is_valid():
      profile=form.save(commit=False)
      profile.user= request.user
      profile.save()
      messages.success(request,'登録完了しました。')
      return redirect('/')
  return render(request,'mysites/mypage.html',context)

def contact(request):
  context={
    'grecaptcha_sitekey': os.environ['GRECAPTCHA_SITEKEY'],

  }
  if request.method == "POST":
    #問い合わせがあった場合
    subject='お問い合わせがありました'
    message= """お問い合わせがありました。\n名前:{}\nメールアドレス:{}\n内容:{}""".format(
      request.POST.get('name'),
      request.POST.get('email'),
      request.POST.get('content'))
    email_from = os.environ['DEFFAULT_EMAIL_FROM']
    email_to= [
      os.environ['DEFFAULT_EMAIL_FROM']
      ]
    send_mail(subject,message,email_from,email_to)
    messages.success(request,'お問い合わせいただきありがとうございます。')

  return render(request,'mysites/contact.html',context)

import payjp

class PayView(View):
  payjp.api_key=os.environ['PAYJP_SECRET_KEY']
  public_key=os.environ['PAYJP_PUBLIC_KEY']
  amount=1000
  def get(self,request):
    context={
      'amount':self.amount,
      'public_key':self.public_key,
    }
    return render(request,'mysites/pay.html',context)

  def post(self,request):
    customer=payjp.Customer.create(
      email='example@pay.jp',
      card=request.POST.get('payjp-token')
    )
    charge = payjp.Charge.create(
      amount=self.amount,
      currency='jpy',
      customer=customer.id,
      description='支払いテスト'
    )
    context={
      'amount':self.amount,
      'public_key':self.public_key,
      'charge':charge,
    }
    return render(request,'mysites/pay.html',context)