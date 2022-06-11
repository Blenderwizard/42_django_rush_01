from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect
from .models import DiscussionModel, MessageModel
from .forms import MessageForm
from django.views.generic.edit import FormMixin


class DiscussionListView(ListView):
    paginate_by = 10
    model = DiscussionModel

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(DiscussionListView, self).get_queryset()
        if queryset:
            return queryset.filter(recipientmodel__user=self.request.user)\
                .prefetch_related('recipientmodel_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DiscussionListView, self).get_context_data(**kwargs)
        return context


class DiscussionDetailView(FormMixin, DetailView):
    model = DiscussionModel
    form_class = MessageForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        pk = self.kwargs.get('pk', None)
        # TODO: A FINIR
        form.save()
        return super(DiscussionDetailView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        model = DiscussionModel.objects.filter(id=pk, recipientmodel__user=request.user)
        if not request.user.is_authenticated or not model:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(DiscussionDetailView, self).get_queryset()
        if queryset:
            return queryset.filter(recipientmodel__user=self.request.user)\
                .prefetch_related('recipientmodel_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        for recipient in self.object.recipientmodel_set.all():
            if self.request.user != recipient.user:
                context['user2'] = recipient.user
        context['path'] = self.request.path
        context['object_msglist'] = MessageModel.objects.filter(discussion=self.object)
        return context
