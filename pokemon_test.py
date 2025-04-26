
from Gen3Pokemon import Gen3Pokemon
from Gen3Save import Gen3Save
import struct

POKEMONS_PER_BOX = 30
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
    ) 


def try_version(block: bytes, sect1: int, offset: int) -> bool:
    """Tenta ler Slot 1 de party; retorna True se checksum for válido."""
    start = sect1 + offset
    data100 = block[
        start : start + 100
    ] 
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
    raw = open("assets/sapphire.sav", "rb").read()
    block = raw[0:57344] if True else raw

    vers = detect_gen3_version(block)
    print("Versão Gen3 detectada:", vers)


    save = Gen3Save('assets/sapphire.sav')
    print()
    print("TIME")
    for pkm in save.team:
        print(f"  {pkm.species['name']}/{pkm.name} Level {pkm.level} - Location: {pkm.location} Nature: {pkm.nature} Moves:{pkm.moves} ")
        
    print()
    total = len(save.boxes)
    print(f"Total de Pokémon em todas as boxes: {total}\n")

    # num_boxes = (total + POKEMONS_PER_BOX - 1) // POKEMONS_PER_BOX
    # for box_idx in range(num_boxes):
    #     start = box_idx * POKEMONS_PER_BOX
    #     end   = start + POKEMONS_PER_BOX
    #     box = save.boxes[start:end]
        
    #     print(f"BOX {box_idx+1} ({len(box)} slots ocupados)")
    #     for pkm in box:
    #         print(f"  {pkm.species['name']}/{pkm.name} Level {pkm.level} Nature: {pkm.nature} Moves:{pkm.moves}")
    #     print() 

if __name__ == "__main__":
    main()
