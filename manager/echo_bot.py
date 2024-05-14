import telebot
from telebot import types
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()
from manager_app.models import *
from datetime import datetime, timedelta

bot = telebot.TeleBot("7016034202:AAE_2JBKktW-Sx_QLHenOrtBQY7s8F5ZUL4", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['register'])
def register_user(message):
    sender_chat_id = message.chat.id
    sender_username = message.from_user.username

    # Перевіряємо, чи є користувач в базі даних
    user, created = Users.objects.get_or_create(id_user=sender_chat_id, defaults={'u_username': sender_username})

    if created:
        # Якщо користувач ще не зареєстрований, просимо його ввести інші дані
        bot.send_message(message.chat.id, "Дякуємо за реєстрацію! Тепер натисніть кнопку нижче, щоб надіслати свій номер телефону.")
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton(text="Надіслати номер телефону", request_contact=True)
        keyboard.add(button)
        bot.send_message(message.chat.id, "Натисніть кнопку нижче, щоб надіслати свій номер телефону.", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_phone, user)
    else:
        # Якщо користувач вже зареєстрований, повідомляємо про це
        bot.send_message(message.chat.id, "Ви вже зареєстровані у нашій системі.")

def process_phone(message, user):
    # Отримуємо номер телефону з отриманого контакту
    phone_number = message.contact.phone_number
    user.u_phone = phone_number
    bot.send_message(message.chat.id, "Дякуємо за надіслання номера телефону. Тепер будь ласка, введіть ваше ім'я:")
    bot.register_next_step_handler(message, process_name, user)

def process_name(message, user):
    user.u_name = message.text
    bot.send_message(message.chat.id, "Тепер будь ласка, введіть ваше прізвище:")
    bot.register_next_step_handler(message, process_surname, user)

def process_surname(message, user):
    user.u_surname = message.text
    bot.send_message(message.chat.id, "Тепер будь ласка, введіть ваш email (якщо немає - просто натисніть Enter):")
    bot.register_next_step_handler(message, process_email, user)

def process_email(message, user):
    email = message.text
    if email:
        user.u_email = email
    user.save()
    bot.send_message(message.chat.id, "Дякуємо за введення інформації. Ви успішно зареєстровані!")
 
@bot.message_handler(commands=['create_order'])
def add_order(message):
    sender_chat_id = message.chat.id
    
    try:
        user = Users.objects.get(id_user=sender_chat_id)
        # Перевіряємо, чи користувач вже зареєстрований
        if user:
            if user.u_status:
                bot.send_message(message.chat.id, "Введіть ID товару:")
                # Очікувати відповідь користувача
                bot.register_next_step_handler(message, process_shoes_id)
            else:
                bot.send_message(message.chat.id, "Вибачте, ваш акаунт не активний. Зверніться до адміністратора.")
    except Users.DoesNotExist:
        # Якщо користувача не знайдено, просимо його спочатку зареєструватися
        bot.send_message(message.chat.id, "Ви ще не зареєстровані. Скористайтеся командою /register.")

def process_shoes_id(message):
    try:
        shoes_id = int(message.text)
        try:
            shoes = Shoes.objects.get(id_shoes=shoes_id)
            info_message = f"Інформація про товар:\nНазва: {shoes.sh_name}\nМодель: {shoes.sh_model}\nРозмір: {shoes.sh_size}\nКолір: {shoes.sh_color}\nЦіна: {shoes.sh_price} грн"
            bot.send_message(message.chat.id, info_message)
            bot.send_message(message.chat.id, "Бажаєте зробити замовлення? (Так / Ні)")
            bot.register_next_step_handler(message, process_order_confirmation, shoes)
        except Shoes.DoesNotExist:
            bot.send_message(message.chat.id, "Товар з таким ID не знайдено. Спробуйте ввести інший ID.")
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення ID товару. Введіть ціле число.")

def process_order_confirmation(message, shoes):
    try:
        user = Users.objects.get(id_user=message.chat.id)
        if message.text.lower() == "так":
            bot.send_message(message.chat.id, "Введіть кількість товару:")
            bot.register_next_step_handler(message, process_quantity, shoes, user)
        else:
            bot.send_message(message.chat.id, "Добре, якщо вам знадобиться допомога з замовленням, не соромтесь звертатися!")
    except Users.DoesNotExist:
        bot.send_message(message.chat.id, "Вибачте, але ваш обліковий запис не знайдено. Зареєструйтесь за допомогою команди /register.")

