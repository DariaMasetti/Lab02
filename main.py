
import csv


def carica_da_file(file_path):
    """Carica le foto dal file e le raggruppa per anno."""
    album = {}

    try:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            lettore = csv.reader(file, skipinitialspace=True)
            next(lettore, None)  # Salta l'intestazione

            for campi in lettore:
                if not campi:
                    continue

                codice, titolo, autore, mese, anno = campi

                foto = {
                    "codice": codice.strip(),
                    "titolo": titolo.strip(),
                    "autore": autore.strip(),
                    "mese": int(mese),
                    "anno": int(anno)
                }

                anno = foto["anno"]

                if anno not in album:
                    album[anno] = []

                album[anno].append(foto)

    except FileNotFoundError:
        return None

    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album e al file."""
    if mese < 1 or mese > 12:
        return None

    if cerca_foto(album, codice) is not None:
        return None

    foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    try:

        with open(file_path, "r+", encoding="utf-8", newline="") as file:
            contenuto = file.read()
            file.seek(0, 2)

            if contenuto and not contenuto.endswith(("\n", "\r")):
                file.write("\n")

            scrittore = csv.writer(file)
            scrittore.writerow([codice, titolo, autore, mese, anno])

    except OSError:
        return None


    if anno not in album:
        album[anno] = []

    album[anno].append(foto)

    return foto


def cerca_foto(album, codice):

    for anno in album:
        for foto in album[anno]:
            if foto["codice"] == codice:
                return (
                    f'{foto["codice"]}, {foto["titolo"]}, '
                    f'{foto["autore"]}, {foto["mese"]}, {foto["anno"]}'
                )

    return None


def elenco_foto_anno_per_titolo(album, anno):

    if anno not in album:
        return None

    titoli = []

    for foto in album[anno]:
        titoli.append(foto["titolo"])

    titoli.sort()

    return titoli


def main():
    album = None
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input(
                    "Inserisci il path del file da caricare: "
                ).strip()

                album = carica_da_file(file_path)

                if album is not None:
                    print("Album caricato con successo!")
                    break

                print("File non trovato. Riprova.")

        elif scelta == "2":
            if album is None:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()

            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())

            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(
                album, codice, titolo, autore, mese, anno, file_path
            )

            if foto is not None:
                print("Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto o non è stato caricato.")
                continue

            codice = input(
                "Inserisci il codice della foto da cercare: "
            ).strip()

            risultato = cerca_foto(album, codice)

            if risultato is not None:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto o non è stato caricato.")
                continue

            try:
                anno = int(
                    input("Inserisci l'anno da consultare: ").strip()
                )

            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)

            if titoli is not None:
                print(f"\nFoto del {anno}:")

                for titolo in titoli:
                    print(f"- {titolo}")

            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break

        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()