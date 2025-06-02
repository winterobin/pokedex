# 🧬 Pokémon Stats Explorer with Marimo

This interactive app, built with [Marimo](https://github.com/marimo-team/marimo), allows users to explore Pokémon stats dynamically using dropdown filters and charts. It loads real-time data directly from the PokémonDB GitHub repository in YAML format and visualizes various attributes such as HP, Attack, Defense, and more.

---

## 🚀 Features

- 📥 **Live data loading** from the Pokémon database YAML file
- 🔍 **Interactive filtering** by Type 1 and Type 2 using dropdown menus
- 📊 **Dynamic visualization** of Pokémon base stats with Altair charts
- 📑 **Customizable data table** via column selection checkboxes
- ⚡ **No local dataset required** – everything loads automatically from the web

---

## 🖥️ Preview

![Preview Screenshot](https://github.com/yourusername/your-repo/assets/preview-placeholder.png)

---

## 📦 Requirements

- Python 3.8+
- marimo `>=0.13.15`
- pandas
- altair
- pyyaml
- requests

---

## 🛠️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/pokemon-marimo-explorer.git
cd pokemon-marimo-explorer
pip install -r requirements.txt