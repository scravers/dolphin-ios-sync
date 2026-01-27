import customtkinter
import os
import pygit2

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
    


    save_location = "C:/Users/james/AppData/Roaming/Dolphin Emulator/Wii"
    repo = pygit2.Repository(save_location)
    print(repo)


def create_folder():
    # Create app data folder for saving Dolphin iOS Sync information
    app_data_path = os.path.join(os.getenv('APPDATA'), 'DolphinSync')
    if not os.path.exists(app_data_path):
        os.makedirs(app_data_path)

    dolphin_sync_backups = os.path.join(app_data_path, 'Backups')
    if not os.path.exists(dolphin_sync_backups):
        os.makedirs(dolphin_sync_backups)

    dolphin_sync_credentials = os.path.join(app_data_path, 'Credentials')
    if not os.path.exists(dolphin_sync_credentials):
        os.makedirs(dolphin_sync_credentials)
    

create_folder()

app = App()
app.mainloop()