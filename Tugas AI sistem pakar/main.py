import json
with open("aturan.json", "r", encoding="utf-8") as file:
    knowledge = json.load(file)

print("=" * 45)
print(knowledge["judul"])
print("=" * 45)

print("\nBatas Sistem:")
print(knowledge["batas_keberlakuan"])

pertanyaan = {
    "1": "Apakah kamu menyukai pakaian dengan potongan sederhana, minim motif, dan warna netral?",
    "2": "Apakah kamu lebih menyukai aksesoris sederhana seperti jam tangan polos, kalung tipis, atau tas tanpa banyak hiasan?",

    "3": "Apakah kamu lebih sering memilih kaus, jeans, kemeja santai, atau sweater untuk aktivitas sehari-hari?",
    "4": "Apakah kamu menyukai aksesoris praktis seperti topi, jam tangan kasual, atau tote bag?",

    "5": "Apakah kamu menyukai pakaian oversized, hoodie, atau kaus dengan grafis dan desain mencolok?",
    "6": "Apakah kamu menyukai aksesoris seperti snapback, rantai, sling bag, atau sneakers yang menjadi pusat perhatian?",

    "7": "Apakah kamu menyukai pakaian dengan potongan klasik, motif retro, atau model yang terinspirasi dari era terdahulu?",
    "8": "Apakah kamu menyukai aksesoris seperti kacamata retro, jam tangan klasik, atau tas bergaya vintage?",

    "9": "Apakah kamu menyukai outfit dengan perpaduan warna senada, layering, dan potongan pakaian yang rapi?",
    "10": "Apakah kamu menyukai aksesoris seperti tas kecil, jepit rambut, atau perhiasan minimalis yang melengkapi outfit?",

    "11": "Apakah kamu menyukai pakaian berpotongan rapi seperti blazer, dress, atau celana bahan dengan kesan berkelas?",
    "12": "Apakah kamu menyukai aksesoris seperti jam tangan elegan, anting sederhana, atau tas dengan desain mewah?",

    "13": "Apakah kamu menyukai pakaian bergaya atletik seperti tracksuit, jogger, hoodie, atau pakaian berbahan fleksibel?",
    "14": "Apakah kamu menyukai aksesoris seperti topi olahraga, smartwatch, atau tas ransel sporty?"
}

fakta_user = set()

print("\n=== PERTANYAAN REKOMENDASI ===")
print("Jawab dengan y (Ya) atau n (Tidak)")

for kode, teks in pertanyaan.items():
    while True:
        jawaban = input(f"\n{kode}. {teks} (y/n): ").strip().lower()

        if jawaban == "y":
            fakta_user.add(f"jawaban_{kode}_ya")
            break
        elif jawaban == "n":
            break
        else:
            print("Masukkan y atau n!")

fakta = set(fakta_user)
aturan_terpakai = []
aturan_diproses = set()

while True:
    fakta_sebelumnya = fakta.copy()
    aturan_baru = []

    for aturan in knowledge["aturan"]:
        if aturan["id"] in aturan_diproses:
            continue

        kondisi = aturan["jika"]
        mode = aturan["mode"]

        if mode == "dan":
            cocok = all(item in fakta_sebelumnya for item in kondisi)
        elif mode == "atau":
            cocok = any(item in fakta_sebelumnya for item in kondisi)
        else:
            cocok = False
        if cocok:
            aturan_baru.append(aturan)
    if not aturan_baru:
        break
    for aturan in aturan_baru:
        fakta.add(aturan["maka"])
        aturan_diproses.add(aturan["id"])
        aturan_terpakai.append(aturan)

hasil = [
    aturan for aturan in aturan_terpakai
    if aturan.get("jenis") == "kesimpulan"
]
hasil = hasil[:2]

print("\n" + "=" * 45)
print("=== HASIL REKOMENDASI STYLE ===")
print("=" * 45)

if hasil:
    for nomor, aturan in enumerate(hasil, start=1):
        print(f"\n{nomor}. {aturan['style']}")

        print("\nAturan aktif:")

        for aturan_aktif in aturan_terpakai:
            if aturan_aktif["style"] == aturan["style"]:
                print(f"- {aturan_aktif['id']}")
                
        print(f"\nKesimpulan: {aturan['style']}")
        print("Penjelasan:", aturan["penjelasan"])
        print("\nReferensi:")

        kode_sumber = aturan["sumber"]

        if isinstance(kode_sumber, str):
            kode_sumber = [kode_sumber]

        for kode in kode_sumber:
            print(f"- {kode}: {knowledge['sumber'][kode]}")

        print("-" * 45)
else:
    print("\nStyle belum dapat ditentukan.")
print("\n=== REKOMENDASI SELESAI ===")
