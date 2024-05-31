from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from manager_app.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
import plotly.express as px
from datetime import datetime,timedelta

def items(request):
    data = Shoes.objects.all()
    return render(request, 'manager_app/items.html', {'data': data})


def items_detailed_view(request, id):
    item = get_object_or_404(Shoes, id_shoes=id)
    # Either render only the modal content, or a full standalone page
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        template_name = 'manager_app/items.html'
    else:
        template_name = 'manager_app/items.html'
    return render(request, template_name, {'item':item})
    

    
def items_delete(request, shoes_id):
    item = get_object_or_404(Shoes, id_shoes = shoes_id)

    if request.method == 'POST':
        item.delete()
        return redirect('manager_app:items')

    return redirect('manager_app:items')

def users(request):
    # return render(request, 'users.html')
    data = Users.objects.all()
    return render(request, 'manager_app/users.html', {'data': data})

def users_toggle_status(request, user_id):
    user = get_object_or_404(Users, id_user=user_id)
    if user.u_status != True:
       user.u_status = True
    else:
        redirect('manager_app:users')
    user.save()
    return redirect('manager_app:users')

def users_delete(request, user_id):
    user = get_object_or_404(Users, id_user = user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('manager_app:users')

    return redirect('manager_app:users')

    
def orders(request):
    # return render(request, 'orders.html')
    data = Orders.objects.all()
    for item in data:
        item.order_sum = item.o_count * item.o_shoes.sh_price
    order_status = [(status.value, status.name) for status in Order_status]
    return render(request, 'manager_app/orders.html', {'data': data, 'order_status': order_status})

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
        return redirect('manager_app:orders')

    return redirect('manager_app:orders')


# def order_sum_view(request):
    # total_sum = Orders.objects.aggregate(total_sum=Sum(F('o_count') * F('o_shoes__sh_price')))
    # order_sum = total_sum['total_sum'] if total_sum['total_sum'] else 0
    # return render(request, 'orders.html', {'order_sum': order_sum})


def reservations(request):
    # return render(request, 'orders.html')
    now = timezone.now()
    Reservations.objects.filter(r_end_date__lt=now).delete()

    data = Reservations.objects.all()
    return render(request, 'manager_app/reservations.html', {'data': data})

def reservations_delete(request, reservation_id):
    reservation = get_object_or_404(Reservations, id_reservation = reservation_id)

    if request.method == 'POST':
        reservation.delete()
        return redirect('manager_app:reservations')

    return redirect('manager_app:reservations')

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
                return redirect('manager_app:reservations')
            else:
                error_message = "Вибрана кількість перевищує кількість в наявності"
                return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation, 'shoes_list': shoes_list, 'error_message': error_message})
        else:
            error_message = "Вибране взуття відсутнє в наявності"
            return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation,'shoes_list': shoes_list, 'error_message': error_message})
    else:
        return render(request, 'manager_app/reservations-edit.html', {'reservation': reservation, 'shoes_list': shoes_list})   
   
   
def analytics_for_admin(request):
    total_sum = Orders.calculate_total_sum()
    average_sum = Orders.calculate_average_sum()
    max_sum = Orders.find_max_sum()
    min_sum = Orders.find_min_sum()

    current_month = datetime.now().month
    total_sum_for_current_month = Orders.calculate_total_sum_for_current_month()
    context = {
        'total_sum': total_sum,
        'average_sum': average_sum,
        'max_sum': max_sum,
        'min_sum': min_sum,
        'total_sum_for_current_month': total_sum_for_current_month
    }
    # orders = Orders.objects.all()

    # fig = px.line(
    #     x=[order.o_date_created for order in orders], 
    #     y=[order.o_sum for order in orders]
    #     )
    # chart = fig.write_html()
    # context1 = {'chart': chart}

    return render(request, 'manager_app/analytics_for_admin.html', context)

def analytics_for_user(request):
    return render(request, 'manager_app/analytics_for_user.html')

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



# def analytics_view(request):
#     orders = Orders.objects.all()

#     fig = px.line(
#         x=[order.o_date_created for order in orders], 
#         y=[order.o_sum for order in orders]
#         )
#     chart = fig.show()
#     context = {'chart': chart}
#     return render(request, 'manager_app/analytics.html', context)


# def analytics_view (request):
#     fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
#     fig.show()
#     return render(request, 'manager_app/analytics.html', {'fig': fig})