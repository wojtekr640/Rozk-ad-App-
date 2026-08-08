from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window

# Czysto białe tło imitujące kartkę papieru
Window.clearcolor = (1, 1, 1, 1)

class RozkladJazdyApp(App):
    def build(self):
        root_scroll = ScrollView()
        self.main_box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8), size_hint_y=None)
        self.main_box.bind(minimum_height=self.main_box.setter('height'))

        # --- PANEL STEROWANIA LICZBĄ PRZYSTANKÓW ---
        control_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        lbl_count = Label(text="Liczba przystanków:", color=(0, 0, 0, 1), font_size=dp(12), size_hint_x=None, width=dp(130), halign="left")
        lbl_count.bind(size=lbl_count.setter('text_size'))
        
        btn_minus = Button(text="-", font_size=dp(18), bold=True, size_hint_x=None, width=dp(45))
        btn_minus.bind(on_press=self.odejmij_przystanek)

        self.input_liczba = TextInput(text="30", multiline=False, font_size=dp(14), halign="center")
        self.input_liczba.bind(on_text_validate=self.zmien_liczbe_przystankow)
        
        btn_plus = Button(text="+", font_size=dp(18), bold=True, size_hint_x=None, width=dp(45))
        btn_plus.bind(on_press=self.dodaj_przystanek)

        control_box.add_widget(lbl_count)
        control_box.add_widget(btn_minus)
        control_box.add_widget(self.input_liczba)
        control_box.add_widget(btn_plus)
        self.main_box.add_widget(control_box)

        # --- NAGŁÓWEK ---
        header_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(5))
        
        self.linia_input = TextInput(
            hint_text="Linia", 
            text="",
            halign="center",
            font_size=dp(22),
            size_hint_x=None, width=dp(70),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1)
        )
        
        info_col = BoxLayout(orientation='vertical', spacing=dp(2))
        self.txt_data = TextInput(hint_text="Rozkład jazdy ważny od: ...", text="", multiline=False, font_size=dp(11), background_color=(0.98,0.98,0.98,1), foreground_color=(0,0,0,1))
        self.txt_przystanek = TextInput(hint_text="Przystanek: ...", text="", multiline=False, font_size=dp(11), background_color=(0.98,0.98,0.98,1), foreground_color=(0,0,0,1))
        self.txt_kierunek = TextInput(hint_text="Kierunek: ...", text="", multiline=False, font_size=dp(11), background_color=(0.98,0.98,0.98,1), foreground_color=(0,0,0,1))
        
        info_col.add_widget(self.txt_data)
        info_col.add_widget(self.txt_przystanek)
        info_col.add_widget(self.txt_kierunek)
        
        header_box.add_widget(self.linia_input)
        header_box.add_widget(info_col)
        self.main_box.add_widget(header_box)

        # --- SEKCJE DNI ---
        dni = [
            ("OD PONIEDZIAŁKU DO PIĄTKU (BEZ ŚWIĄT)", ""),
            ("SOBOTA (BEZ ŚWIĄT)", ""),
            ("NIEDZIELA (BEZ ŚWIĄT)", "")
        ]
        
        for tytul, domyslne_godziny in dni:
            box_dzien = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(45))
            lbl = Label(text=tytul, bold=True, color=(0, 0, 0, 1), font_size=dp(11), halign="left", size_hint_y=None, height=dp(20))
            lbl.bind(size=lbl.setter('text_size'))
            
            txt = TextInput(text=domyslne_godziny, hint_text="Wpisz godziny...", multiline=False, font_size=dp(11), background_color=(0.98, 0.98, 0.98, 1), foreground_color=(0, 0, 0, 1), size_hint_y=None, height=dp(25))
            
            box_dzien.add_widget(lbl)
            box_dzien.add_widget(txt)
            self.main_box.add_widget(box_dzien)

        # --- SEKCJA TRASY ---
        trasa_title = Label(
            text="TRASA: nazwa przystanku", 
            bold=True, color=(0, 0, 0, 1), font_size=dp(12), 
            size_hint_y=None, height=dp(25), halign="left"
        )
        trasa_title.bind(size=trasa_title.setter('text_size'))
        self.main_box.add_widget(trasa_title)

        # Kontener na dynamiczną trasę
        self.trasa_container = BoxLayout(orientation='horizontal', size_hint_y=None)
        self.przebuduj_trase(30)
        self.main_box.add_widget(self.trasa_container)

        # --- STOPKA ---
        stopka_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70), spacing=dp(2))
        lbl_stopka_tytul = Label(text="KOMUNIKACJA AUTOBUSOWA", bold=True, color=(0, 0, 0, 1), font_size=dp(10), halign="left", size_hint_y=None, height=dp(15))
        lbl_stopka_tytul.bind(size=lbl_stopka_tytul.setter('text_size'))
        
        self.input_org = TextInput(text="", hint_text="Organizator: ...", multiline=False, font_size=dp(10), background_color=(0.98,0.98,0.98,1), foreground_color=(0,0,0,1), size_hint_y=None, height=dp(25))
        self.input_op = TextInput(text="", hint_text="Operator: ...", multiline=False, font_size=dp(10), background_color=(0.98,0.98,0.98,1), foreground_color=(0,0,0,1), size_hint_y=None, height=dp(25))
        
        stopka_box.add_widget(lbl_stopka_tytul)
        stopka_box.add_widget(self.input_org)
        stopka_box.add_widget(self.input_op)
        self.main_box.add_widget(stopka_box)

        root_scroll.add_widget(self.main_box)
        return root_scroll

    def przebuduj_trase(self, liczba):
        self.trasa_container.clear_widgets()
        
        try:
            liczba = int(liczba)
        except ValueError:
            liczba = 10
            
        if liczba < 1: 
            liczba = 1
        if liczba > 80: 
            liczba = 80

        self.input_liczba.text = str(liczba)

        liczba_kolumn = 3 if liczba >= 3 else liczba
        
        # Równomierne rozdzielenie przystanków na kolumny pionowe
        elementow_na_kolumne = (liczba + liczba_kolumn - 1) // liczba_kolumn
        
        wysokosc_wiersza = dp(26)
        self.trasa_container.height = elementow_na_kolumne * wysokosc_wiersza + dp(10)

        # Generowanie kolumn z uwzględnieniem kolejności pionowej
        for k in range(liczba_kolumn):
            col = BoxLayout(orientation='vertical', spacing=dp(1))
            
            for r in range(elementow_na_kolumne):
                # Obliczanie indeksu przystanku dla układu pionowego
                i = k * elementow_na_kolumne + r
                
                if i < liczba:
                    row = BoxLayout(orientation='horizontal', size_hint_y=None, height=wysokosc_wiersza, spacing=dp(2))
                    
                    symbol = "■" if (i == 0 or i == liczba - 1) else "●"
                    
                    lbl_symbol = Label(text=symbol, color=(0, 0, 0, 1), size_hint_x=None, width=dp(18), font_size=dp(10))
                    
                    input_przystanek = TextInput(
                        text="", 
                        hint_text=f"Przystanek {i+1}",
                        multiline=False,
                        font_size=dp(10),
                        background_color=(0.98, 0.98, 0.98, 1),
                        foreground_color=(0, 0, 0, 1)
                    )
                    
                    row.add_widget(lbl_symbol)
                    row.add_widget(input_przystanek)
                    col.add_widget(row)
                else:
                    # Puste miejsce w kolumnie, aby zachować równy układ
                    empty_row = BoxLayout(size_hint_y=None, height=wysokosc_wiersza)
                    col.add_widget(empty_row)
                    
            self.trasa_container.add_widget(col)

    def zmien_liczbe_przystankow(self, instance):
        try:
            val = int(self.input_liczba.text)
            self.przebuduj_trase(val)
        except ValueError:
            pass

    def dodaj_przystanek(self, instance):
        try:
            val = int(self.input_liczba.text)
            if val < 80:
                self.przebuduj_trase(val + 1)
        except ValueError:
            self.przebuduj_trase(1)

    def odejmij_przystanek(self, instance):
        try:
            val = int(self.input_liczba.text)
            if val > 1:
                self.przebuduj_trase(val - 1)
        except ValueError:
            self.przebuduj_trase(1)

if __name__ == '__main__':
    RozkladJazdyApp().run()
