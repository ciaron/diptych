import os
from django.contrib import admin
from images.models import Image
from django.conf import settings

class ImageAdmin(admin.ModelAdmin):

    # this is required because the Admin interface 'delete' doesn't
    # call the model's own delete() method
    # see http://stackoverflow.com/questions/1471909/django-model-delete-not-triggered
    actions = ['delete_from_disk']

    fieldsets = [
        (None,               {'fields': ['image']}),
        ('Image information', {'fields': ['owner', 'date', 'title', 'caption']}),
    ]

    list_display = ['image', 'owner', 'date']

    def get_actions(self, request):
        actions = super(ImageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_from_disk(self, request, queryset):
        for obj in queryset:
            os.remove(os.path.join(settings.MEDIA_ROOT, obj.image.name))
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 image was"
        else:
            message_bit = "%s images were" % queryset.count()

        self.message_user(request, "%s successfully deleted." % message_bit)

    delete_from_disk.short_description = "Delete selected images"

    # http://stackoverflow.com/questions/5632848/default-value-for-user-foreignkey-with-django-admin
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ImageAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

admin.site.register(Image, ImageAdmin)
