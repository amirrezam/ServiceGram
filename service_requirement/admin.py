from django.contrib import admin


# Register your models here.
from service_requirement.models import CashRequirement, NonCashRequirement, HelpCash, HelpNonCash, Chunk


class CashRequirementAdmin(admin.ModelAdmin):
    pass


class NonCashRequirementAdmin(admin.ModelAdmin):
    pass


class HelpCashAdmin(admin.ModelAdmin):
    pass


class HelpNonCashAdmin(admin.ModelAdmin):
    pass


class ChunkAdmin(admin.ModelAdmin):
    pass


admin.site.register(CashRequirement, CashRequirementAdmin)
admin.site.register(NonCashRequirement, NonCashRequirementAdmin)
admin.site.register(HelpNonCash, HelpNonCashAdmin)
admin.site.register(HelpCash, HelpCashAdmin)
admin.site.register(Chunk, ChunkAdmin)
