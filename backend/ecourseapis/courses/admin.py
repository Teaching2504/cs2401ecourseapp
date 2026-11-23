from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.urls import path

from courses.models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

class  LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date']
    search_fields = ['subject']
    list_filter = ['id', 'subject', 'active']
    readonly_fields = ['image_view']
    form = LessonForm


    def image_view(self, lesson):
        if lesson.image:
            return mark_safe(f"<img src='/static/{lesson.image}' width='200' />")


    class Media:
        css = {
            'all':('/static/css/style.css',)
        }

class MyAdminSite(admin.AdminSite):
    site_header = 'eCourseApp'

    def get_urls(self):
        return [
            path('stats/', self.stats_view)
        ] + super().get_urls()
    def stats_view(self, request):
        #Truy van thong ke
        return TemplateResponse(request, 'admin/stats.html',{
            'stats':Category.objects.all(),
        })

admin_site = MyAdminSite()


admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)