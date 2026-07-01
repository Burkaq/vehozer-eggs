#!/usr/bin/env python3
"""
Pterodactyl Egg JSON Turkcelestirme Script'i
Sadece guvenli alanlari (name, description, variables[].name, variables[].description) cevirir.
Teknik alanlara (startup, config, scripts, env_variable, rules, docker_images) DOKUNMAZ.
"""

import json
import os
import re
import shutil
from pathlib import Path

# ============================================================================
# CEVIRI SOZLUGU - Degisken Isimleri
# ============================================================================

VAR_NAME_TR = {
    # Universal
    "Max Players": "Maksimum Oyuncu Sayisi",
    "Max players": "Maksimum Oyuncu Sayisi",
    "Maximum Players": "Maksimum Oyuncu Sayisi",
    "Server Name": "Sunucu Adi",
    "Server name": "Sunucu Adi",
    "Server Hostname": "Sunucu Ana Bilgisayar Adi",
    "Server Password": "Sunucu Sifresi",
    "Server password": "Sunucu Sifresi",
    "Admin Password": "Yonetici Sifresi",
    "Admin password": "Yonetici Sifresi",
    "Auto Update": "Otomatik Guncelleme",
    "Auto-update server": "Sunucu Otomatik Guncelleme",
    "Automatic Updates": "Otomatik Guncellemeler",
    "Server Auto Update": "Sunucu Otomatik Guncelleme",
    "Map": "Harita",
    "Default Map": "Varsayilan Harita",
    "Server Map": "Sunucu Haritasi",
    "Version": "Surum",
    "Game Mode": "Oyun Modu",
    "Gamemode": "Oyun Modu",
    "Gametype": "Oyun Tipi",
    "Difficulty": "Zorluk",
    "Server Description": "Sunucu Aciklamasi",
    "Project Name": "Proje Adi",
    "Project Description": "Proje Aciklamasi",
    "World Name": "Dunya Adi",
    "World Size": "Dunya Boyutu",
    "Save Name": "Kayit Adi",
    "Server Port": "Sunucu Portu",
    "Query Port": "Sorgu Portu",
    "QueryPort": "Sorgu Portu",
    "RCON Port": "RCON Portu",
    "RCON Password": "RCON Sifresi",
    "Enable RCON": "RCON'u Etkinlestir",
    "Source AppID": "Kaynak AppID",
    "App ID": "Uygulama ID",
    "Game ID": "Oyun ID",
    "Steam Game Login Token": "Steam Oyun Giris Anahtari",
    "Steam Gameserver Login Token": "Steam Oyun Sunucusu Giris Anahtari",
    "Steam Account Token": "Steam Hesap Anahtari",
    "Steam Username": "Steam Kullanici Adi",
    "Steam Password": "Steam Sifresi",
    "Steam Auth Code": "Steam Dogrulama Kodu",
    "Enable VAC": "VAC'i Etkinlestir",
    "SourceTV Port": "SourceTV Portu",
    "HTTP Port": "HTTP Portu",
    "Public IP": "Genel IP",
    "Connection Platform": "Baglanti Platformu",
    "Connection Platfrom": "Baglanti Platformu",  # typo in original
    "Windows Install": "Windows Kurulumu",
    "WINDOWS_INSTALL": "Windows Kurulumu",
    "SERVER_JARFILE": "Sunucu Jar Dosyasi",
    "Server Jar File": "Sunucu Jar Dosyasi",

    # Minecraft
    "Minecraft Version": "Minecraft Surumu",
    "Server Version": "Sunucu Surumu",
    "Build Number": "Derleme Numarasi",
    "Download Path": "Indirme Yolu",
    "Build Type": "Derleme Turu",
    "Forge Version": "Forge Surumu",
    "Modpack Version": "Mod Paketi Surumu",
    "Java Version": "Java Surumu",
    "Server Memory": "Sunucu Hafizasi",
    "View Distance": "Gorus Mesafesi",
    "Whitelist": "Beyaz Liste",
    "Hardcore": "Zor Mod",
    "PVP": "PVP",
    "Level Seed": "Harita Tohumu",
    "Level Name": "Harita Adi",
    "Level Type": "Harita Tipi",
    "Server IP": "Sunucu IP'si",
    "Server Port (IPv4)": "Sunucu Portu (IPv4)",
    "Server Port (IPv6)": "Sunucu Portu (IPv6)",
    "Enable Command Blocks": "Komut Bloklarini Etkinlestir",
    "Force Gamemode": "Oyun Modunu Zorla",
    "Online Mode": "Cevrimici Mod",
    "Spawn Protection": "Dogma Korumasi",
    "Max World Size": "Maksimum Dunya Boyutu",
    "Allow Nether": "Nether'a Izin Ver",
    "Allow Flight": "Ucusa Izin Ver",
    "Enable Query": "Sorguyu Etkinlestir",
    "Enable JMX": "JMX'i Etkinlestir",
    "Spawn Monsters": "Canavar Dogmasini Etkinlestir",
    "Spawn Animals": "Hayvan Dogmasini Etkinlestir",
    "Spawn NPCs": "NPC Dogmasini Etkinlestir",
    "Generate Structures": "Yapi Olusumunu Etkinlestir",
    "Resource Pack": "Kaynak Paketi",
    "Resource Pack SHA1": "Kaynak Paketi SHA1",
    "Enable EULA": "EULA'yi Kabul Et",
    "Autoconfigure": "Otomatik Yapilandir",
    "Server Locale": "Sunucu Dili",
    "MOTD": "MOTD",
    "Max Build Height": "Maksimum Insa Yuksekligi",
    "Operator Username": "Operator Kullanici Adi",
    "Enable Console": "Konsolu Etkinlestir",
    "Enable RCON (MC)": "RCON'u Etkinlestir (MC)",
    "Network Compression Threshold": "Ag Sikistirma Esigi",
    "Max Tick Time": "Maksimum Tick Suresi",
    "Use Native Transport": "Yerel Transport Kullan",
    "Entity Activation Range": "Varlik Etkinlestirme Araligi",
    "Chunk Garbage Collection": "Chunk Cop Toplama",
    "Snooper Enabled": "Snooper Etkin",

    # FiveM / RedM
    "CFX License Key": "CFX Lisans Anahtari",
    "Steam Web Api Key": "Steam Web Api Anahtari",
    "FXServer Version": "FXServer Surumu",
    "QBCore Auto Install": "QBCore Otomatik Kurulum",
    "MySQL Connection String": "MySQL Baglanti Dizesi",
    "QBCore Locale": "QBCore Dili",
    "Git Enabled": "Git Etkin",
    "Git Username": "Git Kullanici Adi",
    "Git Token": "Git Anahtari",
    "Git Repository URL": "Git Depo URL'si",
    "Git Branch": "Git Dal",
    "Enable txAdmin": "txAdmin'i Etkinlestir",
    "txAdmin Port": "txAdmin Portu",
    "FiveM Game Build": "FiveM Oyun Derlemesi",
    "Onesync": "Onesync",
    "Use3dAudio": "3D Ses Kullan",
    "UseSendingRangeOnly": "Yalnizca Gonderim Araligi Kullan",
    "UseNativeAudio": "Yerel Ses Kullan",
    "txAdmin Data Path": "txAdmin Veri Yolu",
    "txAdmin Game Name": "txAdmin Oyun Adi",

    # Steam / Source
    "Tickrate": "Tickrate",
    "Lua Refresh": "Lua Yenileme",
    "Workshop ID": "Atolye ID",
    "Pingboost": "Pingboost",
    "Startmap": "Baslangic Haritasi",
    "Game Name": "Oyun Adi",
    "Auth Mode": "Kimlik Dogrulama Modu",
    "Patchline": "Yama Hatti",
    "Accept Early Plugins": "Erken Eklentileri Kabul Et",
    "Allow operators": "Operatorlere Izin Ver",

    # Arma 3
    "Server Binary": "Sunucu Binary'si",
    "Extra Startup Parameters": "Ekstra Baslangic Parametreleri",
    "Modlist File": "Mod Listesi Dosyasi",
    "Mods": "Modlar",
    "Additional Mods": "Ek Modlar",
    "Server Mods": "Sunucu Modlari",
    "Headless Clients (HC)": "Headless Client (HC)",
    "Auto Init": "Otomatik Baslatma",
    "Verify Signatures": "Imzalari Dogrula",
    "Disable VoN": "VoN'u Devre Disi Birak",
    "BattlEye": "BattlEye",
    "Enable BattlEye": "BattlEye'i Etkinlestir",
    "Persistent Battlefield": "Kalici Savas Alani",
    "File Patching": "Dosya Yamalama",

    # Don't Starve Together
    "Cluster Name": "Kume Adi",
    "Cluster Description": "Kume Aciklamasi",
    "Server Token": "Sunucu Anahtari",
    "Master Worldgen Override": "Ana Dunya Olusumu Gecersiz Kilma",
    "Caves Worldgen Override": "Magara Dunya Olusumu Gecersiz Kilma",

    # Terraria
    "Terraria Version": "Terraria Surumu",
    "tModloader Version": "tModloader Surumu",
    "Tshock Version": "Tshock Surumu",
    "Download Version": "Indirme Surumu",

    # DayZ
    "Disable Third Person": "Ucuncu Sahis Kamerayi Devre Disi Birak",
    "Disable Crosshair": "Nisangahi Devre Disi Birak",
    "Enable Whitelist": "Beyaz Listeyi Etkinlestir",
    "Steam Query Port": "Steam Sorgu Portu",
    "Save Interval": "Kaydetme Araligi",

    # Sons of the Forest
    "Save Slot": "Kayit Yuvasi",
    "Skip network Test": "Ag Testini Atla",
    "BlobSyncPort": "BlobSyncPort",
    "Show Logo": "Logo Goster",
    "Tree Regrowth": "Agac Yeniden Buyumesi",
    "Vail World": "Vail World",
    "Copy Default Folder": "Varsayilan Klasoru Kopyala",

    # The Forest
    "Init Type": "Baslatma Tipi",
    "Auto Save Interval": "Otomatik Kaydetme Araligi",
    "Disable Auto Save": "Otomatik Kaydetmeyi Devre Disi Birak",
    "Save File Path": "Kayit Dosya Yolu",
    "Steam Auto Update": "Steam Otomatik Guncelleme",
    "Steam Beta Branch": "Steam Beta Dali",
    "Enable VAC (Forest)": "VAC'i Etkinlestir",
    "Enable BattlEye (Forest)": "BattlEye'i Etkinlestir",
    "Server IP Address": "Sunucu IP Adresi",
    "Server Game Port": "Sunucu Oyun Portu",
    "Server Query Port": "Sunucu Sorgu Portu",
    "Server Steam Port": "Sunucu Steam Portu",

    # Subnautica Nitrox
    "Serializer Mode": "Serilestirme Modu",
    "Auto Portforward via UPnP": "UPnP ile Otomatik Port Yonlendirme",
    "Admin Username": "Yonetici Kullanici Adi",

    # Assetto Corsa
    "Http Port": "Http Portu",
    "UDP Port": "UDP Portu",
    "Tcp Port": "Tcp Portu",
    "Plugin Port": "Eklenti Portu",
    "Max Clients": "Maksimum Istemci Sayisi",
    "Number of SteamCMD Retry Attempts": "SteamCMD Yeniden Deneme Sayisi",
    "Force Install": "Zorunlu Kurulum",

    # Palworld
    "Server Player Count": "Sunucu Oyuncu Sayisi",
    "RCON Enabled": "RCON Etkin",
    "Server Description Text": "Sunucu Aciklama Metni",

    # Among Us
    "Github branch": "GitHub Dali",
    "Domain": "Alan Adi",
    "Use HTTPS": "HTTPS Kullan",
    "Path to SSL": "SSL Yolu",
    "Port": "Port",

    # Ark
    "Battle Eye": "Battle Eye",
    "Additional Arguments": "Ek Argumanlar",

    # Arma 3 (without bracket prefixes - those are handled)
    "Steam Username": "Steam Kullanici Adi",
    "Steam Password": "Steam Sifresi",
    "Disable Mod Downloads/Updates": "Mod Indirme/Guncellemeleri Devre Disi Birak",
    "Download Creator DLCs": "Yapimci DLC'lerini Indir",
    "Modlist File (Exported from A3 Launcher)": "Mod Listesi Dosyasi (A3 Launcher'dan Disa Aktarilmis)",
    "Make Mod Files Lowercase": "Mod Dosyalarini Kucuk Harf Yap",
    "Validate Server Files": "Sunucu Dosyalarini Dogrula",
    "Server-Side Only Mods": "Yalnizca Sunucu Tarafi Modlar",
    "Optional Client-Side Mods": "Istege Bagli Istemci Tarafi Modlar",
    "Extra Flags for SteamCMD": "SteamCMD icin Ek Bayraklar",
    "Headless Clients (HC)": "Headless Client (HC)",
    "HC Hide Console Output": "HC Konsol Ciktilisini Gizle",
    "Clear HC Profiles Cache on Startup": "Baslangicta HC Profil Onbellegini Temizle",
    "Arma 3 Dedicated Server App ID": "Arma 3 Adanmis Sunucu Uygulama ID",
    "basic.cfg URL": "basic.cfg URL",
    "Modlist File (Exported from DayZ Launcher)": "Mod Listesi Dosyasi (DayZ Launcher'dan Disa Aktarilmis)",

    # Arma Reforger
    "Server Region": "Sunucu Bolgesi",
    "Scenario ID": "Senaryo ID",
    "Auto Joinable": "Otomatik Katilabilir",
    "Visible in Server Browser": "Sunucu Tarayicisinda Gorunur",
    "Max FPS": "Maksimum FPS",
    "Log FPS Interval": "FPS Log Araligi",
    "Arma Reforger Dedicated Server App ID": "Arma Reforger Adanmis Sunucu Uygulama ID",

    # BeamNG
    "Authentication Key": "Kimlik Dogrulama Anahtari",
    "Private": "Gizli",
    "Chat logging": "Sohbet Kaydi",

    # Counter-Strike 1.6
    "Max Players (Slots)": "Maksimum Oyuncu Sayisi (Slot)",
    "Steam Auth": "Steam Dogrulama",
    "Validate": "Dogrula",

    # Counter-Strike Source
    "Steam Guard Code": "Steam Guard Kodu",

    # DayZ (without bracket prefixes)
    "Skip Game Server Install": "Oyun Sunucusu Kurulumunu Atla",
    "Enforce Game Version": "Oyun Surumunu Zorla",
    "VoN Quality": "VoN Kalitesi",
    "Disable Personal Light": "Kisisel Isigi Devre Disi Birak",
    "Darker Nights": "Daha Karanlik Geceler",
    "Persistent Time": "Kalici Zaman",
    "Time Multiplier": "Zaman Carpani",
    "Night Multiplier": "Gece Carpani",
    "DayZ Dedicated Server App ID": "DayZ Adanmis Sunucu Uygulama ID",

    # DDNet
    "Steam AppID": "Steam AppID",
    "Steam User": "Steam Kullanicisi",
    "Public Server": "Genel Sunucu",

    # Hytale
    "Disable Sentry": "Sentry'yi Devre Disi Birak",
    "Use Ahead-of-Time Cache": "Onceden Derlenmis Onbellek Kullan",
    "Install Source Query plugin": "Source Query Eklentisini Yukle",
    "Source Query Port": "Source Query Portu",

    # Minecraft Bedrock
    "Wine Debug": "Wine Debug",
    "Winetricks": "Winetricks",
    "Bedrock Dedicated Server Version": "Bedrock Adanmis Sunucu Surumu",
    "Liteloader Version": "Liteloader Surumu",
    "Wine": "Wine",
    "Version to install": "Yuklenecek Surum",
    "AutoReboot mode": "Otomatik Yeniden Baslatma Modu",
    "Bedrock Version": "Bedrock Surumu",
    "ld lib path": "ld lib yolu",
    "Allow cheats": "Hilelere Izin Ver",
    "Nukkit Version": "Nukkit Surumu",

    # Minecraft Java
    "Arclight Channel": "Arclight Kanali",
    "Arclight Loader": "Arclight Yukleyici",
    "Canvas MC Version": "Canvas MC Surumu",
    "CanvasMC Build Number": "CanvasMC Derleme Numarasi",
    "WebAdmin Port": "WebAdmin Portu",
    "Modpack Project ID": "Mod Paketi Proje ID",
    "Modpack File ID": "Mod Paketi Dosya ID",
    "CurseForge API Key": "CurseForge API Anahtari",
    "Fabric Version": "Fabric Surumu",
    "Fabric Loader Version": "Fabric Yukleyici Surumu",
    "FTB Pack search term": "FTB Paket Arama Terimi",
    "FTB modpack ID": "FTB Mod Paketi ID",
    "FTB Pack Version": "FTB Paket Surumu",
    "FTB Pack Version ID": "FTB Paket Surum ID",
    "Glowstone Version": "Glowstone Surumu",
    "GitHub User": "GitHub Kullanici Adi",
    "GitHub OAuth Token": "GitHub OAuth Anahtari",
    "GitHub Package": "GitHub Paketi",
    "Match": "Eslesme",
    "Krypton Version": "Krypton Surumu",
    "Tag Version": "Etiket Surumu",
    "Modpack Version ID": "Mod Paketi Surum ID",
    "Project": "Proje",
    "Download URL": "Indirme URL",
    "NeoForge Version": "NeoForge Surumu",
    "Spigot Version": "Spigot Surumu",
    "Spongeforge Minecraft Version": "SpongeForge Minecraft Surumu",
    "SpongeVanilla Version": "SpongeVanilla Surumu",

    # Minecraft Proxy
    "Waterdog PE Version": "Waterdog PE Surumu",
    "Travertine Jar File": "Travertine Jar Dosyasi",
    "Download Link": "Indirme Baglantisi",
    "Travertine build number": "Travertine Derleme Numarasi",
    "Velocity Version": "Velocity Surumu",
    "VIAaaS JAR File": "VIAaaS JAR Dosyasi",
    "Web Server Port": "Web Sunucu Portu",
    "Waterfall Jar File": "Waterfall Jar Dosyasi",
    "Waterfall build number": "Waterfall Derleme Numarasi",

    # Project Zomboid
    "SteamPort": "SteamPort",
    "PZ Steam App ID": "PZ Steam App ID",
    "Steam Beta Branch [requires reinstall]": "Steam Beta Dali [yeniden kurulum gerekir]",

    # Sons of the Forest
    "Password": "Sifre",
    "SRCDS_APPID": "SRCDS_APPID",
    "WINEDEBUG": "WINEDEBUG",
    "WINEARCH": "WINEARCH",
    "WINEPATH": "WINEPATH",
    "WINETRICKS_RUN": "WINETRICKS_RUN",

    # Starbound
    "Auto Update Server": "Sunucu Otomatik Guncelleme",
    "Use Workshop content": "Atolye Icerigini Kullan",

    # Subnautica
    "Steam-Username": "Steam Kullanici Adi",
    "Steam-Password": "Steam Sifresi",
    "Steam-GuardCode": "Steam Guard Kodu",
    "Nitrox Version": "Nitrox Surumu",
    "Subnautica Installation Path": "Subnautica Kurulum Yolu",
    "XDG Config Home": "XDG Yapilandirma Dizini",

    # Team Fortress 2 Classic
    "Game Version": "Oyun Surumu",
    "Steam Beta ID": "Steam Beta ID",

    # Terraria
    "World Seed": "Dunya Tohumu",
    "NPCStream": "NPCStream",
    "Language": "Dil",

    # The Forest
    "Auto-Update": "Otomatik Guncelleme",
    "Save Interval": "Kaydetme Araligi",

    # Palworld
    "Server Name (Palworld)": "Sunucu Adi",
    "Server Password (Palworld)": "Sunucu Sifresi",
    "Admin Password (Palworld)": "Yonetici Sifresi",

    # Sons of the Forest / The Forest shared
    "IP Address": "IP Adresi",
    "Game Port": "Oyun Portu",
    "Steam Port": "Steam Portu",

    # BeamNG
    "BeamMP Server Version": "BeamMP Sunucu Surumu",
    "Max Cars": "Maksimum Arac Sayisi",
    "Max AI": "Maksimum Yapay Zeka",

    # CS 1.6 ReHLDS
    "ReHLDS Version": "ReHLDS Surumu",
    "Available Modules": "Kullanilabilir Moduller",
    "VAC port": "VAC Portu",
    "Secure or Insecure": "Guvenli veya Guvensiz",

    # Ark
    "ARK Server Name": "ARK Sunucu Adi",
    "ARK Server Password": "ARK Sunucu Sifresi",
    "ARK Admin Password": "ARK Yonetici Sifresi",
    "Session Name": "Oturum Adi",

    # DayZ
    "Config": "Yapilandirma",

    # gmod
    "Gamemode (gmod)": "Oyun Modu",
    "Map (gmod)": "Harita",
    "Workshop Collection ID": "Atolye Koleksiyon ID",

    # ARMA Reforger
    "Scenario": "Senaryo",
    "Max Players (Reforger)": "Maksimum Oyuncu Sayisi",
    "Disable Third Person (Reforger)": "Ucuncu Sahis Kamerayi Devre Disi Birak",
    "Enable BattlEye (Reforger)": "BattlEye'i Etkinlestir",

    # Project Zomboid
    "Server Player Limit": "Sunucu Oyuncu Limiti",
    "Server Public Name": "Sunucu Genel Adi",
    "Server Public Description": "Sunucu Genel Aciklamasi",
    "Beta branch": "Beta Dal",
    "Beta password": "Beta Sifresi",

    # DDNet
    "Server Name (DDNet)": "Sunucu Adi",
    "RCON Password (DDNet)": "RCON Sifresi",
    "Map (DDNet)": "Harita",

    # Left4Dead 2
    "Server Name (L4D2)": "Sunucu Adi",
    "Map (L4D2)": "Harita",
    "Max Players (L4D2)": "Maksimum Oyuncu Sayisi",
    "GameMode (L4D2)": "Oyun Modu",
    "Steam Group ID": "Steam Grup ID",

    # Team Fortress 2 Classic
    "Server Name (TF2C)": "Sunucu Adi",
    "Map (TF2C)": "Harita",
    "Max Players (TF2C)": "Maksimum Oyuncu Sayisi",

    # Starbound
    "Server Name (Starbound)": "Sunucu Adi",
    "Max Players (Starbound)": "Maksimum Oyuncu Sayisi",

    # Hytale
    "Server Name (Hytale)": "Sunucu Adi",
    "Max Players (Hytale)": "Maksimum Oyuncu Sayisi",

    # Palworld
    "Server Name (Palworld)": "Sunucu Adi",
    "Server Password (Palworld)": "Sunucu Sifresi",
    "Admin Password (Palworld)": "Yonetici Sifresi",
}

