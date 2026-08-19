from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from .models import PromptHistory,PromptTemplate


def home(request):

    return render(
        request,
        "accounts/home.html"
    )


def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = SignupForm()

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    )


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


def user_logout(request):

    logout(request)

    return redirect("login")


# -------------------------------------------------
# PROMPT SCORE
# -------------------------------------------------

def calculate_prompt_score(prompt):

    if not prompt:
        return 0

    score = 0

    prompt_lower = prompt.lower()

    if len(prompt) >= 20:
        score += 20

    if len(prompt) >= 50:
        score += 10

    task_words = [
        "write",
        "create",
        "explain",
        "generate",
        "develop",
        "build",
        "calculate",
        "analyze"
    ]

    if any(
        word in prompt_lower
        for word in task_words
    ):
        score += 20

    context_words = [
        "for",
        "using",
        "about",
        "because",
        "where",
        "when"
    ]

    if any(
        word in prompt_lower
        for word in context_words
    ):
        score += 15

    output_words = [
        "format",
        "steps",
        "example",
        "list",
        "table",
        "code"
    ]

    if any(
        word in prompt_lower
        for word in output_words
    ):
        score += 20

    if len(prompt.split()) >= 10:
        score += 15

    return min(score, 100)


# -------------------------------------------------
# PROMPT SUGGESTIONS
# -------------------------------------------------

def get_prompt_suggestions(prompt):

    if not prompt:
        return [
            "Add a task, context, and desired output format."
        ]

    suggestions = []

    prompt_lower = prompt.lower()

    if len(prompt) < 20:

        suggestions.append(
            "Add more details to make your task clear."
        )

    task_words = [
        "write",
        "create",
        "explain",
        "generate",
        "develop",
        "build",
        "calculate",
        "analyze"
    ]

    if not any(
        word in prompt_lower
        for word in task_words
    ):

        suggestions.append(
            "Clearly mention what you want the AI to do."
        )

    context_words = [
        "for",
        "using",
        "about",
        "because",
        "where",
        "when"
    ]

    if not any(
        word in prompt_lower
        for word in context_words
    ):

        suggestions.append(
            "Add context such as technology, target audience, or purpose."
        )

    output_words = [
        "format",
        "steps",
        "example",
        "list",
        "table",
        "code"
    ]

    if not any(
        word in prompt_lower
        for word in output_words
    ):

        suggestions.append(
            "Specify the desired output format."
        )

    if len(prompt.split()) < 10:

        suggestions.append(
            "Try to make the prompt more specific."
        )

    if not suggestions:

        suggestions.append(
            "Excellent! Your prompt contains good details."
        )

    return suggestions


# -------------------------------------------------
# COMPARE SCORES
# -------------------------------------------------

def compare_prompt_scores(
    original_prompt,
    optimized_prompt
):

    original_score = calculate_prompt_score(
        original_prompt
    )

    optimized_score = calculate_prompt_score(
        optimized_prompt
    )

    improvement = (
        optimized_score -
        original_score
    )

    return (
        original_score,
        optimized_score,
        improvement
    )


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

