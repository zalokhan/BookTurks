from django.contrib import admin

# Register your models here.
from .models import User, Quiz, QuizTag

admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(QuizTag)
