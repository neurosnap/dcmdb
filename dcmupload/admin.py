from django.contrib import admin
from dcmupload.models import Study, Series, Image

admin.site.register(Study)
admin.site.register(Series)
admin.site.register(Image)