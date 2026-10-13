from pathlib import Path
from src import encrypt, decrypt

MODES = {
    "cbc": "CBC",
    "cfb": "CFB",
    "ctr": "CTR",
    "ecb": "ECB",
    "ofb": "OFB",
}

IV_MODES = {"cbc", "cfb", "ofb"}
COUNTER_MODES = {"ctr"}

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value

        print("Input tidak boleh kosong!")

def get_mode():
    while True:
        print(f"\nMode operasi: CBC, CFB, CTR, ECB, OFB")
        mode = input("Mode: ").strip().lower()

        if mode in MODES:
            return mode

        print("Mode tidak valid!")

def get_file_path(prompt, must_exist=False):
    while True:
        raw_path = input(prompt).strip()

        if not raw_path:
            print("Path tidak boleh kosong!")
            continue

        try:
            path = Path(raw_path).expanduser()

            if not path.is_absolute():
                path = Path.cwd() / path
            if must_exist:
                if not path.exists():
                    print("File tidak ditemukan!")
                    continue
                if not path.is_file():
                    print("Path bukan file!")
                    continue
                if not path.stat().st_size:
                    print("Peringatan: file kosong!")
            else:
                if path.exists():
                    if path.is_dir():
                        print("Path mengarah ke direktori!")
                        continue
                    print("File sudah ada. Gunakan nama file lain!")
                    continue
                if not path.parent.exists():
                    print("Direktori tidak ditemukan!")
                    continue
                if not path.parent.is_dir():
                    print("Path direktori output tidak valid!")
                    continue
            return path
        except (OSError, ValueError) as exc:
            print(f"Error saat memeriksa path: {exc}")

def get_cipher_parameters(mode):
    key = get_non_empty_input("Key (string): ")
    parameters = {}

    if mode in IV_MODES:
        parameters["iv"] = get_non_empty_input("IV: ").encode("utf-8")
    elif mode in COUNTER_MODES:
        parameters["counter"] = get_non_empty_input("Counter: ").encode("utf-8")

    return key, parameters


def get_action():
    while True:
        action = input(
            "\nPilih aksi:\n"
            "  1. Encrypt\n"
            "  2. Decrypt\n"
            "  3. Exit\n"
            "Pilihan: "
        ).strip().lower()

        if action in {"1", "encrypt", "e"}:
            return "encrypt"
        if action in {"2", "decrypt", "d"}:
            return "decrypt"
        if action in {"3", "exit", "quit", "q"}:
            return "exit"
        print("Pilihan tidak valid! Masukkan 1, 2, atau 3.")


def process_file():
    action = get_action()

    if action == "exit":
        return False

    mode = get_mode()
    input_path = get_file_path(
        "Path file input: ",
        must_exist=True,
    )
    key, parameters = get_cipher_parameters(mode)

    output_path = get_file_path("Path file output: ")

    try:
        if input_path.resolve() == output_path.resolve():
            print("Nama file input dan output harus berbeda!")
            return True
    except Exception as exc:
        print(f"Error: {exc}")
        return True

    try:
        if action == "encrypt":
            plaintext = input_path.read_text(encoding="utf-8").rstrip("\r\n")

            result = encrypt(plaintext, key, mode, **parameters)
            output_path.write_text(result.hex(), encoding="ascii",)
        else:
            hex_text = input_path.read_text(encoding="ascii").strip()
            try:
                ciphertext = bytes.fromhex(hex_text)
            except ValueError as exc:
                raise ValueError("Ciphertext bukan format hexadecimal yang valid")

            result = decrypt(ciphertext, key, mode, **parameters)
            output_path.write_text(result.rstrip("\r\n"), encoding="utf-8")

        print("\nProses berhasil")
        print(f"Input : {input_path}")
        print(f"Output: {output_path}")

    except (ValueError, TypeError, KeyError) as exc:
        print(f"Error pada proses enkripsi/dekripsi: {exc}")
    except Exception as exc:
        print(
            f"error:: {exc}"
        )

    return True


def main():
    print("=" * 45)
    print("Cakra Cipher CLI Application")
    print("=" * 45)

    while True:
        if not process_file():
            break

if __name__ == "__main__":
    main()
