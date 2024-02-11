from tkinter import Button

from PIL import ImageTk, Image

from canvas import frame, root
from helpers import clean_screen
from json import load, dump


def display_products():
    clean_screen()
    display_stock()


def display_stock():
    with open("db/products.json") as stock:
        info = load(stock)

    x, y = 150, 50

    for item_name, item_info in info.items():
        img = Image.open(item_info['image'])
        resized_image = img.resize((100, 150))
        item_image = ImageTk.PhotoImage(resized_image)
        images.append(item_image)  # keeping a reference of
        # the images so the tkinter garbage collector doesn't delete them

        frame.create_text(x, y, text=item_name, font=('Arial', 11))
        frame.create_image(x, y + 100, image=item_image)

        if item_info["quantity"] > 0:
            color = "green"
            text = f"In stock {item_info['quantity']}"

            item_button = Button(
                root,
                text="Buy",
                bg="green",
                font=('Arial', 11),
                bd=0,
                command=lambda item=item_name, item_details=info: buy_product(item, item_details)
            )

            frame.create_window(x, y + 230, window=item_button)

        else:
            color = "red"
            text = "Out of stock"

        frame.create_text(x, y + 200, text=text, fill=color, font=('Arial', 11, 'bold'))

        x += 200
        if x >= 550:
            y += 270
            x = 150


def buy_product(product_name, info):
    info[product_name]["quantity"] -= 1

    with open("db/products.json", "w") as stock:
        dump(info, stock)

    display_products()


images = []