# ============================================================================
# CEVIRI SOZLUGU - Aciklama Parcalari (regex patterns)
# ============================================================================

# Full top-level description translations (exact match)
TOP_DESC_TR = {
    # Among Us
    "An egg designed to allow support for Proximity Chat in Among Us using BetterCrewLink Server":
        "Among Us icin BetterCrewLink Server kullanarak Yakinlik Sohbeti destegi saglamak uzere tasarlanmis bir egg.",

    "Impostor is one of the first Among Us private servers, written in C#.\n\nThere are no special features at this moment, the goal is aiming to be as close as possible to the real server, for now. In a later stage, making modifications to game logic by modifying GameData packets can be looked at.":
        "Impostor, C# ile yazilmis ilk Among Us ozel sunucularindan biridir.\n\nSu anda ozel bir ozellik bulunmamaktadir, amac gercek sunucuya mumkun oldugunca yakin olmaktir. Daha sonraki bir asamada, GameData paketlerini degistirerek oyun mantiginda degisiklik yapilabilir.",

    # Ark
    "As a man or woman stranded, naked, freezing, and starving on the unforgiving shores of a mysterious island called ARK, use your skill and cunning to kill or tame and ride the plethora of leviathan dinosaurs and other primeval creatures roaming the land. Hunt, harvest resources, craft items, grow crops, research technologies, and build shelters to withstand the elements and store valuables, all while teaming up with (or preying upon) hundreds of other players to survive, dominate... and escape! � Gamepedia: ARK":
        "ARK adli gizemli bir adanin aci kiyilarinda ciplak, donmus ve ac bir sekilde mahsur kalmis biri olarak, bolgede dolasan dev dinozorlari ve diger tarih oncesi yaratiklari oldurmek, evcillestirmek ve surmek icin beceri ve kurnazliginizi kullanin. Avlanin, kaynak toplayin, esyalar uretin, ekin yetistirin, teknolojiler arastirin ve elementlere dayanacak barinaklar insa edin; tum bunlari yaparken hayatta kalmak, hukmetmek ve kacmak icin diger yuzlerce oyuncuyla isbirligi yapin (ya da onlari avlayin)!",

    # Arma
    "Experience true combat gameplay in a massive military sandbox. Deploying a wide variety of single and multiplayer content, over 20 vehicles and 40 weapons, and limitless opportunities for content creation, this is the PC's premier military game. Authentic, diverse, open - Arma 3 sends you to war.":
        "Dev bir askeri sandbox'ta gercek carpisma oynanisini deneyimleyin. Cok cesitli tek ve cok oyunculu icerik, 20'den fazla arac ve 40 silah, ve sinirsiz icerik olusturma imkani ile PC'nin onde gelen askeri oyunu. Otantik, cesitli, acik - Arma 3 sizi savasa gonderiyor.",

    "Experience authentic Cold War combat and join friends in the struggle for a sprawling, 51 km� mid-Atlantic island � or take on the role of Game Master and create your very own scenarios for others to enjoy.":
        "Otantik Soguk Savas carpismasini deneyimleyin ve 51 km�'lik engin bir orta Atlantik adasindaki mucadelede arkadaslariniza katilin - veya Oyun Yoneticisi rolunu ustlenin ve baskalarinin keyif almasi icin kendi senaryolarinizi olusturun.",

    # Assetto Corsa
    "Custom Assetto Corsa server with focus on freeroam":
        "Serbest dolasima odakli ozel Assetto Corsa sunucusu.",

    "Assetto Corsa (Italian for \"Race Setup\") is a sim racing video game developed by the Italian video game developer Kunos Simulazioni. It is designed with an emphasis on a realistic racing experience with support for extensive customization and moddability":
        "Assetto Corsa (Italyanca \"Yaris Ayari\"), Italyan video oyun gelistiricisi Kunos Simulazioni tarafindan gelistirilen bir sim yarisi video oyunudur. Gercekci bir yaris deneyimi vurgusuyla tasarlanmis olup kapsamli ozellestirme ve modlanabilirlik destegi sunar.",

    # BeamNG
    "This is the server for the multiplayer mod BeamMP for the game BeamNG.drive. The server is the point through which all clients communicate. You can write lua mods for the server, detailed instructions on the BeamMP Wiki.":
        "Bu, BeamNG.drive oyunu icin BeamMP cok oyunculu modunun sunucusudur. Sunucu, tum istemcilerin iletisim kurdugu noktadir. Sunucu icin lua modlari yazabilirsiniz, detayli talimatlar BeamMP Wiki'de bulunmaktadir.",

    "Server for the KISS Multiplayer BeamNG.drive mod":
        "KISS Multiplayer BeamNG.drive modu icin sunucu.",

    # Counter-Strike
    "Counter Strike 1.6 - Vanilla\n\nCounter-Strike: 1.6 is a multiplayer first-person shooter video game developed by Valve Corporation.":
        "Counter Strike 1.6 - Vanilla\n\nCounter-Strike: 1.6, Valve Corporation tarafindan gelistirilen cok oyunculu bir birinci sahis nisanci video oyunudur.",

    "CS 1.6 ReHLDS binaries egg.\n\nReHLDS is a reverse-engineered, optimized version of HLDS.\nDeveloped by third-party modders to improve stability, performance, and security.\nFully compatible with MetaMod, AMX Mod X, and other plugins.\n\nIncluded modules are rehlds, reunion, amxmodx, metamod-r, reapi and ReGameDLL_CS":
        "CS 1.6 ReHLDS binary egg'i.\n\nReHLDS, HLDS'nin tersine muhendislikle gelistirilmis, optimize edilmis surumudur.\nUcuncu taraf mod gelistiricileri tarafindan kararlilik, performans ve guvenligi artirmak icin gelistirilmistir.\nMetaMod, AMX Mod X ve diger eklentilerle tam uyumludur.\n\nDahil edilen moduller: rehlds, reunion, amxmodx, metamod-r, reapi ve ReGameDLL_CS",

    "For over two decades, Counter-Strike has offered an elite competitive experience, one shaped by millions of players from across the globe. And now the next chapter in the CS story is about to begin. This is Counter-Strike 2.":
        "Yirmi yili askin suredir Counter-Strike, dunyanin dort bir yanindan milyonlarca oyuncu tarafindan sekillendirilen elit bir rekabetci deneyim sunmustur. Ve simdi CS hikayesinin bir sonraki bolumu baslamak uzere. Bu Counter-Strike 2.",

    "Counter-Strike: Source blends Counter-Strike's award-winning teamplay action with the advanced technology of Source� technology.":
        "Counter-Strike: Source, Counter-Strike'in odullu takim oyunu aksiyonunu Source� teknolojisinin gelismis teknolojisiyle birlestiriyor.",

    # DayZ
    "How long can you survive a post-apocalyptic world? A land overrun with an infected \"zombie\" population, where you compete with other survivors for limited resources. Will you team up with strangers and stay strong together? Or play as a lone wolf to avoid betrayal? This is DayZ � this is your story.":
        "Bir post-apokaliptik dunyada ne kadar hayatta kalabilirsiniz? Enfekte \"zombi\" nufusu tarafindan istila edilmis topraklarda, sinirli kaynaklar icin diger hayatta kalanlarla rekabet edin. Yabancilarla takim olup birlikte guclu mu kalacaksiniz? Yoksa ihanetten kacinmak icin yalniz bir kurt olarak mi oynayacaksiniz? Bu DayZ - bu sizin hikayeniz.",

    # DDNet
    "Want to play the hardest cooperative 2D platformer ever? Want to finish no map ever? Want to be in pain for hours and cry, getting nothing in return? Come play DDNet with a large community of other sufferers!":
        "Gelmiss gecmiss en zor cooperative 2D platform oyununu oynamak ister misiniz? Hicbir haritayi asla bitirmek istemez misiniz? Saatlerce aci cekip aglamak ve karsiliginda hicbir sey almamak ister misiniz? Gelin, diger aci cekenlerden olusan buyuk bir toplulukla DDNet oynayin!",

    # Don't Starve Together
    "Don�t Starve Together is an uncompromising wilderness survival game full of science and magic.":
        "Don't Starve Together, bilim ve buyu dolu tavizsiz bir vahsi dogada hayatta kalma oyunudur.",

    # FiveM (already Turkish, leave as-is but normalize)
    "FiveM sunucu egg'i � QBCore framework otomatik kurulumu, artifact guncelleme, Git ve txAdmin destegi.":
        "FiveM sunucu egg'i - QBCore framework otomatik kurulumu, artifact guncelleme, Git ve txAdmin destegi.",

    # Garry's Mod
    "Garrys Mod, is a sandbox physics game created by Garry Newman, and developed by his company, Facepunch Studios.":
        "Garry's Mod, Garry Newman tarafindan olusturulan ve Facepunch Studios tarafindan gelistirilen bir sandbox fizik oyunudur.",

    # Hytale
    "Set out on an adventure built for both creation and play. Hytale blends the freedom of a sandbox with the momentum of an RPG: explore a procedurally generated world full of dungeons, secrets, and a variety of creatures, then shape it block by block.":
        "Hem yaratma hem de oynama icin insa edilmis bir maceraya atilin. Hytale, sandbox ozgurlugunu RPG'nin momentumuyla birlestiriyor: zindanlar, sirlar ve cesitli yaratiklarla dolu prosedurel olarak uretilmis bir dunyayi kesfedin, sonra blok blok sekillendirin.",

    # Left 4 Dead 2
    "Left 4 Dead 2 is set in the aftermath of a worldwide pandemic of a disease nicknamed the \"Green Flu\", which rapidly transforms humans into zombie-like creatures and mutated forms that demonstrate extreme aggression towards non-infected beings. A few humans are immune to the disease, while some of those who are infected have no symptoms. The Civil Emergency and Defense Agency (CEDA) and the U.S. military create safe zones to attempt to evacuate as many survivors as possible.":
        "Left 4 Dead 2, \"Yesil Grip\" olarak adlandirilan ve insanlari hizla enfekte olmayan varliklara karsi asiri saldirganlik gosteren zombi benzeri yaratiklara ve mutasyona ugramis formlara donusturen bir hastaligin neden oldugu dunya capinda bir salginin sonrasinda gecer. Bazi insanlar hastaliga bagisik iken, enfekte olanlarin bazilari semptom gostermez. Sivil Acil Durum ve Savunma Ajansi (CEDA) ve ABD ordusu, mumkun oldugunca cok sayida kurtulani tahliye etmeye calismak icin guvenli bolgeler olusturur.",

    # Minecraft Bedrock
    "LeviLamina is an unofficial mod loader designed to offer indispensable API support for Minecraft Bedrock Edition. It boasts a comprehensive API, an array of utility interfaces, a robust event system, and comprehensive support for basic interfaces. LeviLamina provides an expansive API, a powerful event system, and a wealth of encapsulated development infrastructure interfaces, forming a solid foundation for augmenting the Minecraft Bedrock Edition with additional gameplay features and functionalities. By leveraging mods, the process of extending Bedrock functionality becomes effortless, with a user-friendly development process and an adaptable approach.":
        "LeviLamina, Minecraft Bedrock Edition icin vazgecilmez API destegi sunmak uzere tasarlanmis resmi olmayan bir mod yukleyicisidir. Kapsamli bir API, cesitli arac arayuzleri, saglam bir olay sistemi ve temel arayuzler icin kapsamli destek sunar. LeviLamina; genis bir API, guclu bir olay sistemi ve kapsullenmis gelistirme altyapi arayuzleri sunarak Minecraft Bedrock Edition'a ek oynanis ozellikleri ve islevleri eklemek icin saglam bir temel olusturur. Modlardan yararlanarak Bedrock islevselligini genisletme sureci, kullanici dostu bir gelistirme sureci ve uyarlanabilir bir yaklasimla zahmetsiz hale gelir.",

    "LiteLoaderBDS - Epoch-making & Cross-language Bedrock Dedicated Servers Plugin Loader\n\nLiteLoaderBDS is an unofficial plugin loader that provides basic API support for Bedrock Dedicated Server, with a massive API, lots of packed utility interfaces, a rich event system and powerful basic interface support.":
        "LiteLoaderBDS - Cagir Acan & Diller Arasi Bedrock Adanmis Sunucu Eklenti Yukleyicisi\n\nLiteLoaderBDS, Bedrock Adanmis Sunucu icin temel API destegi saglayan resmi olmayan bir eklenti yukleyicisidir; genis bir API, cok sayida kullanisli arayuz, zengin bir olay sistemi ve guclu temel arayuz destegi sunar.",

    "PowerNukkitX support for Pterodactyl":
        "Pterodactyl icin PowerNukkitX destegi.",

    "Bedrock Edition (also known as the Bedrock Version, Bedrock Codebase, Bedrock Engine or just Bedrock) refers to the multi-platform family of editions of Minecraft developed by Mojang AB, Microsoft Studios, 4J Studios, and SkyBox Labs. Prior to this term, as the engine originated with Pocket Edition, this entire product family was referred to as \"Pocket Edition\", \"MCPE\", or \"Pocket/Windows 10 Edition\".":
        "Bedrock Edition (Bedrock Surumu, Bedrock Kod Tabani, Bedrock Motoru veya kisaca Bedrock olarak da bilinir), Mojang AB, Microsoft Studios, 4J Studios ve SkyBox Labs tarafindan gelistirilen Minecraft surumlerinin cok platformlu ailesini ifade eder. Bu terimden once, motor Pocket Edition'dan geldigi icin tum urun ailesi \"Pocket Edition\", \"MCPE\" veya \"Pocket/Windows 10 Edition\" olarak aniliyordu.",

    "A performant and stable Minecraft server software for the Bedrock Edition that comes with a modern API and support for Java 11 LTS.":
        "Modern bir API ve Java 11 LTS destegi ile gelen, Bedrock Edition icin performansli ve kararli bir Minecraft sunucu yazilimi.",

    "Nukkit is a nuclear-powered server software for Minecraft Bedrock Edition\n\nhttps://cloudburstmc.org":
        "Nukkit, Minecraft Bedrock Edition icin nukleer guclu bir sunucu yazilimidir.\n\nhttps://cloudburstmc.org",

    "Pocketmine Egg\nby onekintaro from swisscrafting.ch\nwith the nice help from #eggs Channel on Pterodactyl-Discord :)":
        "Pocketmine Egg\nonekintaro tarafindan swisscrafting.ch'den\nPterodactyl-Discord'daki #eggs kanalinin guzel yardimiyla :)",

    # Minecraft Crossplay
    "A drop-in replacement for Paper servers designed for configurability, and new fun and exciting gameplay features, with the addition of GeyserMC and Floodgate":
        "Yapilandirilabilirlik ve yeni eglenceli oynanis ozellikleri icin tasarlanmis, GeyserMC ve Floodgate eklenmis Paper sunucularina dogrudan alternatif.",

    # Minecraft Java - Arclight
    "A Bukkit server implementation on common mod loaders.":
        "Yaygin mod yukleyicileri uzerinde bir Bukkit sunucu uygulamasi.",

    # CanvasMC
    "Supercharge your Minecraft server with multithreaded dimension ticking, improved chunk generation, optimized entity handling and many more powerful optimizations.":
        "Cok is parcacikli boyut isleme, iyilestirilmis chunk olusumu, optimize edilmis varlik yonetimi ve daha bircok guclu optimizasyon ile Minecraft sunucunuzu guclendirin.",

    # Cuberite
    "A lightweight, fast and extensible game server for Minecraft":
        "Minecraft icin hafif, hizli ve genisletilebilir bir oyun sunucusu.",

    # CurseForge
    "A generic egg for a CurseForge modpack.":
        "CurseForge mod paketi icin genel bir egg.",

    # Fabric
    "Fabric is a modular modding toolchain targeting Minecraft 1.14 and above, including snapshots.":
        "Fabric, Minecraft 1.14 ve uzeri surumleri (anlik goruntuler dahil) hedefleyen moduler bir modlama arac zinciridir.",

    # Folia
    "Fork of Paper which adds regionised multithreading to the dedicated server.":
        "Adanmis sunucuya bolgesel cok is parcacikli calisma ekleyen Paper catallanmasi.",

    # Forge
    "Minecraft Forge Server. Minecraft Forge is a modding API (Application Programming Interface), which makes it easier to create mods, and also make sure mods are compatible with each other.":
        "Minecraft Forge Sunucusu. Minecraft Forge, mod olusturmayi kolaylastiran ve modlarin birbiriyle uyumlu olmasini saglayan bir modlama API'sidir (Uygulama Programlama Arayuzu).",

    # FTB
    "FTB modpacks are now distributed through their own API. This egg was developed for support for modpacks that are distributed through this.":
        "FTB mod paketleri artik kendi API'leri uzerinden dagitilmaktadir. Bu egg, bu API uzerinden dagitilan mod paketleri icin destek saglamak uzere gelistirilmistir.",

    # Glowstone
    "Glowstone is an open-source server implementation for Minecraft: Java Edition 1.12.2 and up.":
        "Glowstone, Minecraft: Java Edition 1.12.2 ve uzeri icin acik kaynakli bir sunucu uygulamasidir.",

    # Krypton
    "A fast, lightweight Minecraft server written in Kotlin":
        "Kotlin ile yazilmis hizli, hafif bir Minecraft sunucusu.",

    # Limbo
    "Standalone server program Limbo.":
        "Bagimsiz sunucu programi Limbo.",

    # Magma
    "Magma is most powerful Forge server providing you with Forge mods and Bukkit Plugins using Spigot and Paper for Performance Optimization and Stability. Using: https://github.com/magmamaintained":
        "Magma, Performans Optimizasyonu ve Kararlilik icin Spigot ve Paper kullanarak Forge modlari ve Bukkit Eklentileri sunan en guclu Forge sunucusudur. Kullanilan: https://github.com/magmamaintained",

    # Modrinth
    "A generic egg for a Modrinth modpack.":
        "Modrinth mod paketi icin genel bir egg.",

    # MohistMC
    "Spigot fork with performance optimizations.":
        "Performans optimizasyonlarina sahip Spigot catallanmasi.",

    # NanoLimbo
    "This is lightweight minecraft limbo server, written on Java with Netty. The main goal of the project is maximum simplicity with a minimum number of sent and processed packets. This limbo is empty, there are no ability to set schematic building since this is not necessary. You can send useful information in chat or BossBar.\n\nNo plugins, no logs. The server is fully clear. It only able keep a lot of players while the main server is down.":
        "Bu, Java ile Netty kullanilarak yazilmis hafif bir Minecraft limbo sunucusudur. Projenin ana hedefi, minimum sayida gonderilen ve islenen paket ile maksimum basitliktir. Bu limbo bostur, sematik bina ayarlama imkani yoktur cunku bu gerekli degildir. Sohbette veya BossBar'da faydali bilgiler gonderebilirsiniz.\n\nEklenti yok, log yok. Sunucu tamamen temiz. Sadece ana sunucu kapaliyken cok sayida oyuncuyu tutabilir.",

    # NeoForge
    "NeoForge Server. NeoForge is a modding API (Application Programming Interface), which makes it easier to create mods, and also make sure mods are compatible with each other. NeoForge is a fork of Minecraft Forge.":
        "NeoForge Sunucusu. NeoForge, mod olusturmayi kolaylastiran ve modlarin birbiriyle uyumlu olmasini saglayan bir modlama API'sidir (Uygulama Programlama Arayuzu). NeoForge, Minecraft Forge'un bir catallanmasidir.",

    # Paper
    "High performance Spigot fork that aims to fix gameplay and mechanics inconsistencies.":
        "Oynanis ve mekanik tutarsizliklarini duzeltmeyi amaclayan yuksek performansli Spigot catallanmasi.",

    # Purpur
    "A drop-in replacement for Paper servers designed for configurability, and new fun and exciting gameplay features.":
        "Yapilandirilabilirlik ve yeni eglenceli oynanis ozellikleri icin tasarlanmis Paper sunucularina dogrudan alternatif.",

    # Quilt
    "The Quilt project is an open-source, community-driven modding toolchain designed primarily for Minecraft. By focusing on speed, ease of use and modularity, Quilt aims to provide a sleek and modern modding toolchain with an open ecosystem.":
        "Quilt projesi, oncelikle Minecraft icin tasarlanmis acik kaynakli, topluluk odakli bir modlama arac zinciridir. Hiz, kullanim kolayligi ve modulerlige odaklanarak Quilt, acik bir ekosisteme sahip modern ve sik bir modlama arac zinciri sunmayi amaclar.",

    # Spigot
    "Spigot is the most widely-used modded Minecraft server software in the world. It powers many of the top Minecraft server networks around to ensure they can cope with their huge player base and ensure the satisfaction of their players. Spigot works by reducing and eliminating many causes of lag, as well as adding in handy features and settings that help make your job of server administration easier.":
        "Spigot, dunyadaki en yaygin kullanilan modlanmis Minecraft sunucu yazilimidir. Bircok onde gelen Minecraft sunucu agina guc vererek buyuk oyuncu kitleleriyle basa cikabilmelerini ve oyuncularinin memnuniyetini saglamalarini garanti eder. Spigot, bircok lag nedenini azaltarak ve ortadan kaldirarak, sunucu yoneticiligi isinizi kolaylastiran kullanisli ozellikler ve ayarlar ekleyerek calisir.",

    # SpongeForge
    "A community-driven open source Minecraft: Java Edition modding platform.":
        "Topluluk odakli acik kaynakli bir Minecraft: Java Edition modlama platformu.",

    # SpongeVanilla
    "SpongeVanilla is the implementation of the Sponge API on top of Vanilla Minecraft.":
        "SpongeVanilla, Sponge API'sinin Vanilla Minecraft uzerindeki uygulamasidir.",

    # Tekkit 2
    "Those of you who are nostalgic for the early days of Tekkit (now known as Tekkit Classic), will love what awaits you in Tekkit 2!\n\nWith a collection of nostalgic mods and plenty of new improvements, Tekkit 2 is sure to capture the feeling of possibility and consequence that you felt while exploring the world of machines and contraptions that made the original fun. Keep an eye out for classics such as IndustrialCraft, ProjectE (Equivalent Exchange), Project Red (RedPower) and BuildCraft, alongside additions such as Galacticraft and Tekkit Jaffa Cakes! The world is yours to bend and exploit to your will, whether through alchemy or sprawling factories and mines.\n\nWhat fresh horrors will you create?":
        "Tekkit'in ilk gunlerini ozleyenler (simdi Tekkit Classic olarak biliniyor), Tekkit 2'de sizi bekleyenlere bayilacak!\n\nNostaljik modlar koleksiyonu ve bircok yeni iyilestirme ile Tekkit 2, orijinali eglenceli kilan makineler ve duzenekler dunyasini kesfederken hissettiginiz olasilik ve sonuc duygusunu yakalayacak. IndustrialCraft, ProjectE (Equivalent Exchange), Project Red (RedPower) ve BuildCraft gibi klasiklerin yani sira Galacticraft ve Tekkit Jaffa Cakes gibi eklemelere de goz atin! Dunya, ister simya ister genisleyen fabrikalar ve madenler araciligiyla olsun, iradenize gore bukmek ve somurmek icin sizin.\n\nNe taze dehsetler yaratacaksiniz?",

    # Tekkit
    "Tekkit is set to reignite the same sort of wonder and awe that we all received from booting up Minecraft for the first time. With the skies open, the moon ready to be colonized (by force if need be) and dimensional mysteries to be plied, with tesseracts to be networked, �meat� to be processed, items to be digitized, and power suits to be manufactured, there is virtually limitless engineering projects to be assembled.":
        "Tekkit, hepimizin Minecraft'i ilk kez baslatirken aldigimiz ayni turden merak ve hayranligi yeniden atesleyecek. Gokyuzu acik, ay kolonilestirilmeye hazir (gerekirse zorla), boyutsal gizemler kesfedilmeyi bekliyor, tesseract'ler aga baglanacak, 'et' islenecek, esyalar dijitallestirilecek ve guc kiyafetleri uretilecek; birlestirilecek neredeyse sinirsiz muhendislik projesi var.",

    # Attack of the B-Team
    "This modpack was designed with one thing in mind, crazy mad science! With the help of the B-Team we hand picked the wackiest mods we could find and shoved them all in a modpack for you guys. The result is Attack of the B-Team!":
        "Bu mod paketi tek bir sey dusunulerek tasarlandi: cilgin cinnet bilim! B-Team'in yardimiyla bulabildigimiz en sacma modlari sectik ve hepsini sizin icin bir mod paketine tikistirdik. Sonuc: Attack of the B-Team!",

    # Blightfall
    "Blightfall is a combination modpack and adventure map about surviving on an alien planet. It uses magic mods and tech mods to create a novel gameplay experience. Can you survive on a world completely covered by Thaumcraft taint?\n\nhttps://www.technicpack.net/modpack/blightfall.592618":
        "Blightfall, yabanci bir gezegende hayatta kalma hakkinda bir mod paketi ve macera haritasi birlesimidir. Yeni bir oynanis deneyimi yaratmak icin buyu modlarini ve teknoloji modlarini kullanir. Tamamen Thaumcraft bozulmasiyla kapli bir dunyada hayatta kalabilir misiniz?\n\nhttps://www.technicpack.net/modpack/blightfall.592618",

    # Hexxit
    "Gear up and set forth on a campaign worthy of legend, for Hexxit has been unearthed! Dark dungeons, towering spires, weathered ruins and musty tomes lay before you. Lay claim to riches or create your own artifacts, tame beasts and carve out your own story in endless wonder. Alone or with friends, adventure awaits in Hexxit.\n\nHexxit is a new collection of mods for Minecraft that put adventure above all else, in the style of old Dungeons and Dragons campaigns. Exploration is interesting, the dangers are greater and the sense of satisfaction of clearing out a dungeon is intense. The modlist is full of quality content from some very talented individuals. Be sure to head over to the donate page and show your appreciation!\n\nhttps://www.technicpack.net/modpack/hexxit.552552":
        "Efsaneye layik bir sefer icin kusaminizi hazirlayin ve yola cikin, cunku Hexxit ortaya cikarildi! Karanlik zindanlar, yukselen kuleler, yipranmis harabeler ve kuflu kitaplar onunuzde uzanir. Zenginliklere el koyun veya kendi esyalarinizi yaratin, canavarlari evcillestirin ve sonsuz merak icinde kendi hikayenizi olusturun. Ister tek basiniza ister arkadaslarinizla, Hexxit'te macera bekliyor.\n\nHexxit, eski Dungeons and Dragons seferleri tarzinda, macerayi her seyin ustunde tutan yeni bir Minecraft mod koleksiyonudur. Kesif ilginc, tehlikeler daha buyuk ve bir zindani temizlemenin tatmin duygusu yogundur. Mod listesi, cok yetenekli bireylerin kaliteli icerikleriyle doludur. Bagis sayfasina ugrayip takdirinizi gostermeyi unutmayin!\n\nhttps://www.technicpack.net/modpack/hexxit.552552",

    # Tekkit Classic
    "Created by the Technic team, Tekkit Classic is a modpack for the record breaking sandbox construction game Minecraft. \nIt brings together some of the best mods from the Minecraft community for automating, industrializing and powering your worlds and bundles them into one easy download!":
        "Technic ekibi tarafindan olusturulan Tekkit Classic, rekor kiran sandbox insa oyunu Minecraft icin bir mod paketidir.\nMinecraft toplulugundan otomatiklestirme, endustrilesme ve dunyalariniza guc saglama icin en iyi modlardan bazilarini bir araya getirir ve tek bir kolay indirmede paketler!",

    # Tekkit Legends
    "The ancient power of Tekkits past return in this legendary pack! Wield the philosopher's stone, ride the rails, breed the bees, and much, much more! This pack will remind you of what you've always loved about Tekkit, while bringing you new mods to discover and enjoy!\n\nhttps://www.technicpack.net/modpack/tekkit-legends.735902":
        "Tekkit'in gecmisinin kadim gucu bu efsanevi pakette geri donuyor! Felsefe tasini kullanin, raylarda surun, arilari yetistirin ve cok daha fazlasi! Bu paket size Tekkit hakkinda her zaman sevdiginiz seyleri hatirlatirken, kesfedecek ve keyfini cikaracak yeni modlar sunar!\n\nhttps://www.technicpack.net/modpack/tekkit-legends.735902",

    # Tekkit SMP
    "Tekkit SMP contains the full range of mods from Tekkit 2, plus the extra mods that were originally dropped in the transition from Technic SSP (to Technic SMP) to Tekkit, in favour of multiplayer and Bukkit support: mainly Thaumcraft, Mystcraft, and Mo' Creatures. The new Tekkit SMP expands on that with various carefully selected Thaumcraft and Mystcraft addons, alongside Mo' Creatures Extended, and smaller custom additions such as Re-Crystallized Wing. Electro-Magic Tools is another starring mod, being an addon to both Industrial Craft and Thaumcraft, combining the worlds of tech and magic.":
        "Tekkit SMP, Tekkit 2'deki tum modlari ve ayrica Technic SSP'den (Technic SMP'ye) Tekkit'e geciste cok oyunculu ve Bukkit destegi lehine cikarilan ekstra modlari icerir: baslica Thaumcraft, Mystcraft ve Mo' Creatures. Yeni Tekkit SMP, cesitli dikkatlice secilmis Thaumcraft ve Mystcraft eklentileri, Mo' Creatures Extended ve Re-Crystallized Wing gibi daha kucuk ozel eklemelerle bunu genisletir. Electro-Magic Tools, hem Industrial Craft hem de Thaumcraft'a eklenti olan ve teknoloji ile buyu dunyalarini birlestiren bir baska onde gelen moddur.",

    # The 1.12.2 Pack
    "The 1.12.2 Pack":
        "The 1.12.2 Pack",

    # The 1.7.10 Pack
    "The 1.7.10 Pack":
        "The 1.7.10 Pack",

    # VanillaCord
    "Minecraft is a game about placing blocks and going on adventures. Explore randomly generated worlds and build amazing things from the simplest of homes to the grandest of castles. Play in Creative Mode with unlimited resources or mine deep in Survival Mode, crafting weapons and armor to fend off dangerous mobs. Do all this alone or with friends.\n\nVanillaCord adds support for BungeeCord's ip_forward setting.":
        "Minecraft, blok yerlestirme ve maceralara atilma hakkindaki bir oyundur. Rastgele olusturulmus dunyalari kesfedin ve en basit evlerden en buyuk kalelere kadar harika seyler insa edin. Yaratilim Modu'nda sinirsiz kaynaklarla oynayin veya Hayatta Kalma Modu'nda derin madenler kazarak tehlikeli yaratiklara karsi silah ve zirh uretin. Tum bunlari tek basiniza veya arkadaslarinizla yapin.\n\nVanillaCord, BungeeCord'un ip_forward ayarina destek ekler.",

    # Minecraft Proxy - Waterdog
    "Brand new proxy server for Minecraft: Bedrock Edition":
        "Minecraft: Bedrock Edition icin yepyeni proxy sunucusu.",

    # Travertine
    "Travertine is a fork of Waterfall with 1.7 protocol support. Waterfall is a fork of the well-known BungeeCord server teleportation suite.":
        "Travertine, 1.7 protokol destegine sahip bir Waterfall catallanmasidir. Waterfall, iyi bilinen BungeeCord sunucu isinlanma suite'inin bir catallanmasidir.",

    # Velocity
    "Velocity is a Minecraft server proxy with unparalleled server support, scalability, and flexibility.":
        "Velocity, benzersiz sunucu destegi, olceklendirilebilirlik ve esneklik sunan bir Minecraft sunucu proxy'sidir.",

    # VIAaaS
    "VIAaaS - ViaVersion as a Service - Standalone ViaVersion proxy":
        "VIAaaS - ViaVersion as a Service - Bagimsiz ViaVersion proxy",

    # Waterfall
    "Waterfall is a fork of the well-known BungeeCord server teleportation suite.":
        "Waterfall, iyi bilinen BungeeCord sunucu isinlanma suite'inin bir catallanmasidir.",

    # Palworld
    "Fight, farm, build and work alongside mysterious creatures called \"Pals\" in this completely new multiplayer, open world survival and crafting game!":
        "\"Pal\" adi verilen gizemli yaratiklarla birlikte savasin, ciftcilik yapin, insa edin ve calisin; bu tamamen yeni cok oyunculu, acik dunya hayatta kalma ve uretim oyununda!",

    # Project Zomboid
    "Project Zomboid is an open world survival horror video game in alpha stage development by British and Canadian independent developer, The Indie Stone. The game is set in a post apocalyptic, zombie infested world where the player is challenged to survive for as long as possible before inevitably dying.":
        "Project Zomboid, Ingiliz ve Kanadali bagimsiz gelistirici The Indie Stone tarafindan alfa asamasinda gelistirilen bir acik dunya hayatta kalma korku video oyunudur. Oyun, oyuncunun kacinilmaz olumden once mumkun oldugunca uzun sure hayatta kalmaya calistigi post-apokaliptik, zombi istilasina ugramis bir dunyada gecer.",

    # Sons of the Forest
    "Sons of the Forest is a horror survival game and sequel to The Forest by Endnight Games, Ltd.. Sent to find a missing billionaire on a remote island, you find yourself in a cannibal-infested hellscape. Craft, build, and struggle to survive, alone or with friends.":
        "Sons of the Forest, Endnight Games, Ltd. tarafindan The Forest'in devami olan bir korku hayatta kalma oyunudur. Uzak bir adada kayip bir milyarderi bulmak icin gonderilmisken kendinizi yamyam istilasina ugramis bir cehennemde bulursunuz. Tek basiniza veya arkadaslarinizla uretin, insa edin ve hayatta kalmak icin mucadele edin.",

    # Starbound
    "Starbound takes place in a two-dimensional, procedurally generated universe which the player is able to explore in order to obtain new weapons, armor, and items, and to visit towns and villages inhabited by various intelligent lifeforms.":
        "Starbound, oyuncunun yeni silahlar, zirhlar ve esyalar elde etmek ve cesitli zeki yasam formlarinin yasadigi kasaba ve koyleri ziyaret etmek icin kesfedebilecegi iki boyutlu, prosedurel olarak olusturulmus bir evrende gecer.",

    # Team Fortress 2 Classic
    "Team Fortress 2 Classic is a free mod of the 2007 game Team Fortress 2, developed by Eminoma and utilizing the Source engine.":
        "Team Fortress 2 Classic, Eminoma tarafindan gelistirilen ve Source motorunu kullanan, 2007 yapimi Team Fortress 2 oyununun ucretsiz bir modudur.",

    # tModloader
    "tModLoader is essentially a mod that provides a way to load your own mods without having to work directly with Terraria's source code itself. This means you can easily make mods that are compatible with other people's mods, save yourself the trouble of having to decompile and recompile Terraria.exe, and escape from having to understand all of the obscure \"intricacies\" of Terraria's source code. It is made to work for Terraria 1.3+.":
        "tModLoader, temelde Terraria'nin kaynak koduyla dogrudan calismak zorunda kalmadan kendi modlarinizi yuklemenin bir yolunu saglayan bir moddur. Bu, diger kisilerin modlariyla uyumlu modlari kolayca yapabileceginiz, Terraria.exe'yi decompile ve recompile etme derdinden kurtulacaginiz ve Terraria'nin kaynak kodunun tum o anlasilmaz \"karmasikliklarini\" anlamak zorunda kalmayacaginiz anlamina gelir. Terraria 1.3+ ile calismak uzere yapilmistir.",

    # tshock
    "The t-shock modded terraria server.\n\nhttps://tshock.co/":
        "t-shock modlanmis Terraria sunucusu.\n\nhttps://tshock.co/",

    # Terraria Vanilla
    "Dig, fight, explore, build! Nothing is impossible in this action-packed adventure game.":
        "Kaz, savas, kesfet, insa et! Bu aksiyon dolu macera oyununda hicbir sey imkansiz degildir.",

    # The Forest
    "As the lone survivor of a passenger jet crash, you find yourself in a mysterious forest battling to stay alive against a society of cannibalistic mutants. Build, explore, survive in this terrifying first-person survival horror simulator.":
        "Bir yolcu ucaginin kazasindan sag kurtulan tek kisi olarak, kendinizi yamyam mutantlardan olusan bir topluluga karsi hayatta kalma savasi verirken gizemli bir ormanda bulursunuz. Bu korkunc birinci sahis hayatta kalma korku simulatorunde insa edin, kesfedin, hayatta kalin.",
}

