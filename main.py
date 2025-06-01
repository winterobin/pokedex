import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#stampa i primi 5 record del dataset

df = pd.read_csv("data/Pokemon.csv")
print(df.head())

#distibuzione del tipo primario dei Pokémon

sns.countplot(data=df, x="Type 1", order=df["Type 1"].value_counts().index)
plt.xticks(rotation=45)
plt.title("Distribuzione del tipo primario dei Pokémon")
plt.tight_layout()
#plt.savefig("plots/distribuzione_tipologie.png")
plt.show()

#analisi del power creep

df["Total"] = df[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].sum(axis=1)

sns.boxplot(data=df, x="Generation", y="Total")
plt.title("Distribuzione della potenza totale per generazione")
plt.show()