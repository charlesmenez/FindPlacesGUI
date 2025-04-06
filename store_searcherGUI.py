import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import csv
import time
import re
from typing import List, Dict, Optional

API_KEY = ""

def geocodificar_endereco(endereco: str) -> str:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": endereco, "key": API_KEY}
    resposta = requests.get(url, params=params).json()
    if resposta.get("status") == "OK" and resposta.get("results"):
        local = resposta["results"][0]["geometry"]["location"]
        return f"{local['lat']},{local['lng']}"
    else:
        raise ValueError("Endereço não encontrado.")

def buscar_estabelecimentos(localizacao: str, termo: str, raio: int) -> List[Dict[str, Optional[str]]]:
    url_base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": localizacao,
        "radius": raio,
        "keyword": termo,
        "key": API_KEY
    }

    estabelecimentos = []
    while True:
        resposta = requests.get(url_base, params=params).json()
        if resposta.get("status") not in ["OK", "ZERO_RESULTS"]:
            raise Exception(f"Erro na busca: {resposta.get('status')}")

        for lugar in resposta.get("results", []):
            place_id = lugar.get("place_id")
            detalhes = buscar_detalhes_estabelecimento(place_id)
            if detalhes:
                estabelecimentos.append(detalhes)

        next_page_token = resposta.get("next_page_token")
        if next_page_token:
            time.sleep(2)
            params = {"pagetoken": next_page_token, "key": API_KEY}
        else:
            break

    return estabelecimentos

def buscar_detalhes_estabelecimento(place_id: str) -> Dict[str, Optional[str]]:
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website",
        "key": API_KEY
    }

    resposta = requests.get(url, params=params).json()
    dados = resposta.get("result", {})

    telefone = dados.get("formatted_phone_number")
    whatsapp_link = gerar_link_whatsapp(telefone) if telefone else ""

    return {
        "Nome": dados.get("name"),
        "Endereço": dados.get("formatted_address"),
        "Telefone": telefone,
        "Site": dados.get("website"),
        "WhatsApp": whatsapp_link
    }

def gerar_link_whatsapp(telefone: str) -> str:
    numero_limpo = re.sub(r"\D", "", telefone)
    if not numero_limpo.startswith("55"):
        numero_limpo = "55" + numero_limpo
    return f"https://wa.me/{numero_limpo}"

def salvar_em_csv(lista: List[Dict[str, Optional[str]]], arquivo: str) -> None:
    with open(arquivo, mode="w", newline="", encoding="utf-8") as f:
        campos = ["Nome", "Endereço", "Telefone", "Site", "WhatsApp"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for item in lista:
            writer.writerow(item)

# ----- INTERFACE GUI -----

def executar_busca():
    endereco = entry_endereco.get()
    termo = entry_termo.get()
    raio = entry_raio.get()
    nome_arquivo = entry_arquivo.get()

    if not nome_arquivo.endswith(".csv"):
        nome_arquivo += ".csv"

    if not endereco or not termo or not raio:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        raio = int(raio)
        status_text.set("Geocodificando endereço...")
        root.update()
        localizacao = geocodificar_endereco(endereco)

        status_text.set("Buscando estabelecimentos...")
        root.update()
        resultados = buscar_estabelecimentos(localizacao, termo, raio)

        status_text.set(f"Salvando {len(resultados)} resultados...")
        salvar_em_csv(resultados, nome_arquivo)

        status_text.set("✅ Busca concluída com sucesso!")
        messagebox.showinfo("Sucesso", f"{len(resultados)} resultados salvos em '{nome_arquivo}'.")

    except Exception as e:
        status_text.set("❌ Erro na execução.")
        messagebox.showerror("Erro", str(e))

# ----- Construção da Janela -----

root = tk.Tk()
root.title("🔍 Buscador Google Places")
root.geometry("500x400")

tk.Label(root, text="📍 Endereço:").pack()
entry_endereco = tk.Entry(root, width=50)
entry_endereco.pack()

tk.Label(root, text="🔎 Termo de busca:").pack()
entry_termo = tk.Entry(root, width=50)
entry_termo.pack()

tk.Label(root, text="📏 Raio (metros):").pack()
entry_raio = tk.Entry(root, width=50)
entry_raio.insert(0, "3000")
entry_raio.pack()

tk.Label(root, text="💾 Nome do arquivo CSV:").pack()
entry_arquivo = tk.Entry(root, width=50)
entry_arquivo.insert(0, "estabelecimentos.csv")
entry_arquivo.pack()

tk.Button(root, text="🚀 Iniciar Busca", command=executar_busca, bg="green", fg="white").pack(pady=10)

status_text = tk.StringVar()
status_text.set("Aguardando dados...")
tk.Label(root, textvariable=status_text, fg="blue").pack(pady=10)

root.mainloop()

