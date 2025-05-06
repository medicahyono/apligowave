import paramiko
import json

# Fungsi untuk merestart AP menggunakan SSH
def restart_ap(ip, nama, username, password):
    try:
        # Membuat koneksi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, password)

        # Mengirim perintah reboot ke AP Ligowave
        stdin, stdout, stderr = ssh.exec_command('reboot')

        # Menunggu hingga perintah selesai dieksekusi
        stdout.channel.recv_exit_status()

        print(f"Access Point {ip} ({nama}) berhasil di-restart!")
    except Exception as e:
        print(f"Terjadi kesalahan saat merestart AP {ip} ({nama}): {e}")
    finally:
        # Menutup koneksi SSH
        ssh.close()

# Fungsi untuk membaca daftar AP dari file JSON
def load_ap_list(file_path):
    try:
        with open(file_path, 'r') as file:
            ap_list = json.load(file)
        return ap_list
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file JSON: {e}")
        return []

# Main function
if __name__ == "__main__":
    # Path ke file JSON yang berisi daftar AP
    json_file = 'dbAP_nftligowave.json'

    # Memuat daftar AP dari file JSON
    ap_list = load_ap_list(json_file)

    # Merestart setiap AP dalam daftar
    for ap in ap_list:
        ip = ap.get('ip')
        nama=ap.get('nama')
        username = ap.get('username', 'admin')  # Default username 'admin'
        password = ap.get('password')

        if ip and password:
            restart_ap(ip, nama, username, password)
        else:
            print(f"Informasi tidak lengkap untuk AP {ap} ({nama})")
