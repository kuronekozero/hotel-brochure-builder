import tkinter
import tkinter.messagebox
from idlelib import editor

from PIL import Image, ImageDraw, ImageFont
import customtkinter
import requests
import json
import re
import os


def work_dir(pic_1): #def work_dir(pic_1, pic_2, pic_3):
    pic_1 = pic_1.replace(" ", "")
    # pic_2 = pic_2.replace(" ", "")
    # pic_3 = pic_3.replace(" ", "")
    if not os.path.isdir("Hotel-Brochure-Builder"):
        os.mkdir("Hotel-Brochure-Builder")
    if not os.path.isdir("Hotel-Brochure-Builder/tmp"):
        os.mkdir("Hotel-Brochure-Builder/tmp")

    if os.path.exists("Hotel-Brochure-Builder/tmp/pic_1.jpg"):
        os.remove("Hotel-Brochure-Builder/tmp/pic_1.jpg")
    p = requests.get(pic_1[0:(len(pic_1) - 1)])
    out = open("Hotel-Brochure-Builder/tmp/pic_1.jpg", "wb")
    out.write(p.content)
    out.close()

    # if os.path.exists("Hotel-Brochure-Builder/tmp/pic_2.jpg"):
    #     os.remove("Hotel-Brochure-Builder/tmp/pic_2.jpg")
    # p = requests.get(pic_2[0:(len(pic_2) - 1)])
    # out = open("Hotel-Brochure-Builder/tmp/pic_2.jpg", "wb")
    # out.write(p.content)
    # out.close()
    #
    # if os.path.exists("Hotel-Brochure-Builder/tmp/pic_3.jpg"):
    #     os.remove("Hotel-Brochure-Builder/tmp/pic_3.jpg")
    # p = requests.get(pic_3[0:(len(pic_3) - 1)])
    # out = open("Hotel-Brochure-Builder/tmp/pic_3.jpg", "wb")
    # out.write(p.content)
    # out.close()


def keypress(e):
    if e.keycode == 86 and e.keysym != 'v':
        widget = app.focus_get()
        widget.event_generate("<<Paste>>")
    elif e.keycode == 67 and e.keysym != 'c':
        widget = app.focus_get()
        widget.event_generate("<<Copy>>")
    elif e.keycode == 88 and e.keysym != 'x':
        widget = app.focus_get()
        widget.event_generate("<<Cut>>")


def pars_url(enter_url):
    if enter_url.find("d=") != -1:
        x = enter_url[(enter_url.find("d=") + 2):len(enter_url)]
        x = x.replace(" ", "")
        enter_url = "https://tourvisor.ru/xml/modact.php?currency=0&shortid=" + x + "&session=f2be8b233ce2bd47ab598b39b5416591b60831c2cd2a257c45f4fee092118875c4934acf41a15ad15a4fe2088fc4d0df93d79e9780883e6ddf3b75368285f88773a4bfbb42193ce18de24c15fc2f15b0"
    else:
        textbox.delete("0.0", "end")
        textbox.insert("0.0", "Неправильный формат ссылки")
    return enter_url