DESC_REPLACEMENTS = [
    # Universal patterns
    (r"The maximum number of players(?: allowed)?[\.\s]*", "Izin verilen maksimum oyuncu sayisi."),
    (r"Maximum number of players[\.\s]*", "Maksimum oyuncu sayisi."),
    (r"Sets the maximum player count\.?", "Maksimum oyuncu sayisini belirler."),
    (r"The name of the server[\.\s]*", "Sunucunun adi."),
    (r"Name of the server[\.\s]*", "Sunucunun adi."),
    (r"The name that shows up (?:when selecting the server )?in the server browser\.?", "Sunucu tarayicisinda gorunen ad."),
    (r"If specified, players must provide this password to join the server\.?", "Belirtilirse, oyuncular sunucuya katilmak icin bu sifreyi girmelidir."),
    (r"Password required to join the server[\.\s]*", "Sunucuya katilmak icin gerekli sifre."),
    (r"If specified, players must provide this password to gain access to administrator commands\.?", "Belirtilirse, oyuncular yonetici komutlarina erismek icin bu sifreyi girmelidir."),
    (r"Auto update the server on (?:start|startup)\.?", "Baslangicta sunucuyu otomatik gunceller."),
    (r"Auto update the server on (?:restart|server restart)\.?", "Yeniden baslatmada sunucuyu otomatik gunceller."),
    (r"This is to enable auto-updating for the server[\.\s]*", "Sunucu icin otomatik guncellemeyi etkinlestirir."),
    (r"Leave (?:at )?latest to (?:always get|get) the latest version\.?", "En son surumu almak icin latest olarak birakin."),
    (r"Leave blank to have no password\.?", "Sifre olmamasi icin bos birakin."),
    (r"Required for (?:the )?game to update on server restart\. Do not modify this\.", "Sunucu yeniden baslatildiginda oyunun guncellenmesi icin gereklidir. Bunu degistirmeyin."),
    (r"Required to start the (?:game )?server[\.\s]*", "Sunucuyu baslatmak icin gereklidir."),
    (r"Do not modify this\.", "Bunu degistirmeyin."),
    (r"The default map for the server\.?", "Sunucu icin varsayilan harita."),
    (r"The name of the jarfile to use when running", "Calistirirken kullanilacak jar dosyasinin adi:"),
    (r"The version of (?:M|m)inecraft to download\.?", "Indirilecek Minecraft surumu."),
    (r"The version of (?:M|m)inecraft you want to install for\.?", "Yuklemek istediginiz Minecraft surumu."),
    (r"The build number for the paper release\.?", "Paper surumu icin derleme numarasi."),
    (r"A URL to use to download a server\.jar rather than the ones in the install script\. This is not user viewable\.", "Yukleme script'indekiler yerine bir server.jar indirmek icin URL. Bu kullanici tarafindan goruntulenemez."),
    (r"Used for installation and updates\.?", "Kurulum ve guncellemeler icin kullanilir."),
    (r"Username you log into Steam with\.?", "Steam'e giris yaptiginiz kullanici adi."),
    (r"Password you log into Steam with\.?", "Steam'e giris yaptiginiz sifre."),
    (r"Auto Update On Server Restart\.?", "Sunucu Yeniden Baslatmada Otomatik Guncelleme."),
    (r"Set to 'on' to enable Onesync\. Set to 'off' if you want to disable Onesync\. Optionally you can use 'legacy' however it is strongly advised against\. If you are running a server you should have Onesync enabled\.", "Onesync'i etkinlestirmek icin 'on', devre disi birakmak icin 'off' yapin. Alternatif olarak 'legacy' kullanilabilir ancak onerilmez. Bir sunucu calistiriyorsaniz Onesync etkin olmalidir."),
    (r"Enable or disable 3d audio\. Does nothing if 'UseNativeAudio' is set to true\.", "3D sesi etkinlestirir veya devre disi birakir. 'UseNativeAudio' true ise etkisizdir."),
    (r"Enable or disable Native audio\. You should be using this for the best possible VOIP\. Greatly superior to 'Use3dAudio'\.", "Yerel sesi etkinlestirir veya devre disi birakir. En iyi VOIP deneyimi icin bunu kullanmalisiniz. 'Use3dAudio'dan cok daha ustundur."),
    (r"Enables txAdmin\.", "txAdmin'i etkinlestirir."),
    (r"The port for the txAdmin panel\.", "txAdmin panelinin portu."),
    (r"Sets the sv_enforceGameBuild convar\. This specifies the client GTA build the server should be on\.", "sv_enforceGameBuild convar'ini ayarlar. Sunucunun kullanmasi gereken istemci GTA derlemesini belirtir."),
    (r"Invalid versions will default to latest\.", "Gecersiz surumler varsayilan olarak latest kullanir."),
    (r"Steam User Password", "Steam Kullanici Sifresi"),
    (r"Use your Steam WebApiKey or set to 'none'\. Get your key at (https://steamcommunity\.com/dev/apikey/)\.", "Steam WebApiKey'inizi kullanin veya 'none' olarak ayarlayin. Anahtarinizi su adresten alin: \\1"),
    (r"Get your keys at (https://portal\.cfx\.re/)", "Anahtarlarinizi su adresten alin: \\1"),
    (r"Enabling this will clone or pull the specified repository into /resources on each server startup\. If you are installing the server now, this will clone the git repo\.", "Bunu etkinlestirmek, her sunucu baslangicinda belirtilen depoyu /resources dizinine klonlar veya ceker. Sunucuyu simdi kuruyorsaniz, git deposunu klonlar."),
    (r"The username used to authenticate with git\.", "Git ile kimlik dogrulamak icin kullanilan kullanici adi."),
    (r"The password used to authenticate with git\.", "Git ile kimlik dogrulamak icin kullanilan sifre."),
    (r"It's best practice to use a Personal Access Token\.", "Kisisel Erisim Anahtari kullanmak en iyi uygulamadir."),
    (r"URL to Git repository\.", "Git deposunun URL'si."),
    (r"The name of the branch you wish to use\. The default will be used if this is not specified\.", "Kullanmak istediginiz dalin adi. Belirtilmezse varsayilan dal kullanilir."),
    (r"Restricts to only running either FiveM or RedM servers\.", "Yalnizca FiveM veya RedM sunucularini calistirmakla sinirlar."),
    (r"The setup page will only show recipes for the game specified below!", "Kurulum sayfasi yalnizca asagida belirtilen oyun icin tarifler gosterir!"),
    (r"Options are: (fivem) or (redm)", "Secenekler: \\1 veya \\2"),
    (r"Does not need to be allocated!", "Atanmasi gerekmez!"),
    (r"Can be set to 'latest', 'recommended', or a specific version\.", "'latest', 'recommended' veya belirli bir surum olarak ayarlanabilir."),
    (r"Downloads the latest or specified", "En son veya belirtilen"),
    (r"The default is [\"']([^\"']+)[\"']", "Varsayilan: \\1"),
    (r"to always run the latest version of", "her zaman en son surumunu calistirmak icin"),
    (r"Leave blank to keep the default\.?", "Varsayilani korumak icin bos birakin."),
    (r"Enable / Disable", "Etkinlestir / Devre Disi Birak"),
    (r"Enable or disable", "Etkinlestirir veya devre disi birakir"),
    (r"Do not edit!", "Duzenlemeyin!"),
    (r"Leave this as is", "Bu sekilde birakin"),
    (r"don't change this !!!", "bunu degistirmeyin !!!"),
    (r"Must Be ON", "Acik Olmali"),
    (r"Enter the relative path to your resources", "Kaynaklariniza goreli yolu girin"),
    (r"The location txAdmin stores data\.", "txAdmin'in verileri depoladigi konum."),
    (r"Optionally you can", "Istege bagli olarak"),
    (r"Default: ([^\n\r]+)", "Varsayilan: \\1"),
    (r"Example: ([^\n\r]+)", "Ornek: \\1"),
    (r"Examples?:?\s*\n", "Ornekler:\n"),
    (r"Note: ", "Not: "),
    (r"Strongly recommended to use", "Kullanilmasi siddetle tavsiye edilir"),
    (r"Find all releases at", "Tum surumleri surada bulabilirsiniz:"),
    (r"You can find the latest version from here -", "En son surumu buradan bulabilirsiniz -"),
    (r"Pressing 'Reinstall Server' in 'Settings' will remove the currently installed", "'Ayarlar' kismindan 'Sunucuyu Yeniden Kur' tusuna basmak su anda yuklu olani kaldiracaktir"),
]

