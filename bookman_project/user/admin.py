from django.contrib import admin

from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin) :

	def has_add_permission(self, request, obj=None) :
		return True

	def has_view_permission(self, request, obj=None) :
		return (obj!=None and request.user==self) or request.user.is_librarian or request.user.is_superuser

	def has_change_permission(self, request, obj=None) :
		return (obj!=None and request.user==self) or request.user.is_librarian or request.user.is_superuser

	def has_del_permission(self, request, obj=None) :
		return (obj!=None and request.user==self) or request.user.is_librarian or request.user.is_superuser

