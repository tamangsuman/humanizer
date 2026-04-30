from django import forms

MODE_CHOICES = [
    ('balanced', 'Balanced'), ('academic', 'Academic'), ('professional', 'Professional'),
    ('casual', 'Casual'), ('seo', 'SEO Optimized'), ('creative', 'Creative')
]

TOOL_CHOICES = [
    ('humanizer', 'AI Text Humanizer'), ('detector', 'AI Content Detector'),
    ('paraphrase', 'Paraphrase Text'), ('grammar', 'Grammar Check'),
    ('summarizer', 'Text Summarizer'), ('researcher', 'AI Researcher'),
    ('fact-checker', 'Fact Checker'), ('plagiarism', 'Check Plagiarism'),
    ('emails', 'Emails'), ('instagram', 'Instagram Captions'), ('tiktok', 'TikTok Video Scripts'),
    ('facebook', 'Facebook Ad Copy'), ('product', 'Product Descriptions'),
    ('google-ad', 'Google Ad Copy'), ('essay', 'Essay Writer'), ('rewrite', 'Rewrite Article'),
    ('extend', 'Extend Text'), ('medium-article', 'Medium Article'), ('long-article', 'Long Article'),
    ('book-writer', 'Book Writer'), ('academic', 'Academic Support'), ('citation', 'Citation Machine'),
]

class TextToolForm(forms.Form):
    tool_id = forms.ChoiceField(choices=TOOL_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    mode = forms.ChoiceField(choices=MODE_CHOICES, initial='balanced', widget=forms.Select(attrs={'class': 'form-select'}))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'text-area', 'rows': 12,
        'placeholder': 'Paste text, a topic, draft, URL description, or instructions here...'
    }))

class FileUploadForm(forms.Form):
    tool_id = forms.ChoiceField(choices=[('summarizer', 'Summarize file'), ('analyze-file', 'Analyze file'), ('humanizer', 'Humanize extracted text')])
    file = forms.FileField(help_text='Supports .txt, .pdf, and .docx')
