from django.shortcuts import render, get_object_or_404, redirect
from manager_app.models import *
from django.contrib import messages
from datetime import datetime,timedelta


def add_item(request):

    if request.method == 'POST':
        sh_name = request.POST.get('sh_name')
        sh_model = request.POST.get('sh_model')
        sh_size = request.POST.get('sh_size')
        sh_color = request.POST.get('sh_color')
        sh_manufacturer = request.POST.get('sh_manufacturer')
        sh_count = request.POST.get('sh_count')
        sh_price = request.POST.get('sh_price')
        sh_image = request.FILES.get('sh_image')
            
        Shoes.objects.create(
                sh_name=sh_name,
                sh_model=sh_model,
                sh_size=sh_size,
                sh_color=sh_color,
                sh_manufacturer=sh_manufacturer,
                sh_count=sh_count,
                sh_price=sh_price,
                sh_image=sh_image
            )
        messages.success(request, 'Елемент успішно додано.')
        
        return redirect('manager_app:items')  # Замість 'items' вставте правильну назву вашого URL
    else:
        return render(request, 'manager_add/items-add.html')
    

def add_order(request):
    shoes_list = Shoes.objects.all()
    user_list = Users.objects.all()  # Отримуємо список користувачів
    order_status = [(status.value, status.name) for status in Order_status]

    if request.method == 'POST':
        o_shoes_id = request.POST.get('o_shoes')
        o_recipient = request.POST.get('o_recipient')
        o_address = request.POST.get('o_address')
        o_comment = request.POST.get('o_comment')
        o_status = request.POST.get('o_status')
        o_user_id = request.POST.get('o_user')  # Отримуємо ID користувача
        o_count = int(request.POST.get('o_count', 0))

        shoes = get_object_or_404(Shoes, id_shoes=o_shoes_id)
        user = get_object_or_404(Users, id_user=o_user_id)

        if shoes.sh_count > 0:
            if o_count <= shoes.sh_count:
                if o_status in [status.value for status in Order_status]:
                    o_sum = shoes.sh_price * o_count

                    Orders.objects.create(
                        o_shoes=shoes,
                        o_count=o_count,
                        o_status=o_status,
                        o_recipient=o_recipient,
                        o_address=o_address,
                        o_comment=o_comment,
                        o_sum=o_sum,
                        o_user=user  # Зберігаємо користувача в замовленні
                    )
                    shoes.sh_count -= o_count
                    shoes.save()
                    messages.success(request, 'Замовлення успішно створено.')
                    return redirect('manager_app:orders')
                else:
                    error_message = "Неправильний статус замовлення"
                    messages.error(request, error_message)
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                messages.error(request, error_message)
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            messages.error(request, error_message)
        return render(request, 'manager_add/orders-add.html', {'shoes_list': shoes_list, 'user_list': user_list, 'order_status': order_status, 'error_message': error_message, 'form_data': request.POST})
    else:
        return render(request, 'manager_add/orders-add.html', {'shoes_list': shoes_list, 'user_list': user_list, 'order_status': order_status})


def add_reservation(request):
    shoes_list = Shoes.objects.all()
    user_list = Users.objects.all()  # Отримуємо список користувачів

    if request.method == 'POST':
        r_shoes_id = request.POST.get('r_shoes')
        r_user_id = request.POST.get('r_user')  # Отримуємо ID користувача
        r_count = int(request.POST.get('r_count', 0))

        try:
            shoes = Shoes.objects.get(id_shoes=r_shoes_id)
        except Shoes.DoesNotExist:
            error_message = "Взуття з вказаним ідентифікатором не існує"
            return render(request, 'manager_add/reservations-add.html', {'shoes_list': shoes_list, 'user_list': user_list, 'error_message': error_message, 'form_data': request.POST})
        
        try:
            user = Users.objects.get(id_user=r_user_id)
        except Users.DoesNotExist:
            error_message = "Користувач з вказаним ідентифікатором не існує"
            return render(request, 'manager_add/reservations-add.html', {'shoes_list': shoes_list, 'user_list': user_list, 'error_message': error_message, 'form_data': request.POST})

        if shoes.sh_count > 0:
            if r_count <= shoes.sh_count:
                Reservations.objects.create(
                    r_shoes=shoes,
                    r_count=r_count,
                    r_user=user  # Зберігаємо користувача в резервації
                )
                shoes.sh_count -= r_count
                shoes.save()
                messages.success(request, 'Резервацію успішно створено.')
                return redirect('manager_app:reservations')
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                messages.error(request, error_message)
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            messages.error(request, error_message)
        return render(request, 'manager_add/reservations-add.html', {'shoes_list': shoes_list, 'user_list': user_list, 'error_message': error_message, 'form_data': request.POST})
    else:
        return render(request, 'manager_add/reservations-add.html', {'shoes_list': shoes_list, 'user_list': user_list})