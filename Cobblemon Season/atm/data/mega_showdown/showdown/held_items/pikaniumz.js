{
    name: "Pikanium Z",
    spritenum: 649,
    onTakeItem: false,
	onModifyAtkPriority: 1,
    onModifyAtk(atk, pokemon) {
      if (pokemon.baseSpecies.baseSpecies === "Pikachu") {
        return this.chainModify(2);
      }
    },
    onModifySpAPriority: 1,
    onModifySpA(spa, pokemon) {
      if (pokemon.baseSpecies.baseSpecies === "Pikachu") {
        return this.chainModify(2);
      }
    },	
    zMove: "Catastropika",
    zMoveFrom: "Volt Tackle",
    itemUser: ["Pikachu"],
    num: 794,
    gen: 7,
    isNonstandard: "Past"
}