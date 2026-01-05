{
    name: "Pikashunium Z",
    spritenum: 659,
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
    zMove: "10,000,000 Volt Thunderbolt",
    zMoveFrom: "Thunderbolt",
    itemUser: ["Pikachu-Original", "Pikachu-Hoenn", "Pikachu-Sinnoh", "Pikachu-Unova", "Pikachu-Kalos", "Pikachu-Alola", "Pikachu-Partner"],
    num: 836,
    isNonstandard: "Past",
    gen: 7
}