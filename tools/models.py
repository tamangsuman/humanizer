from django.conf import settings
from django.db import models

class Generation(models.Model):
    TOOL_CHOICES = [
        ('humanizer', 'AI Text Humanizer'), ('detector', 'AI Content Detector'),
        ('paraphrase', 'Paraphrase Text'), ('grammar', 'Grammar Check'),
        ('summarizer', 'Summarizer'), ('researcher', 'AI Researcher'),
        ('fact-checker', 'Fact Checker'), ('emails', 'Emails'),
        ('instagram', 'Instagram Captions'), ('facebook', 'Facebook Ad Copy'),
        ('product', 'Product Description'), ('essay', 'Essay Writer'),
        ('rewrite', 'Rewrite Article'), ('extend', 'Extend Text'),
        ('academic', 'Academic Support'), ('chatbot', 'AI Chatbot'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tool_id = models.CharField(max_length=60, choices=TOOL_CHOICES, default='humanizer')
    mode = models.CharField(max_length=40, default='balanced')
    original_text = models.TextField()
    result_text = models.TextField(blank=True)
    ai_score = models.FloatField(default=0)
    plagiarism_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_tool_id_display()} - {self.created_at:%Y-%m-%d}'
