from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import StrategyPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import StrategyPost
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import FormView
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import Comment
from .forms import CommentCreateForm  
from django.shortcuts import redirect, get_object_or_404 , resolve_url



class IndexView(ListView):
    template_name = 'index.html'
    queryset = StrategyPost.objects.order_by('-posted_at')
    paginate_by = 9

@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    form_class = StrategyPostForm
    template_name = "post_strategy.html"
    success_url = reverse_lazy('strategy:post_done')
    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'

class CategoryView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = StrategyPost.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories
    
class UserView(ListView):
    template_name ='index.html'
    paginate_by = 9
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = StrategyPost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list
    
class DetailView(DetailView):
    template_name ='detail.html'
    model = StrategyPost

#----------------------------------------------------
    def get_context_data(self, **kwargs):
        post_pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォームを渡す
        detail = get_object_or_404(StrategyPost, pk=post_pk)
        context = {
                "detail": detail,
                "comments": Comment.objects.filter(target=detail.id)   #該当記事のコメントだけを渡します。
        }
        return context

class MypageView(ListView):
    template_name ='mypage.html'
    paginate_by = 9
    def get_queryset(self):
        queryset = StrategyPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
class StrategyDeleteView(DeleteView):
    model = StrategyPost
    template_name ='strategy_delete.html'
    success_url = reverse_lazy('strategy:index')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class StrategyUpdateView(UpdateView):
    model = StrategyPost
    template_name = 'strategy_update.html'
    fields = ['title', 'strategy']
    success_url = reverse_lazy('strategy:index')

#---------------------------------------------------

class ContactView(FormView):
    template_name ='contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('strategy:contact')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['form'])
        return context

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合わせ：{}'.format(title)

        message = \
            '送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:\n{3}'\
            .format(name, email, title, message)
        
        from_email = 'admin@example.com'

        to_list = ['kkr.python9999@gmail.com']

        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )
        message.send()
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)
    
#----------------------------------------------------

class CommentCreate(CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentCreateForm
    success_url = reverse_lazy('strategy:comment_done')

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(StrategyPost, pk=post_pk)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.target = post
        comment.save()
        self.object = comment
        return redirect('strategy:comment_done', pk=post_pk)
    
    def get_context_data(self, **kwargs):    
    # def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['strategy'] = get_object_or_404(StrategyPost, pk=self.kwargs['pk'])
        return context

class CommentSuccessView(TemplateView):
    template_name = 'comment_form_success.html'

class CommentDeleteView(DeleteView):
    model = Comment
    template_name ='comment_delete.html'
    success_url = reverse_lazy('strategy:strategy_detail')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class CommentUpdateView(UpdateView):
    # model = StrategyPost
    model = StrategyPost
    template_name = 'comment_update.html'
    fields = ['text']
    success_url = reverse_lazy('strategy:strategy_detail')
    def get_queryset(self):
        articles = StrategyPost.objects.filter(comment=self.request.user).prefetch_related('text')
        return articles
#----------------------------------------------------
    # def get_context_data(self, **kwargs):
    #     post_pk = self.kwargs['pk']
    #     context = super().get_context_data(**kwargs)
    #     # テンプレートにコメント作成フォームを渡す
    #     detail = get_object_or_404(StrategyPost, pk=post_pk)
    #     context = {
    #             "detail": detail,
    #             "comments": Comment.objects.filter(target=detail.id)   #該当記事のコメントだけを渡します。
    #     }
    #     return context
