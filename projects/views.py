# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from projects.forms import ContactForm
from projects.models import ContactMessage
from django.conf import settings
from django.contrib import messages
from projects.resume_analyzer.main import generate_text, get_llama_assistance, extract_text_from_docx, clean_text
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
import pdfplumber
import google.generativeai as genai
from django.utils.html import mark_safe
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from pandasql import sqldf as pysql
import os

from projects.query_builder.main import get_llama_assistance_qb
import json
import logging
import sqlite3
from flask import jsonify

# NavBar
def index(request):
    return render(request, "index.html")

def about(request): 
    return render(request, "about.html")

def projects(request):
    return render(request, "projects.html")

def connect(request):
    return render(request, "connect.html")

def thank_you(request):
    return render(request, "thankyou.html")

# Projects Pages
def machine_learning(request):
    return render(request, "machine_learning/machine_learning.html")

def deep_learning(request):
    return render(request, "deep_learning/deep_learning.html")

def generative_ai(request):
    return render(request, "generative_ai/generative_ai.html")


# Contact Form
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Example: Sending email
            send_mail(
                'Message from the Portfolio page',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Add a success message
            messages.success(request, 'Your message has been sent successfully! Now Shooo...!!')

            # Redirect to a different URL (PRG pattern)
            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


DOCX = ".docx"
UNSUPPORTED_FILE_TYPE = "Unsupported file format. Please upload a PDF or DOCX file."
def resume_analyzer(request):
    return render(request, "generative_ai/resume_analyzer/resume_analyzer.html")

def compare(request):
    if request.method == 'POST':
        selected_model = request.POST.get('selected_model')
        job_description = request.POST.get('job_description')
        resume = request.FILES.get('resume')

        if not (resume and job_description):
            return HttpResponseBadRequest("Please provide both resume and job description.")

        try:
            if resume.name.endswith('.pdf'):
                with pdfplumber.open(resume) as pdf:
                    all_text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                all_text = clean_text(all_text)
            elif resume.name.endswith(DOCX):
                all_text = extract_text_from_docx(resume)
                all_text = clean_text(all_text)
            else:
                return HttpResponseBadRequest(UNSUPPORTED_FILE_TYPE)

            main_role = '''[You're a professional consultant helping people land their dream job, by analyzing the job description and their resume details. YOU DO NOT HAVE TO MENTION YOUR ROLE TO THE USER, start direct to the point.
            You'll identify discrepancies, recommend areas for improvement, align candidate qualifications with company expectations, and outline areas of development. 
            This involves discerning the candidate's strengths and weaknesses, assessing their compatibility with the company's needs, and proposing actionable steps for improvement. 
            However, if the job description (JD) is entirely unrelated to the resume, strictly recommend them to prioritize focusing on the relevant areas instead of the unrelated ones.
            Note this: If you find both the Resume/Job-Description data is irrelevant, be bold and answer them about its irrelevance, be wild with the responses. One more thing, feel free to write as lengthy as you can]'''

            if selected_model == 'llama':
                structured_text = get_llama_assistance(f'''I need your help to organize and structure the Resume text, even personal information:
                                                {all_text}''')
                comparison = get_llama_assistance(f'''{main_role}
                Here's the Job Description: [{job_description}] 
                And here's the Resume Details: [{structured_text}]''')
            elif selected_model == 'genai':
                structured_text = generate_text(f'''I need your help to organize and structure the Resume text, even personal information:
                                                {all_text}''')
                comparison = generate_text(f'''{main_role}
                Here's the Job Description: [{job_description}] 
                And here's the Resume Details: [{structured_text}]''')

            return JsonResponse({"comparison": comparison})

        except Exception as e:
            return HttpResponseBadRequest(str(e))

def review(request):
    if request.method == 'POST':
        selected_model = request.POST.get('selected_model')
        resume = request.FILES.get('resume')

        if not resume:
            return HttpResponseBadRequest("Please upload a resume to review.")

        try:
            if resume.name.endswith('.pdf'):
                with pdfplumber.open(resume) as pdf:
                    all_text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                all_text = clean_text(all_text)
            elif resume.name.endswith('.docx'):
                all_text = extract_text_from_docx(resume)
                all_text = clean_text(all_text)
            else:
                return HttpResponseBadRequest(UNSUPPORTED_FILE_TYPE)

            review_prompt = f'''Please review the following resume text and provide a detailed analysis. Start with scoring the resume, you can write massive responses:
                                {all_text}'''

            if selected_model == 'llama':
                review = get_llama_assistance(review_prompt)
            elif selected_model == 'genai':
                review = generate_text(review_prompt)
            else:
                return HttpResponseBadRequest("Invalid model selected.")

            return JsonResponse({'review': review}) # OR you can use return HttpResponse(review, content_type="text/plain") 

        except Exception as e:
            return HttpResponseBadRequest(str(e))

def ask_question(request):
    if request.method == 'POST':
        selected_model = request.POST.get('selected_model')
        review_text = request.POST.get('review_text')
        user_question = request.POST.get('user_question')

        if not (review_text and user_question):
            return HttpResponseBadRequest("Both review text and user question are required.")

        prompt = f'''Based on the following review (given solely by you), answer the user's question in detail.
        It can be any question, so be friendly and open :) Don't mention your role.
        [Your Content Review:
        {review_text}]

        [User Question:
        {user_question}]

        Response:'''

        if selected_model == 'llama':
            response = get_llama_assistance(prompt)
        elif selected_model == 'genai':
            response = generate_text(prompt)

        return render(request, 'resume_analyzer/ask_question.html', {'response': response})

    return HttpResponseBadRequest("Invalid request method.")

def view_resume_content(request):
    if request.method == 'POST':
        resume = request.FILES.get('resume')

        if not resume:
            return HttpResponseBadRequest("Please upload a resume (PDF or DOCX) to view.")

        try:
            if resume.name.endswith('.pdf'):
                with pdfplumber.open(resume) as pdf:
                    all_text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                all_text = clean_text(all_text)
                structured_text = get_llama_assistance(f"I need your help to organize and structure the Resume text, don't mention your role or what task you did:\n{all_text}")
            elif resume.name.endswith('.docx'):
                all_text = extract_text_from_docx(resume)
                all_text = clean_text(all_text)
                structured_text = get_llama_assistance(f"I need your help to organize and structure the Resume text, don't mention your role or what task you did:\n{all_text}")
            else:
                return HttpResponseBadRequest("Unsupported file format. Please upload a PDF or DOCX file.")

            return JsonResponse({'structured_text': structured_text})

        except Exception as e:
            return HttpResponseBadRequest(f"Error processing the resume: {str(e)}")

    return HttpResponseBadRequest("Invalid request method.")


def query_builder(request):
    return render(request, "generative_ai/query_builder/query_builder.html")

logger = logging.getLogger(__name__)

@csrf_exempt
def get_query(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        query = request.POST.get('query')
        
        if file and query:
            df = pd.read_csv(file)
            columns_info = df.dtypes.to_dict()
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns
            unique_values = {col: df[col].value_counts().head(10).index.tolist() for col in categorical_columns}
            formatted_metadata = "\n".join([f"{col}: {dtype} (unique values: {unique_values.get(col, 'N/A')})" for col, dtype in columns_info.items()])
            
            # Get the SQL query from LLM
            sql_query = get_llama_assistance_qb(query, formatted_metadata)
            
            try:
                # Execute the SQL query using pandasql
                result_df = pysql(sql_query, locals())
                
                # Convert the result to JSON
                result_json = result_df.to_json(orient='records')
                
                return JsonResponse({'result': json.loads(result_json)})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)