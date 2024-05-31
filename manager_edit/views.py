from django.shortcuts import render, get_object_or_404, redirect
from manager_app.models import *
from django.contrib import messages


def update_item(request, shoes_id):
    # Отримуємо об'єкт Shoes за його ідентифікатором
    item = get_object_or_404(Shoes, id_shoes=shoes_id)
    if request.method == 'POST':
        item.sh_name = request.POST.get('sh_name')
        item.sh_model = request.POST.get('sh_model')
        item.sh_size = request.POST.get('sh_size')
        item.sh_color = request.POST.get('sh_color')
        item.sh_manufacturer = request.POST.get('sh_manufacturer')
        item.sh_count = request.POST.get('sh_count')
        item.sh_price = request.POST.get('sh_price')
        # item.sh_image = request.POST.get('sh_image')
        # images = request.FILES.getlist('sh_images')
        
        sh_image = request.FILES.get('sh_image')
        if sh_image:
            item.sh_image = sh_image
        item.save()
        return redirect('manager_app:items')
    else:
        return render(request, 'manager_edit/items-edit.html', {'item': item})


def update_user(request, user_id):
    user = get_object_or_404(Users, id_user = user_id)
    
    if request.method == 'POST':
        user.u_username = request.POST.get('u_username')
        user.u_name = request.POST.get('u_name')
        user.u_surname = request.POST.get('u_surname')
        user.u_email = request.POST.get('u_email')
        user.u_phone = request.POST.get('u_phone')
        user.u_status = request.POST.get('u_status') == True
        user.u_role = request.POST.get('u_role')
        user.save()
        return redirect('manager_app:users')
    else:
        user_roles = [(role.value, role.name) for role in User_role]
        return render(request, 'manager_edit/users-edit.html', {'user': user, 'user_roles': user_roles})
    

def update_order(request, order_id):
    order = get_object_or_404(Orders, id_order=order_id)
    shoes_list = Shoes.objects.all()

    if request.method == 'POST':
        o_shoes_id = request.POST.get('o_shoes')
        o_recipient = request.POST.get('o_recipient')
        o_address = request.POST.get('o_address')
        o_comment = request.POST.get('o_comment')
        o_status = request.POST.get('o_status')  # Retrieve o_status from POST data
        o_sum = request.POST.get('o_sum')
        o_user = request.POST.get('o_user')
        
        try:
            shoes = Shoes.objects.get(id_shoes=o_shoes_id)
        except Shoes.DoesNotExist:
            error_message = "Взуття з вказаним ідентифікатором не існує"
            messages.error(request, error_message) 
            return render(request, 'manager_edit/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
        
        # Перевіряємо, чи кількість взуття більше 0
        if shoes.sh_count > 0:
            # Отримуємо кількість, яку користувач ввів
            o_count = int(request.POST.get('o_count', 0))
           
            # Перевіряємо, чи введена кількість менше або дорівнює кількості в наявності
            if o_count <= shoes.sh_count:
                order.o_shoes = shoes
                order.o_count = o_count
                
                if o_status in [status.value for status in Order_status]:
                    order.o_status = o_status
                    order.o_recipient = o_recipient
                    order.o_address = o_address
                    order.o_comment = o_comment
                    order.save()
                    return redirect('manager_app:orders')
                else:
                    error_message = "Неправильний статус замовлення"
                    messages.error(request, error_message) 
                    return render(request, 'manager_edit/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                messages.error(request, error_message) 
                return render(request, 'manager_edit/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            messages.error(request, error_message) 
            return render(request, 'manager_edit/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
    else:
        order_status = [(status.value, status.name) for status in Order_status]
        return render(request, 'manager_edit/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'order_status': order_status})


def update_reservation(request, reservation_id):
    # Отримуємо об'єкт Shoes за його ідентифікатором
    reservation = get_object_or_404(Reservations, id_reservation=reservation_id)
    
    shoes_list = Shoes.objects.all()
    if request.method == 'POST':
        r_shoes_id = request.POST.get('r_shoes')
        try:
            shoes = Shoes.objects.get(id_shoes=r_shoes_id)
        except Shoes.DoesNotExist:
            error_message = "Взуття з вказаним ідентифікатором не існує"
            return render(request, 'manager_edit/reservations-edit.html', {'reservation': reservation, 'error_message': error_message})
        
        # Перевіряємо, чи кількість взуття більше 0
        if shoes.sh_count > 0:
            # Отримуємо кількість, яку користувач ввів
            r_count = int(request.POST.get('r_count', 0))
            
            # Перевіряємо, чи введена кількість менше або дорівнює кількості в наявності
            if r_count <= shoes.sh_count:
                reservation.r_shoes = shoes
                reservation.r_count = r_count
                reservation.save()
                return redirect('manager_app:reservations')
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                return render(request, 'manager_edit/reservations-edit.html', {'reservation': reservation, 'shoes_list': shoes_list, 'error_message': error_message})
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            return render(request, 'manager_edit/reservations-edit.html', {'reservation': reservation,'shoes_list': shoes_list, 'error_message': error_message})
    else:
        return render(request, 'manager_edit/reservations-edit.html', {'reservation': reservation, 'shoes_list': shoes_list})   
   