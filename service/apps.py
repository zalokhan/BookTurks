"""
App Config for service app
"""
from __future__ import unicode_literals
from django.apps import AppConfig

from concurrent import futures


class ServiceConfig(AppConfig):
    """
    Service Config -> BookTurks
    Add app config here.
    """
    name = 'service'
    verbose_name = "Book Turks Service"

    profile_sync_thread_pool = futures.ThreadPoolExecutor(max_workers=10)
