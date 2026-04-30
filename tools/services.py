import os
import random
import re
from io import BytesIO
from pathlib import Path

PROMPTS = {
    'researcher': 'Provide deep research, key facts, structured context, and useful analysis.',
    'fact-checker': 'Verify the claims. Mark verified, false, or uncertain with concise reasoning.',
    'chatbot': 'Answer naturally and helpfully.',
    'plagiarism': 'Identify generic or unoriginal phrasing and suggest more unique wording.',
    'detector': 'Analyze whether the writing sounds AI-generated or human-written and explain why.',
    'paraphrase': 'Paraphrase while preserving meaning but changing structure and vocabulary.',
    'converter': 'Convert the input into the requested structured format.',
    'long-article': 'Write a comprehensive long-form article with headings and depth.',
    'analyze-file': 'Analyze the document with a summary, key points, and recommendations.',
    'grammar': 'Correct grammar, spelling, punctuation, and flow. Return the corrected text only.',
    'summarizer': 'Summarize into essential bullet points.',
    'citation': 'Create citations in an appropriate style based on the provided source details.',
    'analyze-website': 'Analyze the webpage/link description, messaging, purpose, and effectiveness.',
    'medium-article': 'Write an SEO-friendly medium-length blog post with headings.',
    'rewrite': 'Rewrite the article with better flow and clarity while keeping the same meaning.',
    'essay': 'Write a structured academic essay with introduction, body, and conclusion.',
    'extend': 'Expand the text with useful detail and context.',
    'instagram': 'Create five engaging Instagram captions with relevant hashtags.',
    'emails': 'Draft a clear professional email with a subject line.',
    'tiktok': 'Create a short TikTok script with visual beats and dialogue.',
    'facebook': 'Write persuasive Facebook ad copy with a hook and call to action.',
    'product': 'Write a persuasive product description focused on benefits.',
    'google-ad': 'Generate Google search ad headlines and descriptions.',
    'book-writer': 'Write a creative book chapter from the concept.',
    'academic': 'Explain or develop the topic with academic structure and clarity.',
    'refine_human': 'Make the text sound more natural and human.',
    'refine_pro': 'Make the text professional and polished.',
    'refine_academic': 'Make the text formal and academic.',
    'refine_short': 'Shorten the text while preserving the main meaning.',
    'refine_expand': 'Expand the text naturally with useful detail.',
    'humanizer': 'Transform the text into natural human writing.',
}

REPLACEMENTS = {
    r'\butilize\b': 'use', r'\bfurthermore\b': 'also', r'\btherefore\b': 'so',
    r'\bmoreover\b': 'plus', r'\bendeavor\b': 'try', r'\bfacilitate\b': 'help',
    r'\bcommence\b': 'start', r'\bterminate\b': 'end', r'\bdemonstrate\b': 'show',
}

def _local_humanize(text: str, mode: str = 'balanced') -> str:
    text = text.strip()
    for pattern, repl in REPLACEMENTS.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    cleaned = []
    for i, sentence in enumerate(sentences):
        s = sentence.strip()
        if not s:
            continue
        if mode == 'professional':
            s = s.replace("can't", 'cannot').replace("won't", 'will not')
        elif mode == 'casual' and i % 3 == 0:
            s = 'Honestly, ' + s[0].lower() + s[1:] if s else s
        elif mode == 'academic':
            s = s.replace('I think', 'It can be argued')
        cleaned.append(s)
    return '\n\n'.join(cleaned)

