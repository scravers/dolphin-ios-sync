import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dolphin iOS Sync")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(self, text="Get Latest Saves (Pull)", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("Button Pressed")


def setup():
    print("Test")

setup()

app = App()
app.mainloop()