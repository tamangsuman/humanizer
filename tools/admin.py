from django.contrib import admin
from .models import Generation

@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ('tool_id', 'mode', 'ai_score', 'plagiarism_score', 'created_at')
    search_fields = ('original_text', 'result_text', 'tool_id')
    list_filter = ('tool_id', 'mode', 'created_at')
