{
	name: "Mewtwonite Y",
	spritenum: 601,
	megaStone: "Mewtwo-Mega-Y",
	megaEvolves: ["Mewtwo","Mewtwo-Armored"],
	itemUser: ["Mewtwo"],
	onTakeItem(item, source) {
		if (item.megaEvolves === source.baseSpecies.baseSpecies) return false;
		return true;
	},
	num: 663,
	gen: 6,
	isNonstandard: "Past"
}
