# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import AbstractUser


class LoginView(View):

    def post(self, request):
        pass

    def get(self, request):
        pass


class LogoutView(View):

    def post(self, request):
        pass