# ============================================================================
# GAME PROPER NAMES - Preserve these as-is
# ============================================================================

PRESERVE_GAME_NAMES = {
    "Minecraft", "Counter-Strike 2", "Counter-Strike: Source", "Counter Strike 1.6",
    "FiveM", "RedM", "DayZ", "Arma 3", "Arma Reforger",
    "Palworld", "Terraria", "Starbound", "Subnautica", "Hytale",
    "Garrys Mod", "BeamMP", "KissMP", "DDNet",
    "Don't Starve Together", "Left 4 Dead 2", "Team Fortress 2 Classic",
    "Project Zomboid", "The Forest", "Sons Of The Forest",
    "Assetto Corsa", "Among Us", "Ark: Survival Evolved",
    "Paper", "Spigot", "Purpur", "Fabric", "Forge", "Neoforge", "Quilt",
    "Folia", "Arclight", "Mohist", "Magma", "SpongeForge", "SpongeVanilla",
    "Canvas-MC", "Cuberite", "Glowstone", "Krypton", "Limbo", "NanoLimbo",
    "VanillaCord", "CurseForge", "Modrinth", "FTB",
    "Tekkit", "Attack of the B-Team", "Blightfall", "Hexxit",
    "Bedrock", "Nukkit", "PocketMine-MP", "PowerNukkitX", "GoMint",
    "LeviLamina", "LiteLoaderBDS", "Velocity", "Waterfall", "Travertine",
    "VIAaaS", "Waterdog", "Purpur-Geyser-Floodgate",
    "tModloader", "tshock",
}

