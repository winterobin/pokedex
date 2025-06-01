import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, mo, pd


@app.cell
def _(pd):
    df = pd.read_csv("data/Pokemon.csv")
    return (df,)


@app.cell
def _(df, mo):
    # Crea il menu a tendina con i nomi dei Pokémon
    dropdown1 = mo.ui.dropdown.from_series(df["Type 1"], label="Scegli il Tipo 1 del Pokémon", searchable=True)
    dropdown2 = mo.ui.dropdown.from_series(df["Type 2"], label="Scegli il Tipo 2 del Pokémon", searchable=True)

    # Visualizza il menu
    dropdown1, dropdown2
    return dropdown1, dropdown2


@app.cell
def _(df, dropdown1, dropdown2):
    # Filtra il DataFrame in base alla selezione
    Tipo1 = dropdown1.value
    Tipo2 = dropdown2.value
    if not Tipo2:
        dati_pokemon = df[df["Type 1"] == Tipo1]
    else:
        dati_pokemon = df[(df["Type 1"] == Tipo1) & (df["Type 2"] == Tipo2)]
    return (dati_pokemon,)


@app.cell
def _(dati_pokemon):
    # Visualizza i dati del Pokémon selezionato
    dati_pokemon
    return


@app.cell
def _(alt, dati_pokemon):
    # Trasforma in long format
    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    df_stat = dati_pokemon[["Name"] + stats].melt(
        id_vars="Name", var_name="Stat", value_name="Value"
    )

    # Altair chart
    chart2 = (
        alt.Chart(df_stat)
        .mark_point()
        .encode(
            x=alt.X("Stat:N", sort=stats),
            y="Value:Q",
            color="Stat:N",
            tooltip=["Name:N", "Stat:N", "Value:Q"]
        )
        #.properties(title=f"Statistiche di {pokemon}")
    )

    chart2
    return


if __name__ == "__main__":
    app.run()
