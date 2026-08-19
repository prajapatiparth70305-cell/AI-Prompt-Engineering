from django.db import models
from django.contrib.auth.models import User


class PromptHistory(models.Model):
    CATEGORY_CHOICES = [
        ("coding", "Coding"),
        ("study", "Study"),
        ("interview", "Interview"),
        ("content", "Content"),
        ("data", "Data"),
        ("general", "General"),

    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_prompt = models.TextField()
    optimized_prompt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_favorite = models.BooleanField(default=False,null=True)


    def __str__(self):
        return self.original_prompt[:50]

class PromptTemplate(models.Model):

    CATEGORY_CHOICES = [
        ("coding", "💻 Coding"),
        ("study", "📚 Study"),
        ("interview", "💼 Interview"),
        ("content", "✍️ Content Writing"),
        ("data", "📊 Data Analysis"),
        ("email", "📧 Email Writing"),
        ("general", "📝 General"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="general"
    )

    template = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title