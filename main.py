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
        self.configure(fg_color="#020617")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.side_bar_frame = customtkinter.CTkFrame(self, fg_color="#080e21", corner_radius=0, border_color="#334155", border_width=1)
        self.side_bar_frame.grid(row=0, column=0, padx=(50,0), pady=(20, 20), sticky="nsw")

        # Create dashboard
        self.dashboard_frame = customtkinter.CTkFrame(self, fg_color="#10182c", corner_radius=0, border_color="#334155", border_width=1)
        self.dashboard_frame.grid(row=0, column=1, padx=(0,50), pady=(20, 20), sticky="nswe")

        # Create settings
        self.settings_frame = customtkinter.CTkFrame(self, fg_color="#10182c", corner_radius=0, border_color="#334155", border_width=1)
        self.settings_frame.grid(row=0, column=1, padx=(0,50), pady=(20, 20), sticky="nswe")
        # Hide settings on launch
        self.settings_frame.lower()

        # Create side bar label
        self.side_bar_label = customtkinter.CTkLabel(self.side_bar_frame, text="Dolphin iOS Sync", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.side_bar_label.grid(row=0, column=0, padx=(20, 30), pady=(40, 0), sticky="w")

        # Create dashboard label
        self.side_bar_label = customtkinter.CTkLabel(self.dashboard_frame, text="Dashboard", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.side_bar_label.grid(row=0, column=0, padx=(20, 30), pady=(40, 0), sticky="w")

        # Create dashboard sub label
        self.side_bar_label = customtkinter.CTkLabel(self.dashboard_frame, text="Ready to sync Dolphin progress", font=customtkinter.CTkFont(size=14))
        self.side_bar_label.grid(row=1, column=0, padx=(20, 30), pady=(5, 0))
    
        # Create settings label
        self.side_bar_label = customtkinter.CTkLabel(self.settings_frame, text="Settings", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.side_bar_label.grid(row=0, column=0, padx=(20, 30), pady=(40, 0), sticky="w")

        # ---------- SIDEBAR BUTTONS ----------
        # Create dashboard button
        self.dashboard_button = customtkinter.CTkButton(self.side_bar_frame, text="Dashboard", height=40, width=80, corner_radius=15, command=self.open_dashboard_callback)
        self.dashboard_button.grid(row=1, column=0, padx=(20,20), pady=(20, 20), sticky="ew")
        
        # Create settings button
        self.settings_button = customtkinter.CTkButton(self.side_bar_frame, text="Settings", height=40, width=80, corner_radius=15, command=self.open_settings_callback)
        self.settings_button.grid(row=2, column=0, padx=(20,20), pady=(20, 20), sticky="ew")

        # ---------- DASHBOARD BUTTONS ----------
        # Create pull button
        self.git_pull_button = customtkinter.CTkButton(self.dashboard_frame, text="Get Latest Saves (Pull)", height=40, width=80, corner_radius=15, command=self.git_pull_button_callback)
        self.git_pull_button.grid(row=2, column=0, padx=(20,20), pady=(20, 20), sticky="w")
        
        # Create push button
        self.git_push_button = customtkinter.CTkButton(self.dashboard_frame, text="Upload Latest Save (Push)", height=40, width=80, corner_radius=15, command=self.git_push_button_callback)
        self.git_push_button.grid(row=3, column=0, padx=(20,20), pady=(20, 20), sticky="ew")

        # ---------- SETTINGS BUTTONS ----------
        # Create SSH key copy button
        self.ssh_copy_key_button = customtkinter.CTkButton(self.settings_frame, text="Copy Public Key to Clipboard", height=40, width=80, corner_radius=15, command=self.ssh_key_copy_button_callback)
        self.ssh_copy_key_button.grid(row=1, column=0, padx=(20,20), pady=(20, 20), sticky="ew")

        # Create SSH key gen button
        self.ssh_gen_button = customtkinter.CTkButton(self.settings_frame, text="Generate new SSH Keys", height=40, width=80, corner_radius=15, command=self.ssh_gen_button_callback)
        self.ssh_gen_button.grid(row=2, column=0, padx=(20,20), pady=(20, 20), sticky="ew")

        # self.button = customtkinter.CTkButton(self, text="Open Dialog", command=self.type_click_event)
        # self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def open_dashboard_callback(self):
        self.settings_frame.lower()
        self.dashboard_frame.lift()


    def open_settings_callback(self):
        self.dashboard_frame.lower()
        self.settings_frame.lift()


    def git_pull_button_callback(self):
        git_pull()

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


def git_pull():
    save_location = "C:/Users/james/AppData/Roaming/Dolphin Emulator/Wii"

    
    try:
        
        subprocess.run(["git", "fetch", "origin"], cwd=save_location)

        subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=save_location)


    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")



'''
 - Create orphan branch
 - Add save files to that branch
 - Commit
 - Delete main branch
 - Rename orphan branch to main

These steps are to ensure the size of the repository stays small, with local backups being the prefered backup option.

'''
def git_push():
    save_location = "C:/Users/james/AppData/Roaming/Dolphin Emulator/Wii"
    app_data_path = os.path.join(os.getenv('APPDATA'), 'Dolphin iOS Sync')
    priv_key_path = os.path.join(app_data_path, 'Credentials', 'id_ed25519')

    ssh_cmd = f'ssh -i "{priv_key_path}" -o StrictHostKeyChecking=no'
    
    try:
        
        subprocess.run(["git", "checkout", "--orphan", "temp_branch"], cwd=save_location)
        
        subprocess.run(["git", "add", "."], cwd=save_location, check=True)
        
        subprocess.run(["git", "commit", "-m", "Syncing saves from PC"], cwd=save_location)

        subprocess.run(["git", "branch", "-D", "main"], cwd=save_location)

        subprocess.run(["git", "branch", "-m", "main"], cwd=save_location)

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
            print(f"Push successful! {result.stderr}")
        else:
            print(f"Push failed: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")

def create_folder():
    # Create app data folder for saving Dolphin iOS Sync information
    app_data_path = os.path.join(os.getenv('APPDATA'), 'Dolphin iOS Sync')
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
    app_data_path = os.path.join(os.getenv('APPDATA'), 'Dolphin iOS Sync')
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
    app_data_path = os.path.join(os.getenv('APPDATA'), 'Dolphin iOS Sync')
    dolphin_sync_credentials = os.path.join(app_data_path, 'Credentials')
    public_key_path = os.path.join(dolphin_sync_credentials, "id_ed25519.pub")

    with open(public_key_path, "r") as f:
        return f.read()

create_folder()

app = App()
app.mainloop()