import customtkinter
import os
import pygit2
import pyperclip
import subprocess

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


class SideBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, fg_color, border_color, border_width, open_dashboard, open_settings):
        super().__init__(master)
        self.configure(fg_color=fg_color)
        self.configure(border_color=border_color)
        self.configure(border_width=border_width)

        self.open_dashboard = open_dashboard
        self.open_settings = open_settings
        
        self.configure(corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        self.grid(row=0, column=0, padx=(50,0), pady=(20, 20), sticky="nsw")

        # Create label
        self.label = customtkinter.CTkLabel(self, text="Dolphin iOS Sync", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=0, padx=(20, 30), pady=(40, 0), sticky="w")

        # Create dashboard button
        self.dashboard_button = customtkinter.CTkButton(self, text="Dashboard", height=40, width=200, corner_radius=15, command=self.open_dashboard)
        self.dashboard_button.grid(row=1, column=0, padx=(20,20), pady=(20, 20))

        # Create settings button
        self.settings_button = customtkinter.CTkButton(self, text="Settings", height=40, width=200, corner_radius=15, command=self.open_settings)
        self.settings_button.grid(row=2, column=0, padx=(20,20), pady=(20, 20))



class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, fg_color, border_color, border_width, git_pull_button, git_push_button, launch_dolphin):
        super().__init__(master)
        self.configure(fg_color=fg_color)
        self.configure(border_color=border_color)
        self.configure(border_width=border_width)

        self.git_pull_button = git_pull_button
        self.git_push_button = git_push_button
        self.launch_dolphin = launch_dolphin
        
        self.configure(corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid(row=0, column=1, padx=(0,50), pady=(20, 20), sticky="nswe")

        # Create label
        self.dashboard_label = customtkinter.CTkLabel(self, text="Dashboard", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.dashboard_label.grid(row=0, column=0, padx=(20, 30), pady=(40, 0), sticky="w")

        # Create sub label
        self.dashboard_sub_label = customtkinter.CTkLabel(self, text="Ready to sync Dolphin progress", font=customtkinter.CTkFont(size=14))
        self.dashboard_sub_label.grid(row=1, column=0, columnspan=2, padx=(0, 210), pady=(5, 0))

        # Create pull button
        self.git_pull_button = customtkinter.CTkButton(self, text="Get Latest Saves \n (Pull)", height=40, width=200, corner_radius=15, command=self.git_pull_button)
        self.git_pull_button.grid(row=3, column=0, padx=(20,20), pady=(20, 20), sticky="ew")
        
        # Create push button
        self.git_push_button = customtkinter.CTkButton(self, text="Upload Latest Save \n (Push)", height=40, width=200, corner_radius=15, command=self.git_push_button)
        self.git_push_button.grid(row=3, column=1, padx=(20,20), pady=(20, 20), sticky="ew")

        # Create launch dolphin button
        self.git_push_button = customtkinter.CTkButton(self, text="Launch Dolphin Emulator", height=40, width=200, corner_radius=15, command=self.launch_dolphin)
        self.git_push_button.grid(row=4, column=0, columnspan=2, padx=(20,20), pady=(20, 20), sticky="ew")


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, fg_color, border_color, border_width, ssh_key_copy_button, ssh_gen_button):
        super().__init__(master)
        self.configure(fg_color=fg_color)
        self.configure(border_color=border_color)
        self.configure(border_width=border_width)

        self.ssh_key_copy_button = ssh_key_copy_button
        self.ssh_gen_button = ssh_gen_button
        
        self.configure(corner_radius=0)

        self.grid(row=0, column=1, padx=(0,50), pady=(20, 20), sticky="nswe")

        # Hide settings on launch
        self.lower()

        # Create label
        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=(20, 30), pady=(40, 0), sticky="w")

        # Create SSH key copy button
        self.ssh_copy_key_button = customtkinter.CTkButton(self, text="Copy Public Key to Clipboard", height=40, width=200, corner_radius=15, command=self.ssh_key_copy_button)
        self.ssh_copy_key_button.grid(row=1, column=0, padx=(20,20), pady=(20, 20), sticky="ew")

        # Create SSH key gen button
        self.ssh_gen_button = customtkinter.CTkButton(self, text="Generate new SSH Keys", height=40, width=200, corner_radius=15, command=self.ssh_gen_button)
        self.ssh_gen_button.grid(row=2, column=0, padx=(20,20), pady=(20, 20), sticky="ew")

        # Creaste dolphin location entry
        self.dolphin_entry = customtkinter.CTkEntry(self, placeholder_text="Dolphin Location")
        self.dolphin_entry.grid(row=3, column=0, padx=(20,20), pady=(20, 20), sticky="ew")
        self.dolphin_emulator_path = self.dolphin_entry.get()




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dolphin iOS Sync")
        self.geometry("800x600")
        self.configure(fg_color="#020617")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)



        # Create sidebar frame
        self.side_bar_frame = SideBarFrame(self, fg_color="#080e21", border_color="#334155", border_width=1, 
                                           open_dashboard=self.open_dashboard_callback, open_settings=self.open_settings_callback
                                           )

        # Create dashboard frame
        self.dashboard_frame = DashboardFrame(self, fg_color="#10182c", border_color="#334155", border_width=1, 
                                              git_pull_button=self.git_pull_button_callback, 
                                              git_push_button=self.git_push_button_callback, 
                                              launch_dolphin=self.launch_dolphin_callback
                                              )

        # Create settings frame
        self.settings_frame = SettingsFrame(self, fg_color="#10182c", border_color="#334155", border_width=1,
                                            ssh_key_copy_button=self.ssh_key_copy_button_callback,
                                            ssh_gen_button=self.ssh_gen_button_callback,
                                            )
        

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

    dolphin_sync_settings = os.path.join(app_data_path, 'Settings')
    if not os.path.exists(dolphin_sync_settings):
        os.makedirs(dolphin_sync_settings)
    

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