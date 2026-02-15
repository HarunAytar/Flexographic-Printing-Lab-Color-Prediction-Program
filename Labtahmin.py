import customtkinter as ctk
import pandas as pd
import joblib
import os
from tkinter import messagebox


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RenkTahminApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        self.title("AI Renk Tahmin Sistemi v1.1")
        self.geometry("1100x800")
        self.resizable(True, True) 

        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.join(current_dir, "egitilmis_renk_tahmin_pipeline.pkl")

        
        self.aniloks_map = {
            "1.": "12",
            "2.": "5.5",
            "3.": "6.5",
            "4.": "6.5",
            "5.": "4.5",
            "6.": "4",
            "7.": "5.5",
            "8.": "5.5",
            "9.": "4",
            "10.": "6.5",
            "11.": "5.5",
            "12.": "4",
            "13.": "4",
            "14.": "8.5",
            "15.": "8.5",
            "16.": "10",
            "17.": "5.5",
            "18.": "12",
            "19.": "10"
        }

        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=350, corner_radius=0, label_text="VERİ SETİ PARAMETRELERİ")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.widgets = {}  
        self.create_inputs()

        
        self.result_frame = ctk.CTkScrollableFrame(self, label_text="TAHMİN EKRANI")
        self.result_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.header_label = ctk.CTkLabel(self.result_frame, text="Renk Analizi Sonuçları", font=ctk.CTkFont(size=28, weight="bold"))
        self.header_label.pack(pady=(20, 40))

        
        self.results_container = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.results_container.pack(fill="x", expand=False)

        self.lbl_res_L = self.create_result_card(self.results_container, "Tahmin Edilen L")
        self.lbl_res_a = self.create_result_card(self.results_container, "Tahmin Edilen a")
        self.lbl_res_b = self.create_result_card(self.results_container, "Tahmin Edilen b")

        
        self.predict_button = ctk.CTkButton(
            self.result_frame, 
            text="HESAPLA VE TAHMİN ET", 
            command=self.predict_color, 
            height=60, 
            width=300,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.predict_button.pack(pady=40)

    def load_model(self, path):
        if not os.path.exists(path):
            
            
            return None
        try:
            return joblib.load(path)
        except Exception as e:
            messagebox.showerror("Hata", f"Model yüklenemedi: {e}")
            return None

    def create_inputs(self):
        """Tüm parametreleri veri setindeki isimlerle oluşturur."""
        
        
        self.cat_vars = {
            "filmin rengi": ["seffaf", "opak", "mat"],
            "film cinsi": ["opp", "pe"],
            "kacinci unite": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "klise bandi": ["mor", "pembe", "yesil", "sari"],
            
            "aniloks no": [f"{i}." for i in range(1, 20)], 
            "aniloks kod": ["4", "4.5", "5.5", "6.5", "8.5", "10", "12"], 
            "boya hazirlanmasi": ["temiz kova", "pantone", "kalan pan", "orijinal", "cikma"]
        }

        
        self.num_vars = [
            "film kalinligi",
            "siliv cevre",
            "makine hizi",
            "tambur sicakligi",
            "kurutma sicakligi",
            "viskozite",
            "referans density",
            "referans L",
            "referans a",
            "referans b",
            "bicak basinci"
        ]

        current_row = 0

        
        for col_name, options in self.cat_vars.items():
            lbl = ctk.CTkLabel(self.sidebar_frame, text=col_name, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=current_row, column=0, padx=20, pady=(15, 0), sticky="w")
            
            combo = ctk.CTkOptionMenu(self.sidebar_frame, values=options, width=250)
            combo.grid(row=current_row + 1, column=0, padx=20, pady=(2, 10), sticky="ew")
            
            
            if col_name == "aniloks no":
                combo.configure(command=self.on_aniloks_change)
            
            self.widgets[col_name] = combo
            current_row += 2

        
        ctk.CTkLabel(self.sidebar_frame, text="--- Sayısal Değerler ---", text_color="gray").grid(row=current_row, column=0, pady=20)
        current_row += 1

        
        for col_name in self.num_vars:
            lbl = ctk.CTkLabel(self.sidebar_frame, text=col_name, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=current_row, column=0, padx=20, pady=(10, 0), sticky="w")
            
            entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Değer giriniz...", width=250)
            entry.grid(row=current_row + 1, column=0, padx=20, pady=(2, 10), sticky="ew")
            self.widgets[col_name] = entry
            current_row += 2

        
        
        if "aniloks no" in self.widgets:
            initial_val = self.widgets["aniloks no"].get()
            self.on_aniloks_change(initial_val)

    def on_aniloks_change(self, selected_no):
        """Aniloks No değiştiğinde Aniloks Kod'u otomatik günceller."""
        if selected_no in self.aniloks_map:
            new_code = self.aniloks_map[selected_no]
            
            
            if "aniloks kod" in self.widgets:
                self.widgets["aniloks kod"].set(new_code)

    def create_result_card(self, parent, title):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=("gray85", "gray20"))
        card.pack(pady=10, padx=40, fill="x")
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14))
        lbl_title.pack(pady=(10, 5))
        
        lbl_value = ctk.CTkLabel(card, text="-", font=ctk.CTkFont(size=36, weight="bold"), text_color="#3B8ED0")
        lbl_value.pack(pady=(0, 15))
        
        return lbl_value

    def predict_color(self):
        if self.model is None:
            messagebox.showerror("Hata", "Model dosyası yüklenemediği için tahmin yapılamıyor.")
            return

        input_data = {}
        
        try:
            for col_name, widget in self.widgets.items():
                if isinstance(widget, ctk.CTkOptionMenu):
                    input_data[col_name] = widget.get()
                else:
                    val = widget.get().strip()
                    
                    input_data[col_name] = float(val) if val != "" else 0.0
            
            
            df_input = pd.DataFrame([input_data])
            
            
            prediction = self.model.predict(df_input)
            
            
            res_L, res_a, res_b = prediction[0]
            
            self.lbl_res_L.configure(text=f"{res_L:.2f}")
            self.lbl_res_a.configure(text=f"{res_a:.2f}")
            self.lbl_res_b.configure(text=f"{res_b:.2f}")

        except ValueError as e:
            messagebox.showwarning("Girdi Hatası", "Lütfen tüm sayısal alanlara geçerli rakamlar girin.")
        except Exception as e:
            messagebox.showerror("Model Hatası", f"Tahmin sırasında bir sorun oluştu:\n{e}")

if __name__ == "__main__":
    app = RenkTahminApp()
    app.mainloop()