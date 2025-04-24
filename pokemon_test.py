# pokemon_test.py
from Gen3Save.pokemondata.Gen3Pokemon import Gen3Pokemon
from Gen3Save.pokemondata.Gen3Save import Gen3Save

def main():
    save = Gen3Save('leaf_green.sav')



    print("TIME")
    for pkm in save.team:
        print(f"{pkm.species['name']}/{pkm.name} Level {pkm.level}")

    # Imprimir a box
    print("")
    print(f"BOX 1 {len(save.boxes)}")
    for pkm in save.boxes:
        print("Genero e nome")
        print(f"{save.gender} - {pkm.trainer['name']}")
        print(f"{pkm.species['name']}/{pkm.name} Level {pkm.level}")

if __name__ == "__main__":
    main()
