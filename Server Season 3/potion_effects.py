import re

def extract_damage(text):
    # Regex pattern to match the command block with weapon damage
    damage_pattern = r'''
    \{
\s+command:\s+"\/attribute @s hoths_jeg_attributes:wood_sword base set 25\.25"
\s+elevate_perms:\s+true
\s+icon:\s+\{
\s+Count:\s+1
\s+id:\s+"minecraft:wooden_sword"
\s+tag:\s+\{
\s+Damage:\s+0
\s+\}
\s+\}
\s+id:\s+"3B6FB2C4A2F659A3"
\s+title:\s+"\+0\.25 WOOD SWORD Damage"
\s+type:\s+"command"
\s+\}
    '''
    
    # Using re.DOTALL to match across multiple lines
    match = re.search(damage_pattern, text, re.DOTALL | re.VERBOSE)

    # Print out the match to debug
    if match:
        print("Match found!")
        print(f"Weapon name: {match.group(1)}")
        print(f"Damage: {match.group(2)}")
        return {
            'weapon_name': match.group(1),
            'damage': float(match.group(2))
        }
    else:
        print("No match found.")
        return None

# Example usage
wood_damage = '''
{
    command: "/attribute @s hoths_jeg_attributes:wood_sword base set 25.25"
    elevate_perms: true
    icon: {
        Count: 1
        id: "minecraft:wooden_sword"
        tag: {
            Damage: 0
        }
    }
    id: "3B6FB2C4A2F659A3"
    title: "+0.25 WOOD SWORD Damage"
    type: "command"
}
'''

# Call the function and print the result
result = extract_damage(wood_damage)
if result:
    print(result)
else:
    print("No result.")
