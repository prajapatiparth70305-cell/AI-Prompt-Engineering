from django.urls import path
from .views import (
    dashboard,
    delete_prompt,
    export_prompts,
    home,
    signup,
    toggle_favorite,
    user_login,
    user_logout,
)

urlpatterns = [
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("export_prompts/", export_prompts, name="export_prompts"),
    path("delete_prompt/<int:prompt_id>/", delete_prompt, name="delete_prompt"),
    path("toggle_favorite/<int:prompt_id>/", toggle_favorite, name="toggle_favorite"),
]