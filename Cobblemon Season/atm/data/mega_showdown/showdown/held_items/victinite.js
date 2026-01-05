{
  name: "victinite",
  spritenum: 666,
  megaStone: "Victini-Mega",
  megaEvolves: ["Victini"],
  itemUser: ["Victini"],
  onTakeItem(item, source) {
    if (item.megaEvolves === source.baseSpecies.baseSpecies) return false;
    return true;
  },
  num: -999,
  gen: 5,
  isNonstandard: "Past",
}