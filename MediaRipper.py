import os
import sys
import time
from colorama import init, Fore, Style
import yt_dlp

# Renkleri Başlat
init(autoreset=True)

# Klasör Ayarı
DOWNLOAD_FOLDER = "MediaRipper_Downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- YARDIMCI FONKSIYONLAR ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def title(text):
    os.system(f'title MediaRipper v1.0 | {text}')

def banner():
    clear()
    print(Fore.MAGENTA + Style.BRIGHT + r"""
    ╔══════════════════════════════════════════════════════════╗
    ║  ███╗   ███╗███████╗██████╗ ██╗ █████╗ ██████╗           ║
    ║  ████╗ ████║██╔════╝██╔══██╗██║██╔══██╗██╔══██╗          ║
    ║  ██╔████╔██║█████╗  ██║  ██║██║███████║██████╔╝          ║
    ║  ██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║██╔══██╗          ║
    ║  ██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║██║  ██║ v1.0     ║
    ║  ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝          ║
    ║        ULTIMATE MULTI-PLATFORM DOWNLOADER                ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    print(Fore.CYAN + "    Supported: YouTube, Instagram, TikTok, X, Twitch\n")

# İlerleme Çubuğu (Hook)
def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        print(Fore.YELLOW + f"\r    [download] İndiriliyor: {p}% | Hız: {d.get('_speed_str', 'N/A')}", end='')
    elif d['status'] == 'finished':
        print(Fore.GREEN + "\n    [success] İndirme tamamlandı! İşleniyor...")

# --- İNDİRME MOTORU ---
def download_content(url, mode):
    # Mode 1: Video (Max Quality)
    # Mode 2: Audio (MP3)
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
    }

    if mode == '1': # VIDEO
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        print(Fore.CYAN + " [*] En iyi video kalitesi ve ses birleştiriliyor...")
    
    elif mode == '2': # AUDIO
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        print(Fore.CYAN + " [*] MP3 Dönüştürücü ayarlandi (FFmpeg)...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video Bilgisi Al
            print(Fore.WHITE + " [Analyzing] Link taranıyor...")
            info = ydl.extract_info(url, download=False)
            
            title_vid = info.get('title', 'Bilinmeyen Dosya')
            print(Fore.WHITE + f"\n [Target]: {title_vid}")
            print(Fore.WHITE + f" [Source]: {info.get('extractor_key', 'Unknown')}")
            
            # İndirmeyi Başlat
            ydl.download([url])
            
        print(Fore.GREEN + Style.BRIGHT + f"\n [OK] İşlem Başarılı! Dosya '{DOWNLOAD_FOLDER}' klasöründe.")
        
    except Exception as e:
        print(Fore.RED + f"\n [ERROR] Hata oluştu: {e}")
        print(Fore.YELLOW + " Not: MP3 hatası aldıysanız FFmpeg yüklü değildir.")

    print()
    input(Fore.WHITE + " Ana menü için Enter...")

# --- ANA MENÜ ---
def main():
    while True:
        banner()
        print(Fore.WHITE + "  [1] 🎬 Video İndir (Max Kalite / 4K)")
        print(Fore.WHITE + "  [2] 🎵 Müzik İndir (MP3 Dönüştür)")
        print(Fore.WHITE + "  [3] 📋 Playlist İndir (YouTube)")
        print(Fore.WHITE + "  [4] ❌ Çıkış")
        print(Fore.CYAN + "\n ==========================================================")
        
        choice = input(Fore.GREEN + "  Seçiminiz (1-4): ")
        
        if choice in ['1', '2']:
            url = input(Fore.YELLOW + "  Link'i Yapıştır (URL): ")
            if url.strip(): 
                download_content(url, choice)
            
        elif choice == '3':
            url = input(Fore.YELLOW + "  Playlist Linki: ")
            print(Fore.RED + "  [!] Uyarı: Tüm listeyi indirmek zaman alabilir.")
            c = input("  Onaylıyor musun? (e/h): ")
            if c.lower() == 'e': download_content(url, '1')
            
        elif choice == '4':
            sys.exit()

if __name__ == "__main__":
    main()