def button_function_pars():
    # УДАЛИТЬ
    textbox.insert("0.0", "https://diplomat-tour.ru/tours#tvtourid=3071148563")
    textbox2.insert("0.0", "https://static.tourvisor.ru/hotel_pics/verybig/4/ela-quality-102202340.jpg")
    # УДАЛИТЬ

    ent_url = textbox.get("0.0", "end")
    ent_pic_1 = textbox2.get("0.0", "end")
    # ent_pic_2 = textbox3.get("0.0", "end")
    # ent_pic_3 = textbox4.get("0.0", "end")

    url = pars_url(ent_url)
    try:
        work_dir(ent_pic_1)  #work_dir(ent_pic_1, ent_pic_2, ent_pic_3)
    except Exception:
        print("Отсутствуют фотографии")

    photo_collection = ""  # фото коллекция
    country = ""  # страна

    departure_date = ""  # дата вылета
    number_of_nights = ""  # кол-во ночей

    room_type = ""  # тип номера
    type_of_food = ""  # тип питания

    price = ""  # цена
    rating = ""  # рейтинг

    hotel_name = ""  # название отеля
    stars = ""  # звезды

    resort_name = ""  # название курорта
    beach = ""  # пляж
    year_restoration = "Последняя реставрация: "  # год реставрации

    payload = {}
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "tourvisor.ru",
        "Origin": "https://diplomat-tour.ru",
        "Referer": "https://diplomat-tour.ru/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data_json = response.text
        data = json.loads(data_json)
    except Exception:
        textbox.delete("0.0", "end")
        textbox.insert("0.0", "Получение данных не удалось")

    try:
        photo_collection = ""  # фото коллекция
        country += data["data"]["tour"]["countryname"]  # страна
        textbox51.delete("0.0", "end")
        textbox51.insert("0.0", country)
        departure_date += data["data"]["tour"]["flydate"]  # дата вылета
        textbox52.delete("0.0", "end")
        textbox52.insert("0.0", departure_date)
        number_of_nights += str(data["data"]["tour"]["nights"])  # кол-во ночей
        textbox53.delete("0.0", "end")
        textbox53.insert("0.0", number_of_nights)
        room_type += data["data"]["tour"]["room"]  # тип номера
        textbox91.delete("0.0", "end")
        textbox91.insert("0.0", room_type)

        type_of_food += data["data"]["tour"]["meal"]  # тип питания
        if type_of_food == "BB":
            type_of_food = "BB - Только завтрак"
        if type_of_food == "HB":
            type_of_food = "HB - Завтрак, ужин"
        if type_of_food == "FB":
            type_of_food = "FB - Полный пансион"
        if type_of_food == "AI":
            type_of_food = "AI - Все включено"
        if type_of_food == "UAI":
            type_of_food = "UAI - Ультра все включено"

        textbox81.delete("0.0", "end")
        textbox81.insert("0.0", type_of_food)
        price += str(data["data"]["tour"]["price"])  # цена
        textbox61.delete("0.0", "end")

        price = format_price(price)

        textbox61.insert("0.0", price)
        rating += str(data["data"]["hotel"]["rating"])  # рейтинг
        textbox62.delete("0.0", "end")
        textbox62.insert("0.0", rating)
        hotel_name += data["data"]["hotel"]["hotelname"]  # название отеля
        hotel_name = re.sub(r'\(.*?\)', '', hotel_name).strip()
        textbox7.delete("0.0", "end")
        textbox7.insert("0.0", hotel_name)
        stars = data["data"]["hotel"]["hotelstars"]  # звезды
        textbox63.delete("0.0", "end")
        textbox63.insert("0.0", stars)
        resort_name += data["data"]["hotel"]["hotelregionname"]  # название курорта
        textbox92.delete("0.0", "end")
        textbox92.insert("0.0", resort_name)
        beach += data["data"]["hotel"]["detail"]["beach"]  # пляж
        beach = beach.replace("</LI><LI>", '\n')
        pattern = re.compile(r'<.*?>')
        beach = re.sub(pattern, '', beach)
        textbox100.delete("0.0", "end")
        textbox100.insert("0.0", beach)

        year_restoration += data["data"]["hotel"]["detail"]["repair"]  # год реставрации
        textbox82.delete("0.0", "end")
        textbox82.insert("0.0", year_restoration)
    except Exception:
        print('Один из пунктов отсутствует')

