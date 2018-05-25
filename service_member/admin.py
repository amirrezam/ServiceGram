from django.contrib import admin


# Register your models here.
from service_member.models import Member, Institute, Benefactor, Skill


class MemberAdmin(admin.ModelAdmin):
    pass


class InstituteAdmin(admin.ModelAdmin):
    pass


class BenefactorAdmin(admin.ModelAdmin):
    pass


class SkillAdmin(admin.ModelAdmin):
    pass


admin.site.register(Member, MemberAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Benefactor, BenefactorAdmin)
admin.site.register(Skill, SkillAdmin)