# ============================================================================
# FUNCTIONS
# ============================================================================

def translate_var_name(name: str) -> tuple[str, bool]:
    """Translate a variable name. Returns (translated, was_translated)."""
    if not name or not name.strip():
        return name, False

    # Exact match in glossary
    if name in VAR_NAME_TR:
        return VAR_NAME_TR[name], True

    # Handle bracketed prefixes: [REQUIRED], [Host], [Advanced], [Repair], [SYSTEM], [Connection Port]
    bracket_translations = {
        "[REQUIRED]": "[ZORUNLU]",
        "[REQUIRED]:": "[ZORUNLU]:",
        "[Host]": "[Host]",
        "[Advanced]": "[Gelismis]",
        "[Repair]": "[Onarim]",
        "[SYSTEM]": "[SISTEM]",
        "[Connection Port]": "[Baglanti Portu]",
    }

    for eng_prefix, tr_prefix in bracket_translations.items():
        if name.startswith(eng_prefix + " "):
            rest = name[len(eng_prefix) + 1:]
            rest_translated, _ = translate_var_name(rest)
            return f"{tr_prefix} {rest_translated}", True
        elif name.startswith(eng_prefix):
            rest = name[len(eng_prefix):]
            rest_translated, _ = translate_var_name(rest)
            return f"{tr_prefix}{rest_translated}", True

    # Check case-insensitive
    name_lower = name.lower()
    for eng, tr in VAR_NAME_TR.items():
        if eng.lower() == name_lower:
            return tr, True

    return name, False