def button_function_create():
    """
    Func creates final images with hotels
    :return: hotel image
    """
    departure_date = textbox52.get("0.0", "end")  # дата вылета
    departure_date = "Дата вылета: " + departure_date

    number_of_nights = textbox53.get("0.0", "end")  # кол-во ночей
    number_of_nights = "Кол-во ночей: " + number_of_nights

    room_type = textbox91.get("0.0", "end")  # тип номера
    room_type = "Тип номера: " + room_type

    type_of_food = textbox81.get("0.0", "end")  # тип питания
    type_of_food = "Тип питания: " + type_of_food

    price = textbox61.get("0.0", "end")  # цена

    rating = textbox62.get("0.0", "end")  # рейтинг
    hotel_name = textbox7.get("0.0", "end")  # название отеля
    stars = textbox63.get("0.0", "end")  # звезды

    resort_name = textbox92.get("0.0", "end")  # название курорта
    beach = textbox100.get("0.0", "end")  # пляж
    year_restoration = textbox82.get("0.0", "end")  # год реставрации

    country = textbox51.get("0.0", "end").strip()
    country += ", " + resort_name

    # Открываем изображение
    original_image = Image.open("Hotel-Brochure-Builder/tmp/pic_1.jpg")
    # Открываем изображение шаблона
    template_image = Image.open("template.png")

    # Вызываем функцию crop_to_aspect_ratio
    cropped_image = crop_to_aspect_ratio(original_image, 12 / 8)

    cropped_resized_image = resize_image(cropped_image, 2048)

    hotel_image_height = cropped_resized_image.size[1]

    white_background = create_white_background(2730 - hotel_image_height, 2048)

    # Создаем новое изображение с нужными размерами
    new_image = Image.new('RGB', (2048, 2730))

    # Вставляем изображение отеля и белый фон в нужные места
    new_image.paste(cropped_resized_image, (0, 0))
    new_image.paste(white_background, (0, hotel_image_height))

    # Накладываем изображение шаблона на новое изображение
    new_image.paste(template_image, (0, 0), template_image)

    # Создаем объект ImageDraw для нового изображения
    draw = ImageDraw.Draw(new_image)

    # Загружаем шрифт
    bold_name = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 180) # hotel's font
    bold_price = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 220) # price's font
    semibold = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 80) # country's name/resort
    regular = ImageFont.truetype("fonts/Montserrat-Regular.ttf", 80) # departure date/number of nights
    medium = ImageFont.truetype("fonts/Montserrat-Medium.ttf", 60) # beach info/hotel info

    def draw_centered_text(draw, text, y, font, fill=(0, 0, 0)):
        text_width, _ = font.getsize(text)
        x = (new_image.width - text_width) // 2
        draw.text((x, y), text, fill=fill, font=font)

    # # Вычисляем ширину текста
    # text_width, _ = bold_name.getsize(hotel_name)
    # # Вычисляем координату X для центрирования текста
    # x = (2048 - text_width) // 2
    # # Добавляем текст на изображение
    # draw.text((x, 1120), hotel_name, fill=(32, 32, 32), font=bold_name)

    draw_centered_text(draw, hotel_name, 1120, bold_name, fill=(32, 32, 32))

    def draw_stars(stars):
        """
        This func draws stars on the final image
        :param stars:
        :return:
        """
        stars = int(stars)
        # Открываем изображение звезд
        stars_image = Image.open(f"stars/{stars} star.png")

        # Накладываем изображение звезд на новое изображение
        new_image.paste(stars_image, (620, 1320), stars_image)  # замените x и y на нужные координаты

    draw_stars(stars)

    draw.text((670, 1500), country, fill=(32, 32, 32), font=semibold)
    # draw.text((650, 1000), resort_name, fill="black", font=semibold)
    # draw_centered_text(draw, country, 1500, semibold, fill=(32, 32, 32))

    draw.text((530, 1600), price, fill=(0, 128, 255), font=bold_price)
    # draw_centered_text(draw, price, 1600, bold_price, fill=(0, 128, 255))
    # draw.text((540, 1850), departure_date, fill="black", font=regular)
    draw_centered_text(draw, departure_date, 1850, regular, fill="black")
    # draw.text((640, 1950), number_of_nights, fill="black", font=regular)
    draw_centered_text(draw, number_of_nights, 1950, regular, fill="black")

    draw.text((50, 2250), beach, fill="black", font=medium)


    draw.text((1100, 2250), type_of_food, fill="black", font=medium)

    draw.text((1100, 2300), room_type, fill="black", font=medium)
    draw.text((1100, 2350), year_restoration, fill="black", font=medium)

    if rating == 0:
        pass
    else:
        rating = "Рейтинг: " + rating
        draw.text((1100, 2400), rating, fill="black", font=medium)

    # Сохраняем новое изображение
    new_image.save("Hotel-Brochure-Builder/tmp/output/final_image.jpg")

    # print(country, departure_date, number_of_nights, room_type, type_of_food, price, rating, hotel_name, stars, resort_name, beach, year_restoration, sep="")

