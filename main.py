import customtkinter
import os
import pygit2

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

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
    

def create_ssh_keys():
    # Generate and serialize the private key
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Generate and serialize the public key
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    # Add to "./Dolphin iOS Sync/Credentials"
    app_data_path = os.path.join(os.getenv('APPDATA'), 'DolphinSync')
    dolphin_sync_credentials = os.path.join(app_data_path, 'Credentials')
    private_key_path = os.path.join(dolphin_sync_credentials, "id_ed25519")
    public_key_path = os.path.join(dolphin_sync_credentials, "id_ed25519.pub")

    with open(private_key_path, "wb") as f:
        f.write(private_bytes)
    # Ensure only the user can read and write
    os.chmod(private_key_path, 0o600)

    with open(public_key_path, "wb") as f:
        f.write(public_bytes)

create_folder()

create_ssh_keys()

app = App()
app.mainloop()