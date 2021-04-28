from django.views import View
from django.shortcuts import render


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})
