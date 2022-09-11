from django.shortcuts import render
def confirm_em(request):
    return render(request, "restauth/templates/email_confirmation.html")