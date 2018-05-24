from django.contrib import admin


# Register your models here.
from service_member.models import Member, Institute, Benefactor


class MemberAdmin(admin.ModelAdmin):
    pass


class InstituteAdmin(admin.ModelAdmin):
    pass


class BenefactorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Member, MemberAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Benefactor, BenefactorAdmin)
