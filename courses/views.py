from .models import Course
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields= ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('course_list')
    
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/course/form.html'

class CourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/course/list.html'
    permission_required = 'courses.view_course'
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user) #I only get the courses created by the current user
    
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseEditView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/course/delete.html'
    permission_required = 'courses.delete_course'
    