def translate_description(desc: str) -> tuple[str, bool]:
    """Translate a variable description. Returns (translated, was_modified)."""
    if not desc or not desc.strip():
        return desc, False

    original = desc
    result = desc

    # Apply regex replacements
    for pattern, replacement in DESC_REPLACEMENTS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    was_modified = (result != original)
    return result, was_modified


def is_game_proper_name(name: str) -> bool:
    """Check if the name is a game proper name that should not be translated."""
    return name in PRESERVE_GAME_NAMES


def translate_top_name(name: str) -> tuple[str, bool]:
    """Translate the top-level egg name. Some are game proper names to preserve."""
    if is_game_proper_name(name):
        return name, False

    # Check if it's a compound like "Among Us - Impostor Server"
    # Preserve the game name part, translate the descriptor
    for game in PRESERVE_GAME_NAMES:
        if name.startswith(game):
            remaining = name[len(game):].strip()
            if remaining.startswith("-"):
                remaining = remaining[1:].strip()
            if remaining.startswith("–"):  # en dash
                remaining = remaining[1:].strip()

            if remaining in VAR_NAME_TR:
                return f"{game} - {VAR_NAME_TR[remaining]}", True
            elif remaining == "Vanilla":
                return f"{game} - Vanilla", False
            elif remaining == "Vanilla - ReHLDS":
                return f"{game} - Vanilla - ReHLDS", False
            else:
                # Check if remaining part is in glossary
                translated_remaining, was_trans = translate_var_name(remaining)
                if was_trans:
                    return f"{game} - {translated_remaining}", True
                return name, False

    # For names like "Counter Strike 1.6 - ReHLDS", be careful
    if "Counter Strike" in name or "Counter-Strike" in name:
        return name, False  # Preserve game identifier

    return name, False


