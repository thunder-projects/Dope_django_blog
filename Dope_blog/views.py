from PIL import Image
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Heading, Subheading, Usercontact, Comment, UserProfile, Category, About
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import time
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, CommentForm, UserProfileForm, UserForm
from django.conf import settings
from newsletter.forms import EmailSignupForm
from newsletter.models import Signup
# Create your views here.






def home(request):
    topcats = Category.objects.filter(pk__in=[2, 3, 1])
    posts = Post.objects.all()[:3]
    try:
        latest = Post.objects.latest('timestamp')
    except Post.DoesNotExist:
        latest = None
    user = None
    form = EmailSignupForm()
    return render(request, 'Dope_blog/home.html', {'posts': posts, 'topcats': topcats, 'latest': latest, 'form': form})
    # {'posts': posts, 'topcats': topcats, 'latest': latest, 'form': form}


def contact(request):
    thank = False
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        query = request.POST['query']
        usercontact = Usercontact(
            firstname=firstname, lastname=lastname, email=email, query=query)
        usercontact.save()
        thank = True
    if thank:
        messages.success(request, 'Thanks For Contacting Us...')
        return redirect('contact')
    return render(request, 'Dope_blog/contact.html')


def about(request):
    about = About.objects.get(id=1)
    return render(request, 'Dope_blog/about.html',{'about':about})


def articles(request, category):
    # allposts excluding top 3 post which is showed on home page
    categories = Category.objects.all()
    if category == 'all':
        allposts = Post.objects.all()
    else:
        allposts = Post.objects.filter(topic__icontains=category)
    page = request.GET.get('page', 1)

    # allposts passing to paginator i.e we are not passing queryset(allposts) to template not needed actully
    # bcoz paginator will handle it it will give us a variable which we will pass to template
    # (if we use same name for queryset(of Post.objects) and paginator var not gona  change anything)
    # (from django documentaion)
    # 1) Under the hood, all methods of pagination use the Paginator class. It does all the heavy lifting of actually splitting a QuerySet into Page objects.
    # 2) Give Paginator a list of objects, plus the number of items you’d like to have on each page, and it gives you methods for accessing the items for each page:

    paginator = Paginator(allposts, 12)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'Dope_blog/articles.html', {'posts': posts, 'categories': categories,'category':category })


def post(request, id, slug):
    article = get_object_or_404(Post, pk=id)
    headings = article.heading.all()
    subheadings = article.subheading.all()
    relatedposts = Post.objects.filter(
        topic__icontains=article.topic).exclude(pk=id)
    comments = Comment.objects.filter(
        post=article, reply__isnull=True).order_by('-id')
    allposts = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(allposts, 1)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    prev_slug = ''
    next_slug = ''
    if Post.objects.filter(id=id-1):
        if id-1 > 0:
            prev_slug = Post.objects.get(id=id-1).slug
    if Post.objects.filter(id=id-1):
        if id+1 <= allposts.count() :
            next_slug = Post.objects.get(id=id+1).slug
    form = EmailSignupForm()
    if request.method == 'POST':
        cform = CommentForm(request.POST or None)
        if cform.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('reply_id')
            reply_obj = None
            if reply_id:
                reply_obj = Comment.objects.get(id=reply_id)

            new_comment = cform.save(commit=False)
            new_comment.comment = comment
            new_comment.reply = reply_obj
            new_comment.post = article
            new_comment.commenter = request.user
            new_comment.save()
            # return redirect('post',id=id)
    else:
        cform = CommentForm()

    context = {
        'article': article,
        'headings': headings,
        'subheadings': subheadings,
        'relatedposts': relatedposts, 
        'post': post, 
        'comments': comments, 
        'cform': cform,
        'totallikes' : article.totalLikes(),
        'form':form,
        'next_slug': next_slug,
        'prev_slug':prev_slug,
        # 'totallikes' : totalLikes()
        }

    if request.is_ajax():
        html = render_to_string('Dope_blog/includes/comments.html', context, request=request)
        return JsonResponse({'form':html})

    return render(request, 'Dope_blog/post.html', context)

def articlelikes(request):
    article = get_object_or_404(Post,id=request.POST.get('article_id'))
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    
    context = {
        'article':article,
        'totallikes': article.totalLikes()
    }
    if request.is_ajax():
        html = render_to_string(
            'Dope_blog/articlelikes.html', context, request=request)
        return JsonResponse({'form': html})
    

def search(request):
    start_time = time.time()
    query = request.GET['query']
    searchedposts = ''
    if len(query) >= 1:
        searchedposts = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query))
    lenof = len(searchedposts)
    msg = None
    if lenof == 0:
        msg = 'Sorry we have 0 search results for "{}", Try again with another specific search term'.format(query)

    timed = (round(time.time() - start_time, 4))
    params = {
        'searchedposts': searchedposts,
        'query': query,
        'lenof': lenof,
        'timed': timed,
        'msg':msg
    }
    return render(request, 'Dope_blog/search.html',params)

# user accounts login signup system views____________


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        profile_form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        profile_form = UserProfileForm()
    return render(request, 'Dope_blog/signup.html', {'form': form, 'profile_form': profile_form})


# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email', )
#     template_name = 'Dope_blog/my_account.html'
#     success_url = reverse_lazy('my_account')
    


#     def get_object(self):
#         return self.request.user


@login_required
def Account(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account')

    else:
        u_form = UserForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'Dope_blog/my_account.html', {'form': u_form, "form2": p_form, })




    # if request.method == 'POST':
    #     form = UserProfileForm(request.POST or None,
    #                            request.FILES or None)
    #     if form.is_valid():
    #         profile = UserProfile.objects.get(id=uid)
    #         profile.avatar = form.cleaned_data['avatar']
    #         profile.save()
    #         return redirect('my_account')









