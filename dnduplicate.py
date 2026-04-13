#!/usr/bin/env python3

import os
import sys
import time
from pathlib import Path

R   = "\033[0;31m"
G   = "\033[0;32m"
Y   = "\033[0;33m"
C   = "\033[0;36m"
W   = "\033[1;37m"
DIM = "\033[2m"
RST = "\033[0m"
BOLD= "\033[1m"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def banner():
    print(f"""
{C}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   {W}{BOLD} ██████╗ ███╗   ██╗██████╗ ██╗   ██╗██████╗ {C}           ║
║   {W}{BOLD}██╔══██╗████╗  ██║██╔══██╗██║   ██║██╔══██╗{C}           ║
║   {W}{BOLD}██║  ██║██╔██╗ ██║██║  ██║██║   ██║██████╔╝{C}           ║
║   {W}{BOLD}██║  ██║██║╚██╗██║██║  ██║██║   ██║██╔═══╝ {C}           ║
║   {W}{BOLD}╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝██║     {C}           ║
║   {W}{BOLD} ╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝     {C}           ║
║                                                          ║
║   {Y}        Domain Duplicate Cleaner & Splitter{C}          ║
║   {DIM}               dnduplicate.id  v1.0{C}                  ║
╚══════════════════════════════════════════════════════════╝{RST}
""")


def menu():
    print(f"""  {W}[ MAIN MENU ]{RST}
  {C}─────────────────────────────────────────{RST}
  {G}[1]{RST}  Clear Duplicate Domains
  {G}[2]{RST}  Split Domain List
  {Y}[0]{RST}  Exit
  {C}─────────────────────────────────────────{RST}""")


def prompt_file(label="Input file path"):
    while True:
        path = input(f"\n  {C}» {W}{label}: {RST}").strip().strip('"').strip("'")
        if not path:
            print(f"  {R}[!] Path tidak boleh kosong.{RST}")
            continue
        p = Path(path)
        if not p.exists():
            print(f"  {R}[!] File tidak ditemukan: {path}{RST}")
            continue
        if not p.is_file():
            print(f"  {R}[!] Bukan sebuah file.{RST}")
            continue
        return p


def read_domains(path: Path) -> list[str]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def progress_bar(current, total, width=40):
    pct  = current / total if total else 1
    done = int(pct * width)
    bar  = f"{G}{'█' * done}{DIM}{'░' * (width - done)}{RST}"
    return f"  [{bar}] {W}{current:,}/{total:,}{RST} ({pct*100:.1f}%)"


def clear_duplicates():
    clear()
    banner()
    print(f"  {W}[ OPSI 1 — CLEAR DUPLICATE ]{RST}\n")

    src = prompt_file("File domain (input)")

    print(f"\n  {DIM}Membaca file...{RST}")
    t0    = time.perf_counter()
    raw   = read_domains(src)
    total = len(raw)

    if total == 0:
        print(f"\n  {R}[!] File kosong atau tidak ada domain yang valid.{RST}")
        _pause()
        return

    print(f"  {DIM}Memproses {total:,} domain...{RST}")
    seen   : set[str]  = set()
    unique : list[str] = []
    dups   : list[str] = []

    for d in raw:
        d_low = d.lower()
        if d_low in seen:
            dups.append(d)
        else:
            seen.add(d_low)
            unique.append(d)

    elapsed      = time.perf_counter() - t0
    dup_count    = len(dups)
    unique_count = len(unique)

    print(f"""
  {C}─────────────────────────────────────────{RST}
  {W}HASIL ANALISIS{RST}
  {C}─────────────────────────────────────────{RST}
  Total domain     : {W}{total:,}{RST}
  Domain unik      : {G}{unique_count:,}{RST}
  Domain duplikat  : {R}{dup_count:,}{RST}
  Waktu proses     : {Y}{elapsed*1000:.2f} ms{RST}
  {C}─────────────────────────────────────────{RST}""")

    if dup_count == 0:
        print(f"\n  {G}[✓] Tidak ada duplikat ditemukan. File sudah bersih!{RST}")
        _pause()
        return

    preview_n = min(10, dup_count)
    print(f"\n  {Y}Preview {preview_n} duplikat pertama:{RST}")
    for i, d in enumerate(dups[:preview_n], 1):
        print(f"  {DIM}{i:>3}.{RST}  {d}")
    if dup_count > preview_n:
        print(f"  {DIM}     ... dan {dup_count - preview_n:,} lainnya{RST}")

    default_out = src.parent / f"{src.stem}_clean{src.suffix}"
    out_input   = input(f"\n  {C}» {W}Simpan ke (Enter = {default_out.name}): {RST}").strip()
    out_path    = Path(out_input) if out_input else default_out

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(unique) + "\n")

    print(f"\n  {G}[✓] Berhasil disimpan ke: {W}{out_path}{RST}")
    print(f"  {G}[✓] {unique_count:,} domain unik tersimpan, {dup_count:,} duplikat dihapus.{RST}")

    save_dup = input(f"\n  {Y}Simpan juga daftar duplikat? (y/N): {RST}").strip().lower()
    if save_dup == "y":
        dup_path  = src.parent / f"{src.stem}_duplicates{src.suffix}"
        dup_input = input(f"  {C}» {W}Simpan daftar duplikat ke (Enter = {dup_path.name}): {RST}").strip()
        if dup_input:
            dup_path = Path(dup_input)
        with open(dup_path, "w", encoding="utf-8") as f:
            f.write("\n".join(dups) + "\n")
        print(f"  {G}[✓] Daftar duplikat disimpan ke: {W}{dup_path}{RST}")

    _pause()


