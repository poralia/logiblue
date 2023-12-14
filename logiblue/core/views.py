from django.views import View
from django.shortcuts import render
from django.contrib import messages


class HomeView(View):
    template_name = "home.html"
    context = {}

    def get(self, request, *args, **kwagrs):
        self.context['messages'] = messages.get_messages(request)
        return render(request, self.template_name, self.context)
