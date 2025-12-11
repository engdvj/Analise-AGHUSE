from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
from pathlib import Path
import subprocess
import json
import sys

# ======================================================================
# 0) Arquivo de LOG vindo do .bat
# ======================================================================
if len(sys.argv) < 2:
    print("[ERRO] Caminho do arquivo de log nao informado.")
    print("Uso: python openspeedtest_log.py CAMINHO_DO_ARQUIVO.txt")
    sys.exit(1)

LOG_FILE = Path(sys.argv[1])
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# URL do servidor interno PRODEB (OpenSpeedTest)
PRODEB_URL = "http://10.160.246.25/?Run=5"


# ======================================================================
# 1) PRODEB – OpenSpeedTest interno
# ======================================================================
def run_prodeb():
    print("=== PRODEB (OpenSpeedTest interno) ===")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"[PRODEB] Acessando {PRODEB_URL} ...")
        page.goto(PRODEB_URL)

        print("[PRODEB] Aguardando o teste terminar (ate 3 min)...")
        wait_js = """
        () => {
            const d = document.querySelector('#downResult');
            const u = document.querySelector('#upRestxt');
            const p = document.querySelector('#pingResult');
            const j = document.querySelector('#jitterDesk');
            if (!d || !u || !p || !j) return false;
            const get = el => (el.textContent || '').trim();
            const vals = [get(d), get(u), get(p), get(j)];
            return vals.every(v => v && v !== '---');
        }
        """

        try:
            page.wait_for_function(wait_js, timeout=180_000)  # 180s
        except PlaywrightTimeoutError:
            browser.close()
            print("[PRODEB][ERRO] Timeout: o teste nao terminou em 3 minutos.")
            return None

        def get_text(selector: str) -> str:
            txt = page.text_content(selector)
            return txt.strip() if txt else ""

        download = get_text("#downResult")
        upload = get_text("#upRestxt")
        ping = get_text("#pingResult")
        jitter = get_text("#jitterDesk")

        browser.close()

    print("[PRODEB] Resultados:")
    print(f"    Download: {download} Mbps")
    print(f"    Upload  : {upload} Mbps")
    print(f"    Ping    : {ping} ms")
    print(f"    Jitter  : {jitter} ms")

    return {
        "source": "PRODEB",
        "download": download,
        "upload": upload,
        "ping": ping,
        "jitter": jitter,
    }


# ======================================================================
# 2) Speedtest.net – usando speedtest-cli
# ======================================================================
def run_speedtest_net():
    print("=== Speedtest.net (speedtest-cli) ===")

    comandos = [
        ["speedtest-cli", "--json"],
        ["speedtest", "--json"],
    ]

    ultimo_erro = None

    for cmd in comandos:
        try:
            print(f"[Speedtest.net] Executando: {' '.join(cmd)}")
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )
        except FileNotFoundError as e:
            ultimo_erro = str(e)
            continue

        if proc.returncode != 0:
            ultimo_erro = proc.stderr
            continue

        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            ultimo_erro = f"Erro ao parsear JSON: {e}"
            continue

        download_bps = float(data.get("download", 0.0))
        upload_bps = float(data.get("upload", 0.0))
        ping_ms = float(data.get("ping", 0.0))

        download = round(download_bps / 1_000_000, 2)
        upload = round(upload_bps / 1_000_000, 2)
        ping = round(ping_ms, 2)

        print("[Speedtest.net] Resultados:")
        print(f"    Download: {download} Mbps")
        print(f"    Upload  : {upload} Mbps")
        print(f"    Ping    : {ping} ms")

        return {
            "source": "Speedtest.net",
            "download": f"{download}",
            "upload": f"{upload}",
            "ping": f"{ping}",
        }

    print("[Speedtest.net][ERRO] Nao consegui executar speedtest-cli / speedtest.")
    if ultimo_erro:
        print("Detalhe do ultimo erro:")
        print(ultimo_erro.strip())
    return None


# ======================================================================
# 3) Funções de escrita no mesmo arquivo
# ======================================================================
def append_section_titulo(titulo: str):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write("\n")
        f.write("=========================================================\n")
        f.write(f"{titulo}\n")
        f.write("=========================================================\n")


def salvar_resultado(result):
    if not result:
        return

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fonte = result["source"]
    download = result["download"]
    upload = result["upload"]
    ping = result["ping"]
    jitter = result.get("jitter")

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"DATA_HORA   : {agora}\n")
        f.write(f"FONTE       : {fonte}\n")
        f.write(f"DOWNLOAD    : {download} Mbps\n")
        f.write(f"UPLOAD      : {upload} Mbps\n")
        f.write(f"PING        : {ping} ms\n")
        if jitter is not None:
            f.write(f"JITTER      : {jitter} ms\n")
        f.write("---------------------------------------------------------\n\n")


# ======================================================================
# 4) Execução principal
# ======================================================================
def main():
    print(f"[INFO] Usando arquivo de log: {LOG_FILE}")

    append_section_titulo("[8/7] TESTE DE VELOCIDADE - PRODEB (OpenSpeedTest)")
    r1 = run_prodeb()
    salvar_resultado(r1)

    append_section_titulo("[9/7] TESTE DE VELOCIDADE - SPEEDTEST.NET")
    r2 = run_speedtest_net()
    salvar_resultado(r2)


if __name__ == "__main__":
    main()
