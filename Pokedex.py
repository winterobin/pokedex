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
    url = "https://raw.githubusercontent.com/pokemondb/database/refs/heads/master/data/pokemon-forms.yaml"

    response = requests.get(url)
    response.raise_for_status()

    yaml_text = response.text
    yaml_text = yaml_text.replace("type2: -", 'type2: ""')

    # parsing
    data = yaml.safe_load(yaml_text)

    df = pd.DataFrame(data).T
    stats_df = df["stats"].apply(pd.Series)
    df = df.join(stats_df)
    df.drop(columns=['stats'], inplace=True)

    df = df.reset_index()
    return (df,)


@app.cell
def _(df, mo):
    # Create the menu
    dropdownname = mo.ui.dropdown.from_series(df["index"], label="Choose the first Pokémon name", searchable=True)
    dropdownname2 = mo.ui.dropdown.from_series(df["index"], label="Choose the second Pokémon name", searchable=True)
    dropdown1 = mo.ui.dropdown.from_series(df["type1"], label="Choose the first Type", searchable=True)
    dropdown2 = mo.ui.dropdown.from_series(df["type2"], label="Choose the second Type", searchable=True)

    # Show the menu
    mo.md("""Insert the first pokemon name, if you want to visualize its stats  
    Insert both the first and second pokemon names, if you want to confront their stats  
    Leave the name fields empty and insert type 1 and/or type 2, to visualize the family stats"""), dropdownname, dropdownname2, dropdown1, dropdown2
    return dropdown1, dropdown2, dropdownname, dropdownname2


@app.cell
def _(df, dropdown1, dropdown2, dropdownname, dropdownname2):
    # DataFrame filtering
    Name = dropdownname.value
    Name2 = dropdownname2.value
    Type1 = dropdown1.value
    Type2 = dropdown2.value
    if Name and not Name2 and not Type1 and not Type2:
        pokemon_data = df[df["index"] == Name]
    if Name and Name2 and not Type1 and not Type2:
        pokemon_data = df[(df["index"] == Name) | (df["index"] == Name2)]
    if not Name and Type1:
        pokemon_data = df[df["type1"] == Type1]
    if not Name and Type1 and Type2:
        pokemon_data = df[(df["type1"] == Type1) & (df["type2"] == Type2)]
    if not Name and not Name2 and not Type1 and not Type2:
        pokemon_data = df
    return (pokemon_data,)


@app.cell
def _(df, mo):
    available_columns = df.columns.tolist()

    # Widget: elenco a crocette
    chosen_columns = mo.ui.multiselect(
        options=available_columns,
        value=["index", "formid", "type1", "type2", "hp", "attack","defense","spatk","spdef","speed"],  # starting values
        label="Choose the columns to show:"
    )

    chosen_columns
    return (chosen_columns,)


@app.cell
def _(chosen_columns, pokemon_data):
    pokemon_data[chosen_columns.value]
    return


@app.cell
def _(alt, pokemon_data):
    # Graphs

    stats = ["hp", "attack", "defense", "spatk", "spdef", "speed"]
    df_stat = pokemon_data[["index"] + stats].melt(
        id_vars="index", var_name="Stat", value_name="Value"
    )

    if len(pokemon_data) == 1:
        chart = (
            alt.Chart(df_stat)
            .mark_bar()
            .encode(
                y=alt.Y("Stat:N", sort=stats),
                x=alt.X("Value:Q").scale(domain=(0, 255)),
                color=alt.Color("Stat:N", title="Pokémon", sort=["hp", "attack","defense", "spatk","spdef", "speed"]),
                tooltip=["index:N", "Stat:N", "Value:Q"]
            )
        )

    if len(pokemon_data) == 2:
        df_stat["Stat_Pokemon"] = df_stat["Stat"] + " - " + df_stat["index"]
        ordered_stats = df_stat["Stat_Pokemon"].tolist()

        chart = (
            alt.Chart(df_stat)
            .mark_bar()
            .encode(
                y=alt.Y("Stat_Pokemon:N", sort=ordered_stats, title=""),
                x=alt.X("Value:Q", scale=alt.Scale(domain=(0, 255))),
                color=alt.Color("Stat:N", title="Pokémon", sort=["hp", "attack","defense", "spatk","spdef", "speed"]),
                tooltip=["Stat:N", "index:N", "Value:Q"]
            )
        )

    if len(pokemon_data) >= 3:
        # Altair chart
        chart = (
            alt.Chart(df_stat)
            .mark_circle()
            .encode(
                x=alt.X("Stat:N", sort=stats),
                y=alt.Y("Value:Q").scale(domain=(0, 255)),
                xOffset="jitter:Q",
                color=alt.Color("Stat:N", title="Pokémon", sort=["hp", "attack","defense", "spatk","spdef", "speed"]),
                tooltip=["index:N", "Stat:N", "Value:Q"]
            ).transform_calculate(jitter="sqrt(-2*log(random()))*cos(2*PI*random()) * 0.2")
        
        )

    chart


    return


if __name__ == "__main__":
    app.run()