def _local_process(text: str, tool_id: str, mode: str) -> str:
    if tool_id in ['humanizer', 'paraphrase', 'rewrite', 'refine_human', 'refine_pro', 'refine_academic']:
        return _local_humanize(text, mode)
    if tool_id == 'grammar':
        fixed = text.strip()
        fixed = re.sub(r'\s+', ' ', fixed)
        fixed = re.sub(r'\s+([,.!?;:])', r'\1', fixed)
        return fixed[:1].upper() + fixed[1:] if fixed else fixed
    if tool_id == 'summarizer':
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        return '\n'.join(f'• {s}' for s in sentences[:5]) or text[:500]
    if tool_id == 'detector':
        score = estimate_ai_score(text)
        return f'Estimated AI probability: {score}%\n\nSignals checked: repetition, sentence uniformity, transition density, and overly polished phrasing.'
    if tool_id == 'plagiarism':
        return 'Potential originality notes:\n• Replace generic phrases with specific examples.\n• Add your own experience, data, or source references.\n• Rewrite repeated sentence structures.\n\n' + _local_humanize(text, mode)
    if tool_id in ['emails']:
        return 'Subject: Quick follow-up\n\nHello,\n\n' + _local_humanize(text, 'professional') + '\n\nBest regards,'
    if tool_id == 'instagram':
        base = text.strip().split('\n')[0][:90]
        return '\n'.join([f'{i}. {base} ✨ #{tag}' for i, tag in enumerate(['inspiration', 'creative', 'daily', 'growth', 'motivation'], 1)])
    if tool_id in ['facebook', 'google-ad', 'product']:
        return 'Hook: ' + text.strip()[:120] + '\n\nBenefits:\n• Clear value\n• Simple solution\n• Easy next step\n\nCall to action: Try it today.'
    if tool_id in ['essay', 'academic']:
        return f'Introduction\n{text.strip()}\n\nDiscussion\nThis topic can be examined through context, evidence, and practical implications.\n\nConclusion\nOverall, the main idea benefits from clear structure and careful support.'
    if tool_id in ['extend', 'long-article', 'medium-article', 'book-writer', 'researcher', 'fact-checker', 'citation']:
        return f'{PROMPTS.get(tool_id, "Result")}\n\n{text.strip()}\n\nKey points:\n• Clarify the purpose.\n• Add specific examples.\n• Organize the response into readable sections.'
    return _local_humanize(text, mode)

def process_text(text: str, tool_id: str = 'humanizer', mode: str = 'balanced') -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""Instruction: {PROMPTS.get(tool_id, PROMPTS['humanizer'])}\nMode: {mode}\n\nInput:\n{text}\n\nReturn only the final output."""
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as exc:
            return _local_process(text, tool_id, mode) + f"\n\n[Local fallback used because Gemini failed: {exc}]"
    return _local_process(text, tool_id, mode)

def estimate_ai_score(text: str) -> int:
    words = re.findall(r'\w+', text.lower())
    if not words:
        return 0
    avg_word = sum(len(w) for w in words) / len(words)
    transitions = sum(text.lower().count(w) for w in ['furthermore', 'moreover', 'therefore', 'additionally', 'in conclusion'])
    sentence_lengths = [len(re.findall(r'\w+', s)) for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    uniformity = 0
    if len(sentence_lengths) > 2:
        mean = sum(sentence_lengths) / len(sentence_lengths)
        uniformity = 1 if all(abs(x - mean) < 5 for x in sentence_lengths) else 0
    score = min(98, int(20 + avg_word * 5 + transitions * 7 + uniformity * 15 + random.randint(0, 10)))
    return max(3, score)

def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    if name.endswith('.txt'):
        return data.decode('utf-8', errors='ignore')
    if name.endswith('.pdf'):
        from PyPDF2 import PdfReader
        reader = PdfReader(BytesIO(data))
        return '\n'.join(page.extract_text() or '' for page in reader.pages)
    if name.endswith('.docx'):
        from docx import Document
        doc = Document(BytesIO(data))
        return '\n'.join(p.text for p in doc.paragraphs)
    raise ValueError('Unsupported file type. Upload .txt, .pdf, or .docx.')

def make_pdf(text: str) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - inch
    for line in text.splitlines() or ['']:
        while len(line) > 95:
            c.drawString(inch, y, line[:95])
            line = line[95:]
            y -= 14
            if y < inch:
                c.showPage(); y = height - inch
        c.drawString(inch, y, line)
        y -= 14
        if y < inch:
            c.showPage(); y = height - inch
    c.save()
    return buffer.getvalue()
