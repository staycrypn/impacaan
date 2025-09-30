import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
import random
import requests
from io import BytesIO
from kivy.core.image import Image as CoreImage

# Mnemonica stack
MNEMONICA = [
    "4C", "2H", "7D", "3C", "4H", "6D", "AS", "5H", "9S", "2S", "QH", "3D", "QC",
    "8H", "6S", "5S", "9H", "KC", "2D", "JH", "3S", "8S", "6H", "10C", "5D", "KD",
    "2C", "3H", "8D", "5C", "KS", "JD", "8C", "10S", "KH", "JC", "7S", "10H", "AD",
    "4S", "7H", "4D", "AC", "9C", "JS", "QD", "7C", "QS", "10D", "6C", "AH", "9D"
]

FULL_DECK = MNEMONICA[:]

# Card image cache
IMAGE_CACHE = {}
CARD_URL = "https://deckofcardsapi.com/static/img/{code}.png"
BACK_URL = "https://deckofcardsapi.com/static/img/backBlue.png"

def load_card_image(code):
    if code in IMAGE_CACHE:
        return IMAGE_CACHE[code]
    try:
        url = CARD_URL.format(code=code)
        resp = requests.get(url)
        data = BytesIO(resp.content)
        img = CoreImage(data, ext="png")
        IMAGE_CACHE[code] = img
        return img
    except Exception as e:
        print("Error loading image:", e)
        return None

def load_back_image():
    if "BACK" in IMAGE_CACHE:
        return IMAGE_CACHE["BACK"]
    try:
        resp = requests.get(BACK_URL)
        data = BytesIO(resp.content)
        img = CoreImage(data, ext="png")
        IMAGE_CACHE["BACK"] = img
        return img
    except Exception as e:
        print("Error loading back:", e)
        return None

class Dot(Widget):
    """Super small white dot indicator"""
    def __init__(self, radius=4, color=(1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.color_val = color
        self.size_hint = (None, None)
        self.size = (radius, radius)
        with self.canvas:
            Color(*self.color_val)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

class ACAANHelper(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = [20, 20, 20, 20]
        self.spacing = 20
        Window.clearcolor = (0.12, 0.12, 0.12, 1)

        self.current_card = random.choice(FULL_DECK)
        self.current_number = random.randint(1, 52)
        self.change_card_mode = 'random'
        self.change_number_mode = 'random'

        # Title
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.title_label = Label(text="ACAAN Helper", font_size=28, color=(1,1,1,1), size_hint=(None,1))
        self.title_label.bind(texture_size=self.title_label.setter('size'))
        self.dot = Dot(radius=4, color=(1,1,1))
        self.dot.opacity = 0  # hidden by default
        title_layout.add_widget(self.title_label)
        title_layout.add_widget(self.dot)
        title_layout.add_widget(Widget())  # flexible spacer
        self.add_widget(title_layout)

        # Display layout
        display_layout = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=220)
        self.card_image = Image(size_hint=(None, None), size=(120,180))
        self.number_label = Label(text=f"Position: {self.current_number}", font_size=22, color=(1,1,1,1))
        display_layout.add_widget(self.card_image)
        display_layout.add_widget(self.number_label)
        self.add_widget(display_layout)

        # Buttons
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=60)
        self.change_card_btn = Button(text="Change Card", on_press=self.change_card_action, background_color=(0.2,0.2,0.2,1), color=(1,1,1,1))
        self.change_number_btn = Button(text="Change Number", on_press=self.change_number_action, background_color=(0.2,0.2,0.2,1), color=(1,1,1,1))
        btn_layout.add_widget(self.change_card_btn)
        btn_layout.add_widget(self.change_number_btn)
        self.add_widget(btn_layout)

        self.update_display()

    def update_display(self):
        img = load_card_image(self.current_card)
        if img:
            self.card_image.texture = img.texture
        self.number_label.text = f"Position: {self.current_number}"

        if MNEMONICA.index(self.current_card) + 1 == self.current_number:
            self.dot.opacity = 1
        else:
            self.dot.opacity = 0

    def change_card_action(self, instance):
        if self.change_card_mode == 'random':
            new_card = random.choice(FULL_DECK)
            attempts = 0
            while new_card == self.current_card and attempts < 6:
                new_card = random.choice(FULL_DECK)
                attempts += 1
            self.current_card = new_card
            self.change_number_mode = 'force'
        else:
            self.current_card = MNEMONICA[self.current_number - 1]
            self.change_number_mode = 'random'
        self.change_card_mode = 'random'
        self.update_display()

    def change_number_action(self, instance):
        if self.change_number_mode == 'random':
            self.current_number = random.randint(1, 52)
            self.change_card_mode = 'force'
        else:
            try:
                self.current_number = MNEMONICA.index(self.current_card) + 1
            except ValueError:
                self.current_number = 1
            self.change_card_mode = 'random'
        self.change_number_mode = 'random'
        self.update_display()

class ACAANApp(App):
    def build(self):
        return ACAANHelper()

if __name__ == "__main__":
    ACAANApp().run()
