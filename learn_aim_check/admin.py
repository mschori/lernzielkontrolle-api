from django.contrib import admin

from .models import ActionCompetence, CheckLearnAim, LearnAim, Tag

admin.site.register(Tag)
admin.site.register(ActionCompetence)
admin.site.register(LearnAim)
admin.site.register(CheckLearnAim)
