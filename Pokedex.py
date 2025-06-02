import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import requests
    import yaml
    return alt, mo, pd, requests, yaml


@app.cell
def _(pd, requests, yaml):
    #df = pd.read_csv("data/Pokemon.csv")

    url = "https://raw.githubusercontent.com/pokemondb/database/refs/heads/master/data/pokemon-forms.yaml"

    response = requests.get(url)
    response.raise_for_status()  # solleva un errore se la richiesta fallisce

    yaml_text = response.text
    yaml_text = yaml_text.replace("type2: -", 'type2: ""')

    # Ora puoi fare il parsing in sicurezza
    data = yaml.safe_load(yaml_text)

    # Verifica i primi elementi
    #print(data)

    df = pd.DataFrame(data).T
    stats_df = df["stats"].apply(pd.Series)
    df = df.join(stats_df)
    df.drop(columns=['stats'], inplace=True)
    return (df,)


@app.cell
def _(df, mo):
    # Crea il menu a tendina con i nomi dei Pokémon
    dropdown1 = mo.ui.dropdown.from_series(df["type1"], label="Scegli il Tipo 1 del Pokémon", searchable=True)
    dropdown2 = mo.ui.dropdown.from_series(df["type2"], label="Scegli il Tipo 2 del Pokémon", searchable=True)

    # Visualizza il menu
    dropdown1, dropdown2
    return dropdown1, dropdown2


@app.cell
def _(df, dropdown1, dropdown2):
    # Filtra il DataFrame in base alla selezione
    Tipo1 = dropdown1.value
    Tipo2 = dropdown2.value
    if not Tipo2:
        dati_pokemon = df[df["type1"] == Tipo1]
    else:
        dati_pokemon = df[(df["type1"] == Tipo1) & (df["type2"] == Tipo2)]
    return (dati_pokemon,)


@app.cell
def _(df, mo):
    colonne_disponibili = df.columns.tolist()

    # Widget: elenco a crocette
    colonne_scelte = mo.ui.multiselect(
        options=colonne_disponibili,
        value=["pokemonid", "type1", "type2", "hp", "attack","defense","spatk","spdef","speed"],  # valori iniziali
        label="Scegli le colonne da visualizzare:"
    )

    colonne_scelte
    return (colonne_scelte,)


@app.cell
def _(colonne_scelte, dati_pokemon):
    dati_pokemon[colonne_scelte.value]
    return


@app.cell
def _(alt, dati_pokemon):
    # Trasforma in long format
    stats = ["hp", "attack", "defense", "spatk", "spdef", "speed"]
    df_stat = dati_pokemon[["pokemonid"] + stats].melt(
        id_vars="pokemonid", var_name="Stat", value_name="Value"
    )

    # Altair chart
    chart = (
        alt.Chart(df_stat)
        .mark_point()
        .encode(
            x=alt.X("Stat:N", sort=stats),
            y="Value:Q",
            color="Stat:N",
            tooltip=["pokemonid:N", "Stat:N", "Value:Q"]
        )
        #.properties(title=f"Statistiche di {pokemon}")
    )

    chart
    return


if __name__ == "__main__":
    app.run()
