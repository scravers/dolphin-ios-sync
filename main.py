import customtkinter
import os
import pygit2
import pyperclip
import subprocess

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dolphin iOS Sync")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.pull_button = customtkinter.CTkButton(self, text="Get Latest Saves (Pull)", command=self.button_callback)
        # self.pull_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.git_push_button = customtkinter.CTkButton(self, text="Upload Latest Save (Push)", command=self.git_push_button_callback)
        self.git_push_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.ssh_copy_key_button = customtkinter.CTkButton(self, text="Copy Public Key to Clipboard", command=self.ssh_key_copy_button_callback)
        self.ssh_copy_key_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.ssh_gen_button = customtkinter.CTkButton(self, text="Generate new SSH Keys", command=self.ssh_gen_button_callback)
        self.ssh_gen_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # self.button = customtkinter.CTkButton(self, text="Open Dialog", command=self.type_click_event)
        # self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


    def git_push_button_callback(self):
        git_push()

    def ssh_key_copy_button_callback(self):
        pyperclip.copy(get_public_key())

    def ssh_gen_button_callback(self):
        create_ssh_keys()
        print("Replaced SSH Keys")

    # def type_click_event(self):
    #     dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
    #     print("Number:", dialog.get_input())



def git_push():
    save_location = "C:/Users/james/AppData/Roaming/Dolphin Emulator/Wii"
    app_data_path = os.path.join(os.getenv('APPDATA'), 'DolphinSync')
    priv_key_path = os.path.join(app_data_path, 'Credentials', 'id_ed25519')

    ssh_cmd = f'ssh -i "{priv_key_path}" -o StrictHostKeyChecking=no'
    
    try:
        subprocess.run(["git", "add", "."], cwd=save_location, check=True)
        
        subprocess.run(["git", "commit", "-m", "Syncing saves from PC"], cwd=save_location)
        
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = ssh_cmd
        
        result = subprocess.run(
            ["git", "push", "origin", "main", "--force"], 
            cwd=save_location, 
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Push successful!")
        else:
            print(f"Push failed: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")

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


def get_public_key():
    app_data_path = os.path.join(os.getenv('APPDATA'), 'DolphinSync')
    dolphin_sync_credentials = os.path.join(app_data_path, 'Credentials')
    public_key_path = os.path.join(dolphin_sync_credentials, "id_ed25519.pub")

    with open(public_key_path, "r") as f:
        return f.read()

create_folder()

app = App()
app.mainloop()