# Generated for the converted Django AI Humanizer app
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_id', models.CharField(choices=[('humanizer', 'AI Text Humanizer'), ('detector', 'AI Content Detector'), ('paraphrase', 'Paraphrase Text'), ('grammar', 'Grammar Check'), ('summarizer', 'Summarizer'), ('researcher', 'AI Researcher'), ('fact-checker', 'Fact Checker'), ('emails', 'Emails'), ('instagram', 'Instagram Captions'), ('facebook', 'Facebook Ad Copy'), ('product', 'Product Description'), ('essay', 'Essay Writer'), ('rewrite', 'Rewrite Article'), ('extend', 'Extend Text'), ('academic', 'Academic Support'), ('chatbot', 'AI Chatbot')], default='humanizer', max_length=60)),
                ('mode', models.CharField(default='balanced', max_length=40)),
                ('original_text', models.TextField()),
                ('result_text', models.TextField(blank=True)),
                ('ai_score', models.FloatField(default=0)),
                ('plagiarism_score', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
