{
    name: "Mewtwonite X",
    spritenum: 600,
    megaStone: "Mewtwo-Mega-X",
    megaEvolves: ["Mewtwo","Mewtwo-Armored"],
    itemUser: ["Mewtwo"],
    onTakeItem(item, source) {
        if (item.megaEvolves === source.baseSpecies.baseSpecies) return false;
        return true;
    },
    num: 662,
    gen: 6,
    isNonstandard: "Past"
}
