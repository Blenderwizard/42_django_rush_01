from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect
from .models import DiscussionModel, MessageModel


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


class DiscussionDetailView(DetailView):
    model = DiscussionModel

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if not request.user.is_authenticated:    # TODO: or pk != request.user.id:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        context['objects_msglist'] = MessageModel.objects.filter(discussion=context['object'])
        return context