@login_required
def dashboard(request):

    optimized_prompt = None

    prompt_score = None

    suggestions = []

    original_score = None

    optimized_score = None

    improvement = None

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    category_filter = request.GET.get(
        "category",
        ""
    )

    favorite_filter = request.GET.get(
        "favorite",
        ""
    )

    # ---------------------------------------------
    # CREATE PROMPT
    # ---------------------------------------------

    if request.method == "POST":

        original_prompt = request.POST.get(
            "original_prompt",
            ""
        ).strip()

        technique = request.POST.get(
            "technique",
            "zero_shot"
        )

        category = request.POST.get(
            "category",
            "general"
        )

        if original_prompt:

            prompt_score = calculate_prompt_score(
                original_prompt
            )

            suggestions = get_prompt_suggestions(
                original_prompt
            )

            # ZERO SHOT

            if technique == "zero_shot":

                optimized_prompt = f"""
Task:
{original_prompt}

Requirements:
- Provide a clear and accurate answer.
- Explain the solution step by step.
- Use simple and understandable language.
- Include examples where useful.

Output Format:
- Give the final answer in a structured format.
- Use headings and bullet points where appropriate.
"""

            # ROLE PROMPTING

            elif technique == "role":

                optimized_prompt = f"""
Role:
You are an expert assistant in the relevant subject.

Task:
{original_prompt}

Requirements:
- Provide a professional and accurate answer.
- Explain the solution step by step.
- Use simple and understandable language.
- Include examples where useful.

Output Format:
- Give the final answer in a structured format.
- Use headings and bullet points where appropriate.
"""

            # FEW SHOT

            elif technique == "few_shot":

                optimized_prompt = f"""
You are an AI assistant.

Example 1:
Question: What is Python?
Answer: Python is a high-level programming language.

Example 2:
Question: What is Django?
Answer: Django is a Python web framework.

Now solve this task:

Task:
{original_prompt}

Requirements:
- Follow the style of the examples.
- Provide a clear answer.
- Explain the solution step by step.
- Include examples where useful.

Output Format:
- Give the answer in a structured format.
"""

            # STRUCTURED OUTPUT

            elif technique == "structured":

                optimized_prompt = f"""
Task:
{original_prompt}

Instructions:
Provide a clear and accurate answer.

Return the response using:

1. Introduction
2. Explanation
3. Step-by-Step Solution
4. Example
5. Final Answer

Use simple and understandable language.
"""

            else:

                optimized_prompt = f"""
You are an expert assistant.

Task:
{original_prompt}

Requirements:
- Provide a clear and accurate answer.
- Explain the solution step by step.
- Use simple and understandable language.
- Include examples where useful.

Output Format:
- Give the final answer in a structured format.
- Use headings and bullet points where appropriate.
"""

            # COMPARE

            (
                original_score,
                optimized_score,
                improvement
            ) = compare_prompt_scores(
                original_prompt,
                optimized_prompt
            )

            # SAVE

            PromptHistory.objects.create(
                user=request.user,
                original_prompt=original_prompt,
                optimized_prompt=optimized_prompt,
                category=category
            )

    # ---------------------------------------------
    # HISTORY
    # ---------------------------------------------

    prompts = PromptHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # SEARCH

    if search_query:

        prompts = prompts.filter(
            original_prompt__icontains=search_query
        )

    # CATEGORY

    if category_filter:

        prompts = prompts.filter(
            category=category_filter
        )

    # FAVORITES

    if favorite_filter == "yes":

        prompts = prompts.filter(
            is_favorite=True
        )

    templates = PromptTemplate.objects.filter(
    is_active=True
).order_by("-created_at")
    return render(
        request,
        "accounts/dashboard.html",
        {
            "prompts": prompts,
            "optimized_prompt": optimized_prompt,
            "prompt_score": prompt_score,
            "suggestions": suggestions,
            "original_score": original_score,
            "optimized_score": optimized_score,
            "improvement": improvement,
            "search_query": search_query,
            "category_filter": category_filter,
            "favorite_filter": favorite_filter,
            "templates": templates
        }
    )


# -------------------------------------------------
# DELETE PROMPT
# -------------------------------------------------

@login_required
def delete_prompt(request, prompt_id):

    prompt = PromptHistory.objects.filter(
        id=prompt_id,
        user=request.user
    ).first()

    if prompt:

        prompt.delete()

    return redirect("dashboard")


# -------------------------------------------------
# FAVORITE / UNFAVORITE
# -------------------------------------------------

@login_required
def toggle_favorite(request, prompt_id):

    prompt = PromptHistory.objects.filter(
        id=prompt_id,
        user=request.user
    ).first()

    if prompt:

        prompt.is_favorite = not prompt.is_favorite

        prompt.save()

    return redirect("dashboard")