def format_price(price):
    price = int(price)  # преобразование строки в число
    return "{:,}₽".format(price).replace(",", " ")

def crop_to_aspect_ratio(image, aspect_ratio):
    width, height = image.size
    new_width = min(width, int(height * aspect_ratio))
    new_height = int(new_width / aspect_ratio)

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    return image.crop((left, top, right, bottom))

def resize_image(image, size):
    width, height = image.size

    max_width = size
    max_height = int(max_width * height / width)

    return image.resize((max_width, max_height), Image.ANTIALIAS)

def create_white_background(height, width):
    return Image.new('RGB', (width, height), 'white')

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("Hotel Brochure Builder")
app.geometry("600x800")

app.bind("<Control-KeyPress>", keypress)

deflt_relx = 0.04
otnrely = 0.07
counter_y = 0

label_1_y = 0.01
textbox_1_y = 0.04

logo_label = customtkinter.CTkLabel(app, text="Основная ссылка", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label.place(relx=deflt_relx, rely=label_1_y + otnrely * counter_y)
textbox = customtkinter.CTkTextbox(app, height=25)
textbox.place(relx=deflt_relx, rely=textbox_1_y + otnrely * counter_y, relwidth=1 - deflt_relx * 2)
counter_y += 1

logo_label2 = customtkinter.CTkLabel(app, text="Фото общего вида", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label2.place(relx=deflt_relx, rely=label_1_y + otnrely * counter_y)
textbox2 = customtkinter.CTkTextbox(app, height=25)
textbox2.place(relx=deflt_relx, rely=textbox_1_y + otnrely * counter_y, relwidth=1 - deflt_relx * 2)
counter_y += 1

# logo_label3 = customtkinter.CTkLabel(app, text="Фото пляжа", font=customtkinter.CTkFont(size=14, weight="bold"))
# logo_label3.place(relx=deflt_relx, rely=label_1_y +otnrely*counter_y)
# textbox3 = customtkinter.CTkTextbox(app, height=25)
# textbox3.place(relx=deflt_relx, rely=textbox_1_y  +otnrely*counter_y , relwidth=1-deflt_relx*2)
# counter_y += 1
#
# logo_label4 = customtkinter.CTkLabel(app, text="Фото комнаты", font=customtkinter.CTkFont(size=14, weight="bold"))
# logo_label4.place(relx=deflt_relx, rely=label_1_y +otnrely*counter_y)
# textbox4 = customtkinter.CTkTextbox(app, height=25)
# textbox4.place(relx=deflt_relx, rely=textbox_1_y  +otnrely*counter_y , relwidth=1-deflt_relx*2)
# counter_y += 1

button = customtkinter.CTkButton(master=app, text="Получить данные", command=button_function_pars)
button.place(relx=deflt_relx, rely=0.03 + otnrely * counter_y, relwidth=1 - deflt_relx * 2)
counter_y += 1

label_2_y = 0.02
textbox_2_y = 0.05

logo_label51 = customtkinter.CTkLabel(app, text="Cтрана", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label51.place(relx=deflt_relx, rely=label_2_y + otnrely * counter_y)
textbox51 = customtkinter.CTkTextbox(app, height=25)
textbox51.place(relx=deflt_relx, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 3 - 0.01)  # страна
logo_label52 = customtkinter.CTkLabel(app, text="Дата вылета", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label52.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3, rely=label_2_y + otnrely * counter_y)
textbox52 = customtkinter.CTkTextbox(app, height=25)
textbox52.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 3 - 0.01)  # дата вылета
logo_label53 = customtkinter.CTkLabel(app, text="Кол-во ночей", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label53.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3 * 2, rely=label_2_y + otnrely * counter_y)
textbox53 = customtkinter.CTkTextbox(app, height=25)
textbox53.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3 * 2, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 3 - 0.01)  # кол-во ночей
counter_y += 1

logo_label61 = customtkinter.CTkLabel(app, text="Цена тура", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label61.place(relx=deflt_relx, rely=label_2_y + otnrely * counter_y)
textbox61 = customtkinter.CTkTextbox(app, height=25)
textbox61.place(relx=deflt_relx, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 3 - 0.01)  # цена
logo_label62 = customtkinter.CTkLabel(app, text="Рейтинг отеля", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label62.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3, rely=label_2_y + otnrely * counter_y)
textbox62 = customtkinter.CTkTextbox(app, height=25)
textbox62.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 3 - 0.01)  # рейтинг
logo_label63 = customtkinter.CTkLabel(app, text="Кол-во звезд", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label63.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3 * 2, rely=label_2_y + otnrely * counter_y)
textbox63 = customtkinter.CTkTextbox(app, height=25)
textbox63.place(relx=deflt_relx + (1 - deflt_relx * 2) / 3 * 2, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 3 - 0.01)  # звезды
counter_y += 1

logo_label7 = customtkinter.CTkLabel(app, text="Название отеля", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label7.place(relx=deflt_relx, rely=label_2_y + otnrely * counter_y)
textbox7 = customtkinter.CTkTextbox(app, height=25)
textbox7.place(relx=deflt_relx, rely=textbox_2_y + otnrely * counter_y, relwidth=1 - deflt_relx * 2)  # название отеля
counter_y += 1

logo_label81 = customtkinter.CTkLabel(app, text="Тип питания", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label81.place(relx=deflt_relx, rely=label_2_y + otnrely * counter_y)
textbox81 = customtkinter.CTkTextbox(app, height=25)
textbox81.place(relx=deflt_relx, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 2 - 0.01)  # тип питания
logo_label82 = customtkinter.CTkLabel(app, text="Год реставрации", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label82.place(relx=deflt_relx + (1 - deflt_relx * 2) / 2, rely=label_2_y + otnrely * counter_y)
textbox82 = customtkinter.CTkTextbox(app, height=25)
textbox82.place(relx=deflt_relx + (1 - deflt_relx * 2) / 2, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 2 - 0.01)  # год реставрации
counter_y += 1

logo_label91 = customtkinter.CTkLabel(app, text="Тип номера", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label91.place(relx=deflt_relx, rely=label_2_y + otnrely * counter_y)
textbox91 = customtkinter.CTkTextbox(app, height=25)
textbox91.place(relx=deflt_relx, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 2 - 0.01)  # тип номера
logo_label92 = customtkinter.CTkLabel(app, text="Название курорта", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label92.place(relx=deflt_relx + (1 - deflt_relx * 2) / 2, rely=label_2_y + otnrely * counter_y)
textbox92 = customtkinter.CTkTextbox(app, height=25)
textbox92.place(relx=deflt_relx + (1 - deflt_relx * 2) / 2, rely=textbox_2_y + otnrely * counter_y,
                relwidth=(1 - deflt_relx * 2) / 2 - 0.01)  # название курорта
counter_y += 1

logo_label100 = customtkinter.CTkLabel(app, text="Пляж", font=customtkinter.CTkFont(size=14, weight="bold"))
logo_label100.place(relx=deflt_relx, rely=label_2_y + otnrely * counter_y)
textbox100 = customtkinter.CTkTextbox(app, height=75)
textbox100.place(relx=deflt_relx, rely=textbox_2_y + otnrely * counter_y, relwidth=1 - deflt_relx * 2)  # пляж
counter_y += 1
counter_y += 1

button = customtkinter.CTkButton(master=app, text="Создать", command=button_function_create, height=50)
button.place(relx=deflt_relx, rely=0.03 + otnrely * counter_y, relwidth=1 - deflt_relx * 2)
counter_y += 1

app.mainloop()
