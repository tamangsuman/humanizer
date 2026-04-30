from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TextToolForm, FileUploadForm
from .models import Generation
from .services import estimate_ai_score, extract_text, make_pdf, process_text

TOOLS = [
    ('researcher', '🔎', 'AI Researcher', 'Research and structure information.'),
    ('fact-checker', '🛡️', 'Fact Checker', 'Review claims and reliability.'),
    ('humanizer', '✅', 'AI Text Humanizer', 'Make text read more naturally.'),
    ('detector', '🤖', 'AI Content Detector', 'Estimate AI-writing signals.'),
    ('paraphrase', '🔁', 'Paraphrase Text', 'Rewrite with the same meaning.'),
    ('grammar', '✨', 'Grammar Check', 'Correct grammar and flow.'),
    ('summarizer', '📝', 'Summarizer', 'Pull out key points.'),
    ('emails', '✉️', 'Emails', 'Draft professional emails.'),
    ('instagram', '📸', 'Instagram Captions', 'Create social captions.'),
    ('facebook', '📣', 'Facebook Ad Copy', 'Write ad copy.'),
    ('product', '🛍️', 'Product Descriptions', 'Sell benefits clearly.'),
    ('essay', '📚', 'Essay Writer', 'Structure academic writing.'),
]
REFINERS = [('refine_human','Make more human'),('refine_pro','Make professional'),('refine_academic','Make academic'),('refine_short','Shorten'),('refine_expand','Expand')]

def _user(request):
    return request.user if request.user.is_authenticated else None

def home(request):
    return render(request, 'tools/home.html', {'tools': TOOLS[:8]})

def dashboard(request):
    initial_tool = request.GET.get('tool', 'humanizer')
    form = TextToolForm(initial={'tool_id': initial_tool})
    result = generation = None
    if request.method == 'POST':
        form = TextToolForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']; tool_id = form.cleaned_data['tool_id']; mode = form.cleaned_data['mode']
            result = process_text(text, tool_id, mode)
            generation = Generation.objects.create(user=_user(request), tool_id=tool_id, mode=mode, original_text=text, result_text=result, ai_score=estimate_ai_score(result), plagiarism_score=2)
            messages.success(request, 'Your content was processed successfully.')
    return render(request, 'tools/dashboard.html', {'form': form, 'result': result, 'generation': generation, 'tools': TOOLS, 'refiners': REFINERS})

def tools_page(request):
    return render(request, 'tools/tools.html', {'tools': TOOLS})

def file_tools(request):
    form = FileUploadForm(); result = generation = None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                extracted = extract_text(form.cleaned_data['file']); tool_id = form.cleaned_data['tool_id']
                result = process_text(extracted, tool_id, 'balanced')
                generation = Generation.objects.create(user=_user(request), tool_id=tool_id, mode='file', original_text=extracted, result_text=result, ai_score=estimate_ai_score(result), plagiarism_score=1)
                messages.success(request, 'File text extracted and processed.')
            except Exception as exc:
                messages.error(request, str(exc))
    return render(request, 'tools/file_tools.html', {'form': form, 'result': result, 'generation': generation})

def history(request):
    qs = Generation.objects.all()
    qs = qs.filter(user=request.user) if request.user.is_authenticated else qs.filter(user__isnull=True)[:20]
    return render(request, 'tools/history.html', {'items': qs})

def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); login(request, user); return redirect('dashboard')
    return render(request, 'tools/signup.html', {'form': form})

def download_text(request, pk):
    item = get_object_or_404(Generation, pk=pk)
    response = HttpResponse(item.result_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{item.tool_id}-result.txt"'
    return response

def download_pdf(request, pk):
    item = get_object_or_404(Generation, pk=pk)
    response = HttpResponse(make_pdf(item.result_text), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{item.tool_id}-result.pdf"'
    return response
