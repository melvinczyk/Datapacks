{
		name: "Shadow Mewtwonite Y",
		spritenum: 601,
		megaStone: "Mewtwo-Shadow-Mega-Y",
		megaEvolves: ["Mewtwo-Shadow"],
		itemUser: ["Mewtwo-Shadow"],
		onTakeItem(item, source) {
			if (item.megaEvolves === source.baseSpecies.baseSpecies) return false;
			return true;
		},
		num: -663,
		gen: 6,
		isNonstandard: "Past"
}