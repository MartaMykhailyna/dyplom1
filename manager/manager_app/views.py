from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from manager_app.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

def index(request):
    return render(request, 'manager_app/index.html')

def items(request):
    data = Shoes.objects.all()
    return render(request, 'manager_app/items.html', {'data': data})


def items_detailed_view(request, id):
    item = get_object_or_404(Shoes, id_shoes=id)
    photos = ShoesImages.objects.filter(item=item)
    # Either render only the modal content, or a full standalone page
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        template_name = 'manager_app/items.html'
    else:
        template_name = 'manager_app/items.html'
    return render(request, template_name, {
        'item':item,
        'photos':photos
    })
    
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
        item.sh_image = request.POST.get('sh_image')
        images = request.FILES.getlist('sh_images')
        
        # Оновлюємо дані предмета
        for img in images:
            ShoesImages.objects.create(item=item, images=img)
        item.save()
        return redirect('items')
    else:
        return render(request, 'manager_app/items-edit.html', {'item': item})
    
def items_delete(request, shoes_id):
    item = get_object_or_404(Shoes, id_shoes = shoes_id)

    if request.method == 'POST':
        item.delete()
        return redirect('items')

    return redirect('items')

# def items_form_edit(request, id):
#     item = get_object_or_404(Shoes, id_shoes=id)
#     photos = ShoesImages.objects.filter(item=item)
#     # Either render only the modal content, or a full standalone page
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         template_name = 'manager_app/items.html'
#         if request.method == 'POST':
#             item.sh_name = request.POST.get('sh_name')
#             item.sh_model = request.POST.get('sh_model')
#             item.sh_size_array = request.POST.get('sh_size_array')
#             item.sh_color = request.POST.get('sh_color')
#             item.sh_manufacturer = request.POST.get('sh_manufacturer')
#             item.sh_count = request.POST.get('sh_count')
#             item.sh_price = request.POST.get('sh_price')
#             item.sh_image = request.POST.get('sh_image')
#             item.save()
#             return redirect('items')
#     else:
#         template_name = 'manager_app/items.html'
#     return render(request, template_name, {
#         'item':item,
#         'photos':photos
#     })

def users(request):
    # return render(request, 'users.html')
    data = Users.objects.all()
    return render(request, 'manager_app/users.html', {'data': data})

def users_toggle_status(request, user_id):
    user = get_object_or_404(Users, id_user=user_id)
    if user.u_status != True:
       user.u_status = True
    else:
        redirect('users')
    user.save()
    return redirect('users')

def users_delete(request, user_id):
    user = get_object_or_404(Users, id_user = user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('users')

    return redirect('users')

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
        return redirect('users')
    else:
        user_roles = [(role.value, role.name) for role in User_role]
        return render(request, 'manager_app/users-edit.html', {'user': user, 'user_roles': user_roles})
    
def orders(request):
    # return render(request, 'orders.html')
    data = Orders.objects.all()
    for item in data:
        item.order_sum = item.o_count * item.o_shoes.sh_price
    return render(request, 'manager_app/orders.html', {'data': data})

def orders_detailed_view(request, id):
    item = get_object_or_404(Orders, id_order=id)
    # photos = ShoesImages.objects.filter(item=item)
    # Either render only the modal content, or a full standalone page
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        template_name = 'manager_app/orders.html'
    else:
        template_name = 'manager_app/orders.html'
    return render(request, template_name, {
        'item':item,  
    })
   
def orders_delete(request, order_id):
    order = get_object_or_404(Orders, id_order = order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('orders')

    return redirect('orders')

def update_order(request, order_id):
    # Отримуємо об'єкт Shoes за його ідентифікатором
    order = get_object_or_404(Orders, id_order=order_id)
    
    shoes_list = Shoes.objects.all()
    if request.method == 'POST':
        o_shoes_id = request.POST.get('o_shoes')
        o_recipient = request.POST.get('o_recipient')
        o_address = request.POST.get('o_address')
        o_comment = request.POST.get('o_comment')
        o_status = request.POST.get('o_status')
        o_sum = request.POST.get('o_sum')
        o_user = request.POST.get('o_user')
        try:
            shoes = Shoes.objects.get(id_shoes=o_shoes_id)
        except Shoes.DoesNotExist:
            error_message = "Взуття з вказаним ідентифікатором не існує"
            messages.error(request, error_message) 
            return render(request, 'manager_app/orders-edit.html', {'order': order, 'error_message': error_message})
        
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
                    return redirect('orders')
                else:
                    error_message = "Неправильний статус замовлення"
                    messages.error(request, error_message) 
                    return render(request, 'manager_app/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                messages.error(request, error_message) 
                return render(request, 'manager_app/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            messages.error(request, error_message) 
            return render(request, 'manager_app/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'error_message': error_message})
    else:
        order_status = [(status.value, status.name) for status in Order_status]
        return render(request, 'manager_app/orders-edit.html', {'order': order, 'shoes_list': shoes_list, 'order_status': order_status})

# def order_sum_view(request):
    # total_sum = Orders.objects.aggregate(total_sum=Sum(F('o_count') * F('o_shoes__sh_price')))
    # order_sum = total_sum['total_sum'] if total_sum['total_sum'] else 0
    # return render(request, 'orders.html', {'order_sum': order_sum})


def reservations(request):
    # return render(request, 'orders.html')
    data = Reservations.objects.all()
    return render(request, 'manager_app/reservations.html', {'data': data})

def reservations_delete(request, reservation_id):
    reservation = get_object_or_404(Reservations, id_reservation = reservation_id)

    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations')

    return redirect('reservations')

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
            return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation, 'error_message': error_message})
        
        # Перевіряємо, чи кількість взуття більше 0
        if shoes.sh_count > 0:
            # Отримуємо кількість, яку користувач ввів
            r_count = int(request.POST.get('r_count', 0))
            
            # Перевіряємо, чи введена кількість менше або дорівнює кількості в наявності
            if r_count <= shoes.sh_count:
                reservation.r_shoes = shoes
                reservation.r_count = r_count
                reservation.save()
                return redirect('reservations')
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation, 'shoes_list': shoes_list, 'error_message': error_message})
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation,'shoes_list': shoes_list, 'error_message': error_message})
    else:
        return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation, 'shoes_list': shoes_list})   
   
   
def analytics(request):
    return render(request, 'manager_app/analytics.html')

# orders_with_shoes_info = Orders.objects.select_related('o_shoes').all()

# for order in orders_with_shoes_info:
#     print("Замовлення ID:", order.id_order)
#     print("Колір взуття:", order.o_shoes.sh_color)
#     print("Модель взуття:", order.o_shoes.sh_model)

@receiver(post_save, sender=Orders)
def update_shoes_count_on_order_create(sender, instance, created, **kwargs):
    if created:
        shoes = instance.o_shoes
        shoes.sh_count -= instance.o_count
        shoes.save()

@receiver(post_save, sender=Reservations)
def update_shoes_count_on_reservation_create(sender, instance, created, **kwargs):
    if created:
        shoes = instance.r_shoes
        shoes.sh_count -= instance.r_count
        shoes.save()