def split_domains():
    clear()
    banner()
    print(f"  {W}[ OPSI 2 — SPLIT DOMAIN LIST ]{RST}\n")

    src = prompt_file("File domain (input)")

    print(f"\n  {DIM}Membaca file...{RST}")
    domains = read_domains(src)
    total   = len(domains)

    if total == 0:
        print(f"\n  {R}[!] File kosong atau tidak ada domain yang valid.{RST}")
        _pause()
        return

    print(f"  {G}[✓] Ditemukan {total:,} domain.{RST}")

    while True:
        raw_n = input(f"\n  {C}» {W}Bagi menjadi berapa bagian? {DIM}(maks {total:,}){RST}: ").strip()
        if not raw_n.isdigit() or int(raw_n) < 1:
            print(f"  {R}[!] Masukkan angka bulat positif.{RST}")
            continue
        n_parts = int(raw_n)
        if n_parts > total:
            print(f"  {R}[!] Jumlah bagian ({n_parts:,}) melebihi jumlah domain ({total:,}).{RST}")
            continue
        break

    base      = total // n_parts
    remainder = total % n_parts
    sizes     = [base + (1 if i < remainder else 0) for i in range(n_parts)]

    print(f"""
  {C}─────────────────────────────────────────{RST}
  {W}RENCANA PEMBAGIAN{RST}
  {C}─────────────────────────────────────────{RST}
  Total domain : {W}{total:,}{RST}
  Jumlah bagian: {W}{n_parts}{RST}
  Per bagian   : {W}{base:,}{RST}{f" (+ {remainder} bagian dapat 1 ekstra)" if remainder else ""}
  {C}─────────────────────────────────────────{RST}""")

    default_dir = src.parent / f"{src.stem}_split"
    dir_input   = input(f"\n  {C}» {W}Folder output (Enter = {default_dir.name}/): {RST}").strip()
    out_dir     = Path(dir_input) if dir_input else default_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    default_prefix = src.stem
    prefix_input   = input(f"  {C}» {W}Prefix nama file (Enter = '{default_prefix}'): {RST}").strip()
    prefix         = prefix_input if prefix_input else default_prefix

    t0      = time.perf_counter()
    idx     = 0
    padding = len(str(n_parts))
    written = []

    print(f"\n  {DIM}Menyimpan file...{RST}\n")
    for i, size in enumerate(sizes, 1):
        chunk = domains[idx: idx + size]
        idx  += size
        fname = out_dir / f"{prefix}_part{str(i).zfill(padding)}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk) + "\n")
        written.append((fname, len(chunk)))
        print(f"\r{progress_bar(i, n_parts)}", end="", flush=True)

    elapsed = time.perf_counter() - t0
    print(f"\n\n  {C}─────────────────────────────────────────{RST}")
    print(f"  {W}HASIL PEMBAGIAN{RST}")
    print(f"  {C}─────────────────────────────────────────{RST}")

    for fname, count in written:
        bar = G + "■" * min(30, count * 30 // (base + 1)) + RST
        print(f"  {G}✓{RST}  {fname.name:<40} {W}{count:>6,}{RST} domain  {bar}")

    print(f"  {C}─────────────────────────────────────────{RST}")
    print(f"  Waktu proses : {Y}{elapsed*1000:.2f} ms{RST}")
    print(f"  Folder output: {W}{out_dir}{RST}")
    print(f"  {G}[✓] Selesai! {n_parts} file berhasil dibuat.{RST}")
    _pause()


def _pause():
    input(f"\n  {DIM}Tekan Enter untuk kembali ke menu...{RST}")


def main():
    while True:
        clear()
        banner()
        menu()
        choice = input(f"\n  {C}» {W}Pilih menu: {RST}").strip()

        if choice == "1":
            clear_duplicates()
        elif choice == "2":
            split_domains()
        elif choice == "0":
            clear()
            print(f"\n  {G}Terima kasih telah menggunakan {W}dnduplicate.id{G}!{RST}\n")
            sys.exit(0)
        else:
            print(f"  {R}[!] Pilihan tidak valid. Coba lagi.{RST}")
            time.sleep(1)


if __name__ == "__main__":
    main()
