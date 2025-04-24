# pokemon_test.py
from Gen3Save.pokemondata.Gen3Pokemon import Gen3Pokemon
from Gen3Save.pokemondata.Gen3Save import Gen3Save
import struct

# 3) Defina offsets relativos à Section 1 para cada grupo de jogos
VERSION_OFFSETS = {
    "RSE": 0x0238,  # Ruby/Sapphire/Emerald party offset :contentReference[oaicite:2]{index=2}
    "FRLG": 0x0038,  # FireRed/LeafGreen party offset :contentReference[oaicite:3]{index=3}
}


def find_section1_start(block: bytes) -> int:
    """Encontra o início da Section 1 (ID=1) dentro do bloco ativo de 57 344 bytes."""
    for i in range(14):
        sec = block[i * 4096 : (i + 1) * 4096]
        (sec_id,) = struct.unpack("<H", sec[4084:4086])
        if sec_id == 1:
            return i * 4096
    raise RuntimeError(
        "Section 1 não encontrada"
    )  # :contentReference[oaicite:4]{index=4}


def try_version(block: bytes, sect1: int, offset: int) -> bool:
    """Tenta ler Slot 1 de party; retorna True se checksum for válido."""
    start = sect1 + offset
    data100 = block[
        start : start + 100
    ]  # party Pokémon usa 100 bytes :contentReference[oaicite:5]{index=5}
    try:
        Gen3Pokemon(data100)
        return True
    except Exception:
        return False


def detect_gen3_version(block: bytes) -> str:
    """Retorna 'RSE' ou 'FRLG' conforme offset que validou checksum."""
    sect1 = find_section1_start(block)
    for ver, off in VERSION_OFFSETS.items():
        if try_version(block, sect1, off):
            return ver
    return "UNKNOWN"


def main():
    # Carrega o save e seleciona bloco ativo (feito internamente em Gen3Save)
    #save = Gen3Save("leaf_green.sav")
    # A própria Gen3Save carrega o bloco correto A ou B :contentReference[oaicite:6]{index=6}
    raw = open("leaf_green.sav", "rb").read()
    block = raw[0:57344] if True else raw  # placeholder, Gen3Save já faz

    vers = detect_gen3_version(block)
    print("Versão Gen3 detectada:", vers)


    save = Gen3Save('leaf_green.sav')
    print("TIME")
    for pkm in save.team:
        print(f"{pkm.species['name']}/{pkm.name} Level {pkm.level} - Location: ")

    # Imprimir a box
    print("")
    print(f"BOX 1 {len(save.boxes)}")
    for pkm in save.boxes:
        # print("Genero e nome")
        # print(f"{save.gender} - {pkm.trainer['name']}")
        print(f"{pkm.species['name']}/{pkm.name} Level {pkm.level}")

if __name__ == "__main__":
    main()