def process_quantity(message, shoes, user):
    try:
        quantity = int(message.text)
        if quantity <= 0:
            raise ValueError("Кількість має бути більше нуля.")
        elif quantity > shoes.sh_count:
            bot.send_message(message.chat.id, f"В наявності лише {shoes.sh_count} одиниць цього товару. Введіть іншу кількість:")
            bot.register_next_step_handler(message, process_quantity, shoes, user)
            return
        bot.send_message(message.chat.id, "Введіть отримувача (ім'я та прізвище):")
        bot.register_next_step_handler(message, process_recipient, shoes, user, quantity)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення кількості. Введіть ціле число більше нуля:")
        bot.register_next_step_handler(message, process_quantity, shoes, user)
    except Exception as e:
        bot.send_message(message.chat.id, f"Під час обробки кількості виникла помилка: {e}")

def process_recipient(message, shoes, user, quantity):
    recipient = message.text
    bot.send_message(message.chat.id, "Вкажіть адресу доставки:")
    bot.register_next_step_handler(message, process_address, shoes, user, quantity, recipient)

def process_address(message, shoes, user, quantity, recipient):
    address = message.text
    bot.send_message(message.chat.id, "Якщо є коментар до замовлення, вкажіть його. Якщо немає, просто натисніть Enter:")
    bot.register_next_step_handler(message, process_comment, shoes, user, quantity, recipient, address)

def process_comment(message, shoes, user, quantity, recipient, address):
    comment = message.text
    try:
        order = Orders.objects.create(
            o_user=user,
            o_shoes=shoes,
            o_count=quantity,
            o_sum=shoes.sh_price * quantity,
            o_recipient=recipient,
            o_address=address,
            o_comment=comment if comment else None
        )
        bot.send_message(message.chat.id, "Замовлення успішно створено!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Під час створення замовлення виникла помилка: {e}")
        print({e})


@bot.message_handler(commands=['create_reservation'])
def add_reservation(message):
    sender_chat_id = message.chat.id
    
    try:
        user = Users.objects.get(id_user=sender_chat_id)
        # Перевіряємо, чи користувач вже зареєстрований
        if user:
            if user.u_status:
                bot.send_message(message.chat.id, "Введіть ID товару:")
                # Очікувати відповідь користувача
                bot.register_next_step_handler(message, process_shoes_id)
            else:
                bot.send_message(message.chat.id, "Вибачте, ваш акаунт не активний. Зверніться до адміністратора.")
    except Users.DoesNotExist:
        # Якщо користувача не знайдено, просимо його спочатку зареєструватися
        bot.send_message(message.chat.id, "Ви ще не зареєстровані. Скористайтеся командою /register.")

def process_shoes_id(message):
    try:
        shoes_id = int(message.text)
        try:
            shoes = Shoes.objects.get(id_shoes=shoes_id)
            info_message = f"Інформація про товар:\nНазва: {shoes.sh_name}\nМодель: {shoes.sh_model}\nРозмір: {shoes.sh_size}\nКолір: {shoes.sh_color}\nЦіна: {shoes.sh_price} грн"
            bot.send_message(message.chat.id, info_message)
            # Створюємо клавіатуру з кнопкою "Бронювання"
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_reservation = types.KeyboardButton('Бронювання')
            keyboard.add(button_reservation)
            bot.send_message(message.chat.id, "Натисніть 'Бронювання', щоб підтвердити бронювання.", reply_markup=keyboard)
            # Зберігаємо дані про обране взуття для подальшої обробки
            bot.register_next_step_handler(message, process_reservation_confirmation, shoes)
        except Shoes.DoesNotExist:
            bot.send_message(message.chat.id, "Товар з таким ID не знайдено. Спробуйте ввести інший ID.")
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення ID товару. Введіть ціле число.")

def process_reservation_confirmation(message, shoes):
    user_chat_id = message.chat.id
    user = Users.objects.get(id_user=user_chat_id)
    bot.send_message(message.chat.id, "Введіть кількість товару:")
    # Замість bot.register_next_step_handler(message, process_quantity, shoes, user)
    # Ми реєструємо наступний крок з новою функцією, яка очікує кількість товару
    bot.register_next_step_handler(message, lambda msg: process_quantity(msg, shoes, user, user_chat_id))

def process_quantity(message, shoes, user, user_chat_id):
    try:
        count = int(message.text)
        if count > 0:
            end_date = datetime.now() + timedelta(hours=3)
            reservation = Reservations.objects.create(
                r_shoes=shoes,
                r_count=count,
                r_start_date=datetime.now(),
                r_end_date=end_date,
                r_user=user
            )
            bot.send_message(user_chat_id, "Бронювання підтверджено. Дякуємо!")
        else:
            bot.send_message(user_chat_id, "Некоректне значення кількості. Введіть ціле додатнє число.")
    except ValueError:
        bot.send_message(user_chat_id, "Некоректне значення кількості. Введіть ціле додатнє число.")





bot.infinity_polling()