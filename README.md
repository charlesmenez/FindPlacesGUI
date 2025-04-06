# 🖼️ FindPlaces GUI – Buscador de Estabelecimentos com Interface Gráfica

Este aplicativo em Python permite buscar estabelecimentos próximos a um endereço, com base em um termo de pesquisa, utilizando a **Google Maps API** (Geocoding e Places). Ele possui uma interface gráfica amigável criada com **Tkinter**. Os resultados são exibidos na tela e também salvos em um arquivo `.csv`.

---

## 🎯 Funcionalidades

- Interface gráfica simples e intuitiva
- Busca de locais comerciais com base em endereço e raio
- Geração de links de WhatsApp a partir dos telefones encontrados
- Exportação para `.csv` com nome personalizado

---

## 🖥️ Pré-requisitos

- Python 3.7 ou superior
- Conta Google Cloud com:
  - Geocoding API ativada
  - Places API ativada
- Chave da API do Google Maps

---

---
## 📦 Criando Executável Exe
```bash
pip install pyinstaller
pyinstaller --name "FindPlacesGUI" --onefile --windowed store_searcherGUI.py
```
---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/store-searcher-gui.git
cd store-searcher-gui

pip install -r requirements.txt

