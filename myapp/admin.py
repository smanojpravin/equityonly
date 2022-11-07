from django.contrib import admin
from myapp.models import HistoryOIChange,HistoryOITotal,LiveOIChange,LiveOITotal,LiveOITotalAllSymbol,LiveEquityResult,LiveOIPercentChange,HistoryOIPercentChange, LiveSegment

# Register your models here.
admin.site.register(LiveOIChange)
admin.site.register(LiveOITotal)
admin.site.register(LiveOIPercentChange)
admin.site.register(LiveSegment)
admin.site.register(LiveOITotalAllSymbol)