#!/usr/bin/env python3
"""Fix remaining untranslated descriptions by directly reading original files."""

import json
import os

root = 'C:/Users/burak/Desktop/VEHOZER/EGGS'
tr_root = root + '/translated_eggs'

# Map: rel_path -> Turkish translation
translations = {
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
        "Dahil edilen moduller: rehlds, reunion, amxmodx, metamod-r, reapi ve "
        "ReGameDLL_CS"
    ),
    "counter_strike/counter_strike_source/egg-counter--strike--source.json": (
        "Counter-Strike: Source, Counter-Strike'in odullu takim oyunu "
        "aksiyonunu Source\u2122 teknolojisinin gelismis teknolojisiyle birlestiriyor."
    ),
    "dayz/egg-dayz.json": (
        'Bir post-apokaliptik dunyada ne kadar hayatta kalabilirsiniz? Enfekte '
        '"zombi" nufusu tarafindan istila edilmis topraklarda, sinirli kaynaklar '
        'icin diger hayatta kalanlarla rekabet edin. Yabancilarla takim olup '
        'birlikte guclu mu kalacaksiniz? Yoksa ihanetten kacinmak icin yalniz '
        'bir kurt olarak mi oynayacaksiniz? Bu DayZ - bu sizin hikayeniz.'
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

# Apply translations directly to translated_eggs
fixed = 0
for rel_path, tr_desc in translations.items():
    tr_file = os.path.join(tr_root, rel_path)
    if os.path.exists(tr_file):
        with open(tr_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        original = data.get('description', '')
        data['description'] = tr_desc
        with open(tr_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Fixed: {rel_path}")
        fixed += 1
    else:
        print(f"MISSING: {tr_file}")

print(f"\nTotal fixed: {fixed}/{len(translations)}")
