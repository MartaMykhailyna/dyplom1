from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages




def welcome_page(request):
    return render(request, 'manager_welcome/index.html')

def send_email(request):
    if request.method == 'POST':
        email = request.POST['contact-us']
        
        # Відправка електронної пошти
        send_mail(
            'Умови співпраці та посилання на реєстрацію',
            'Дякуємо за інтерес до нашої платформи. Протягом дня ми надішлемо вам умови співпраці та посилання на реєстрацію через наш Telegram-бот.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        messages.success(request, 'Електронна пошта надіслана успішно.')
        return redirect('welcome-page')
    else:
        return render(request, 'manager_welcome/index.html')