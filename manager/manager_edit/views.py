from django.shortcuts import render

def admins_edit(request):
    return render(request, "manager_edit/admins_edit.html")