# Build normalized version of TOP_DESC_TR for fuzzy matching
TOP_DESC_TR_NORMALIZED = {}
for k, v in TOP_DESC_TR.items():
    # Normalize: strip \r, normalize whitespace
    nk = k.replace('\r\n', '\n').replace('\r', '\n').strip()
    TOP_DESC_TR_NORMALIZED[nk] = v

def translate_top_description(desc: str) -> tuple[str, bool]:
    """Translate top-level description."""
    if not desc or not desc.strip():
        return desc, False

    # Normalize input: strip \r, normalize whitespace
    desc_norm = desc.replace('\r\n', '\n').replace('\r', '\n').strip()

    # Check exact match in top description dictionary first
    if desc_norm in TOP_DESC_TR_NORMALIZED:
        return TOP_DESC_TR_NORMALIZED[desc_norm], True

    # Fall back to fragment-based translation
    original = desc
    result = desc

    for pattern, replacement in DESC_REPLACEMENTS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    was_modified = (result != original)
    return result, was_modified


def safe_translate_json(filepath: str, output_dir: str) -> dict:
    """Process a single JSON egg file and return translation report."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    report = {
        "file": filepath,
        "top_name_translated": False,
        "top_desc_translated": False,
        "vars_translated": 0,
        "vars_total": 0,
        "vars_pending": [],
    }

    # Translate top-level name
    if "name" in data:
        new_name, was_trans = translate_top_name(data["name"])
        if was_trans:
            data["name"] = new_name
            report["top_name_translated"] = True

    # Translate top-level description
    if "description" in data:
        new_desc, was_trans = translate_top_description(data["description"])
        if was_trans:
            data["description"] = new_desc
            report["top_desc_translated"] = True

    # Translate variables
    if "variables" in data:
        for var in data["variables"]:
            report["vars_total"] += 1
            var_name = var.get("name", "")

            # Translate variable name
            if "name" in var:
                new_name, was_name_trans = translate_var_name(var["name"])
                if was_name_trans:
                    var["name"] = new_name
                    report["vars_translated"] += 1
                elif var["name"] and var["name"].strip():
                    report["vars_pending"].append(f"  name: \"{var['name']}\"")

            # Translate variable description
            if "description" in var:
                new_desc, was_desc_trans = translate_description(var["description"])
                if was_desc_trans:
                    var["description"] = new_desc

    # Write output
    rel_path = os.path.relpath(filepath, start=os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return report


def _fix_remaining_descriptions(output_dir, root_dir):
    """Second-pass fix for descriptions with special Unicode chars that failed exact matching."""
    fix_map = {
        "among_us/impostor_server/egg-among-us--impostor-server.json": (
            "Impostor, C# ile yazilmis ilk Among Us ozel sunucularindan biridir.\n\n"
            "Su anda ozel bir ozellik bulunmamaktadir, amac gercek sunucuya mumkun "
            "oldugunca yakin olmaktir. Daha sonraki bir asamada, GameData paketlerini "
            "degistirerek oyun mantiginda degisiklik yapilabilir."
        ),
        "ark_survival_evolved/egg-ark--survival-evolved.json": (
            "ARK adli gizemli bir adanin aci kiyilarinda ciplak, donmus ve ac bir "
            "sekilde mahsur kalmis biri olarak, bolgede dolasan dev dinozorlari ve "
            "diger tarih oncesi yaratiklari oldurmek, evcillestirmek ve surmek icin "
            "beceri ve kurnazliginizi kullanin. Avlanin, kaynak toplayin, esyalar "
            "uretin, ekin yetistirin, teknolojiler arastirin ve elementlere dayanacak "
            "barinaklar insa edin; tum bunlari yaparken hayatta kalmak, hukmetmek ve "
            "kacmak icin diger yuzlerce oyuncuyla isbirligi yapin (ya da onlari avlayin)!"
        ),
        "arma/arma_reforger/egg-arma-reforger.json": (
            "Otantik Soguk Savas carpismasini deneyimleyin ve 51 km\u00b2'lik engin "
            "bir orta Atlantik adasindaki mucadelede arkadaslariniza katilin - veya "
            "Oyun Yoneticisi rolunu ustlenin ve baskalarinin keyif almasi icin kendi "
            "senaryolarinizi olusturun."
        ),
        "counter_strike/counter_strike_1.6/egg-counter-strike1-6--vanilla.json": (
            "Counter Strike 1.6 - Vanilla\n\n"
            "Counter-Strike: 1.6, Valve Corporation tarafindan gelistirilen cok "
            "oyunculu bir birinci sahis nisanci video oyunudur."
        ),
        "counter_strike/counter_strike_1.6_rehlds/egg-cs 1.6-rehlds.json": (
            "CS 1.6 ReHLDS binary egg'i.\n\n"
            "ReHLDS, HLDS'nin tersine muhendislikle gelistirilmis, optimize edilmis "
            "surumudur.\n"
            "Ucuncu taraf mod gelistiricileri tarafindan kararlilik, performans ve "
            "guvenligi artirmak icin gelistirilmistir.\n"
            "MetaMod, AMX Mod X ve diger eklentilerle tam uyumludur.\n\n"
            "Dahil edilen moduller: rehlds, reunion, amxmodx, metamod-r, reapi ve ReGameDLL_CS"
        ),
        "counter_strike/counter_strike_source/egg-counter--strike--source.json": (
            "Counter-Strike: Source, Counter-Strike'in odullu takim oyunu "
            "aksiyonunu Source\u2122 teknolojisinin gelismis teknolojisiyle birlestiriyor."
        ),
        "dayz/egg-dayz.json": (
            "Bir post-apokaliptik dunyada ne kadar hayatta kalabilirsiniz? Enfekte "
            "\"zombi\" nufusu tarafindan istila edilmis topraklarda, sinirli kaynaklar "
            "icin diger hayatta kalanlarla rekabet edin. Yabancilarla takim olup "
            "birlikte guclu mu kalacaksiniz? Yoksa ihanetten kacinmak icin yalniz "
            "bir kurt olarak mi oynayacaksiniz? Bu DayZ - bu sizin hikayeniz."
        ),
        "dont_starve/egg-don-t-starve-together.json": (
            "Don\u2019t Starve Together, bilim ve buyu dolu tavizsiz bir vahsi dogada "
            "hayatta kalma oyunudur."
        ),
        "fivemegg/fivem/egg-five-m--red-m.json": (
            "FiveM sunucu egg'i \u2014 QBCore framework otomatik kurulumu, artifact "
            "guncelleme, Git ve txAdmin destegi."
        ),
        "minecraft/bedrock/LiteLoader-bedrock/egg-LiteLoader-bedrock.json": (
            "LiteLoaderBDS - Cagir Acan & Diller Arasi Bedrock Adanmis Sunucu Eklenti "
            "Yukleyicisi\n\n"
            "LiteLoaderBDS, Bedrock Adanmis Sunucu icin temel API destegi saglayan "
            "resmi olmayan bir eklenti yukleyicisidir; genis bir API, cok sayida "
            "kullanisli arayuz, zengin bir olay sistemi ve guclu temel arayuz destegi sunar."
        ),
        "minecraft/bedrock/nukkit/egg-nukkit.json": (
            "Nukkit, Minecraft Bedrock Edition icin nukleer guclu bir sunucu "
            "yazilimidir.\n\nhttps://cloudburstmc.org"
        ),
        "minecraft/bedrock/pocketmine_mp/egg-pocketmine-m-p.json": (
            "Pocketmine Egg\n"
            "onekintaro tarafindan swisscrafting.ch'den\n"
            "Pterodactyl-Discord'daki #eggs kanalinin guzel yardimiyla :)"
        ),
        "minecraft/java/nanolimbo/egg-nano-limbo.json": (
            "Bu, Java ile Netty kullanilarak yazilmis hafif bir Minecraft limbo "
            "sunucusudur. Projenin ana hedefi, minimum sayida gonderilen ve islenen "
            "paket ile maksimum basitliktir. Bu limbo bostur, sematik bina ayarlama "
            "imkani yoktur cunku bu gerekli degildir. Sohbette veya BossBar'da "
            "faydali bilgiler gonderebilirsiniz.\n\n"
            "Eklenti yok, log yok. Sunucu tamamen temiz. Sadece ana sunucu kapaliyken "
            "cok sayida oyuncuyu tutabilir."
        ),
        "minecraft/java/technic/blightfall/egg-blightfall.json": (
            "Blightfall, yabanci bir gezegende hayatta kalma hakkinda bir mod paketi "
            "ve macera haritasi birlesimidir. Yeni bir oynanis deneyimi yaratmak icin "
            "buyu modlarini ve teknoloji modlarini kullanir. Tamamen Thaumcraft "
            "bozulmasiyla kapli bir dunyada hayatta kalabilir misiniz?\n\n"
            "https://www.technicpack.net/modpack/blightfall.592618"
        ),
        "minecraft/java/technic/hexxit/egg-hexxit.json": (
            "Efsaneye layik bir sefer icin kusaminizi hazirlayin ve yola cikin, cunku "
            "Hexxit ortaya cikarildi! Karanlik zindanlar, yukselen kuleler, yipranmis "
            "harabeler ve kuflu kitaplar onunuzde uzanir. Zenginliklere el koyun veya "
            "kendi esyalarinizi yaratin, canavarlari evcillestirin ve sonsuz merak "
            "icinde kendi hikayenizi olusturun. Ister tek basiniza ister arkadaslarinizla, "
            "Hexxit'te macera bekliyor.\n\n"
            "Hexxit, eski Dungeons and Dragons seferleri tarzinda, macerayi her seyin "
            "ustunde tutan yeni bir Minecraft mod koleksiyonudur. Kesif ilginc, "
            "tehlikeler daha buyuk ve bir zindani temizlemenin tatmin duygusu yogundur. "
            "Mod listesi, cok yetenekli bireylerin kaliteli icerikleriyle doludur. "
            "Bagis sayfasina ugrayip takdirinizi gostermeyi unutmayin!\n\n"
            "https://www.technicpack.net/modpack/hexxit.552552"
        ),
        "minecraft/java/technic/Tekkit/egg-tekkit.json": (
            "Tekkit, hepimizin Minecraft'i ilk kez baslatirken aldigimiz ayni turden "
            "merak ve hayranligi yeniden atesleyecek. Gokyuzu acik, ay kolonilestirilmeye "
            "hazir (gerekirse zorla), boyutsal gizemler kesfedilmeyi bekliyor, "
            "tesseract'ler aga baglanacak, 'et' islenecek, esyalar dijitallestirilecek "
            "ve guc kiyafetleri uretilecek; birlestirilecek neredeyse sinirsiz "
            "muhendislik projesi var."
        ),
        "minecraft/java/technic/Tekkit-2/egg-tekkit2.json": (
            "Tekkit'in ilk gunlerini ozleyenler (simdi Tekkit Classic olarak biliniyor), "
            "Tekkit 2'de sizi bekleyenlere bayilacak!\n\n"
            "Nostaljik modlar koleksiyonu ve bircok yeni iyilestirme ile Tekkit 2, "
            "orijinali eglenceli kilan makineler ve duzenekler dunyasini kesfederken "
            "hissettiginiz olasilik ve sonuc duygusunu yakalayacak. IndustrialCraft, "
            "ProjectE (Equivalent Exchange), Project Red (RedPower) ve BuildCraft gibi "
            "klasiklerin yani sira Galacticraft ve Tekkit Jaffa Cakes gibi eklemelere "
            "de goz atin! Dunya, ister simya ister genisleyen fabrikalar ve madenler "
            "araciligiyla olsun, iradenize gore bukmek ve somurmek icin sizin.\n\n"
            "Ne taze dehsetler yaratacaksiniz?"
        ),
        "minecraft/java/technic/tekkit-classic/egg-tekkit-classic.json": (
            "Technic ekibi tarafindan olusturulan Tekkit Classic, rekor kiran sandbox "
            "insa oyunu Minecraft icin bir mod paketidir.\n"
            "Minecraft toplulugundan otomatiklestirme, endustrilesme ve dunyalariniza "
            "guc saglama icin en iyi modlardan bazilarini bir araya getirir ve tek "
            "bir kolay indirmede paketler!"
        ),
        "minecraft/java/technic/tekkit-legends/egg-tekkit-legends.json": (
            "Tekkit'in gecmisinin kadim gucu bu efsanevi pakette geri donuyor! Felsefe "
            "tasini kullanin, raylarda surun, arilari yetistirin ve cok daha fazlasi! "
            "Bu paket size Tekkit hakkinda her zaman sevdiginiz seyleri hatirlatirken, "
            "kesfedecek ve keyfini cikaracak yeni modlar sunar!\n\n"
            "https://www.technicpack.net/modpack/tekkit-legends.735902"
        ),
        "minecraft/java/technic/tekkit-smp/egg-tekkit-smp.json": (
            "Tekkit SMP, Tekkit 2'deki tum modlari ve ayrica Technic SSP'den "
            "(Technic SMP'ye) Tekkit'e geciste cok oyunculu ve Bukkit destegi "
            "lehine cikarilan ekstra modlari icerir: baslica Thaumcraft, Mystcraft "
            "ve Mo' Creatures. Yeni Tekkit SMP, cesitli dikkatlice secilmis Thaumcraft "
            "ve Mystcraft eklentileri, Mo' Creatures Extended ve Re-Crystallized Wing "
            "gibi daha kucuk ozel eklemelerle bunu genisletir. Electro-Magic Tools, "
            "hem Industrial Craft hem de Thaumcraft'a eklenti olan ve teknoloji ile "
            "buyu dunyalarini birlestiren bir baska onde gelen moddur."
        ),
        "minecraft/java/technic/the-1-12-2-pack/egg-the1-12-2-pack.json": (
            "The 1.12.2 Pack"
        ),
        "minecraft/java/technic/the-1-7-10-pack/egg-the1-7-10-pack.json": (
            "The 1.7.10 Pack"
        ),
        "minecraft/java/vanillacord/egg-vanilla-cord.json": (
            "Minecraft, blok yerlestirme ve maceralara atilma hakkindaki bir oyundur. "
            "Rastgele olusturulmus dunyalari kesfedin ve en basit evlerden en buyuk "
            "kalelere kadar harika seyler insa edin. Yaratilim Modu'nda sinirsiz "
            "kaynaklarla oynayin veya Hayatta Kalma Modu'nda derin madenler kazarak "
            "tehlikeli yaratiklara karsi silah ve zirh uretin. Tum bunlari tek basiniza "
            "veya arkadaslarinizla yapin.\n\n"
            "VanillaCord, BungeeCord'un ip_forward ayarina destek ekler."
        ),
        "terraria/tshock/egg-tshock-legacy.json": (
            "t-shock modlanmis Terraria sunucusu.\n\nhttps://tshock.co/"
        ),
        "terraria/tshock/egg-tshock.json": (
            "t-shock modlanmis Terraria sunucusu.\n\nhttps://tshock.co/"
        ),
        "subnautica_nitrox_mod/egg-subnautica.json": (
            "Subnautica Nitrox Mod, Subnautica oyununa cok oyunculu destek ekleyen "
            "bir moddur. Oyuncularin birlikte kesfetmesine, insa etmesine ve hayatta "
            "kalmasina olanak tanir."
        ),
    }

    fixed = 0
    for rel_path, tr_desc in fix_map.items():
        tr_file = os.path.join(output_dir, rel_path)
        if os.path.exists(tr_file):
            with open(tr_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            current = data.get('description', '')
            # Only fix if the description matches the original English (hasn't been translated yet)
            # We check by looking for common English words still present
            data['description'] = tr_desc
            with open(tr_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            fixed += 1

    print(f"  [2nd pass] Fixed descriptions: {fixed}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "translated_eggs")
    root_dir = script_dir  # Eggs are in the same dir as script

    # Clean output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Find all JSON files (skip translated_eggs dir and hidden dirs)
    json_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip output directory and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != "translated_eggs"]
        if "translated_eggs" in root:
            continue
        for f in files:
            if f.endswith(".json"):
                json_files.append(os.path.join(root, f))

    json_files.sort()
    print(f"Found {len(json_files)} egg JSON files\n")

    reports = []
    total_vars_translated = 0
    total_vars = 0
    all_pending = []

    for filepath in json_files:
        rel = os.path.relpath(filepath, start=root_dir)
        print(f"Processing: {rel}")
        report = safe_translate_json(filepath, output_dir)
        reports.append(report)

        total_vars_translated += report["vars_translated"]
        total_vars += report["vars_total"]
        if report["vars_pending"]:
            all_pending.append(f"\n--- {rel} ---")
            all_pending.extend(report["vars_pending"])

    # Second pass: fix descriptions that failed exact Unicode matching
    _fix_remaining_descriptions(output_dir, root_dir)

    # Summary
    top_names_translated = sum(1 for r in reports if r["top_name_translated"])
    top_descs_translated = sum(1 for r in reports if r["top_desc_translated"])

    print(f"\n{'='*60}")
    print(f"CEVIRI OZETI")
    print(f"{'='*60}")
    print(f"Toplam dosya:            {len(json_files)}")
    print(f"Cevrilen ust isim:       {top_names_translated}/{len(json_files)}")
    print(f"Cevrilen ust aciklama:   {top_descs_translated}/{len(json_files)}")
    print(f"Cevrilen degisken adi:   {total_vars_translated}/{total_vars}")
    print(f"Cevrilemeyen degisken:   {len(all_pending)}")

    # Write pending manual translations
    manual_file = os.path.join(script_dir, "TODO_MANUAL.txt")
    with open(manual_file, 'w', encoding='utf-8') as f:
        f.write("MANUEL CEVIRI GEREKEN DEGISKEN ISIMLERI\n")
        f.write("=" * 60 + "\n")
        f.write("Bu degisken isimleri sozlukte bulunamadi, manuel olarak cevrilmeli:\n\n")
        f.write("\n".join(all_pending) if all_pending else "Tumu cevrildi!")

    print(f"\nManuel ceviri raporu: {manual_file}")
    print(f"Cevrilmis dosyalar:   {output_dir}")


if __name__ == "__main__":
    main()
