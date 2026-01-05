{
	name: "Lucarionite",
	spritenum: 594,
	megaStone: "Lucario-Mega",
	megaEvolves: ["Lucario", "Lucario-PMD-Scarf", "Lucario-PSMD-Scarf", "Lucario-Cafe-Costume", "Lucario-Captain-Costume", "Lucario-Chef-Costume", "Lucario-Concert-Costume", "Lucario-Costume_Party-Costume", "Lucario-Holiday-Costume", "Lucario-Martial_Arts-Costume" , "Lucario-Ruins-Costume" , "Lucario-Space-Costume"],
	itemUser: ["Lucario"],
	onTakeItem(item, source) {
		if (item.megaEvolves === source.baseSpecies.baseSpecies) return false;
		return true;
	},
	num: 673,
	gen: 6,
	isNonstandard: "Past",
}
