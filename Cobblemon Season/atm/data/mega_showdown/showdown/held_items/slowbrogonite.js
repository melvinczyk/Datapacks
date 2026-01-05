{
    name: "Slowbrogonite",
    spritenum: -620,
    megaStone: "Slowbro-Mega-Galar",
    megaEvolves: ["Slowbro-Galar"],
    itemUser: ["Slowbro-Galar"],
    onTakeItem(item, source) {
        if (item.megaEvolves === source.baseSpecies.baseSpecies) return false;
        return true;
    },
    num: -760,
    gen: 6,
    isNonstandard: "Past"
}