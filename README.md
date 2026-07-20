Commandstone is an offline reference and command builder that covers BOTH Minecraft editions — Java and Bedrock. It searches commands, attributes, mobs, effects, enchantments, particles, sounds, biomes, blocks and items in one place.

Java ⇄ Bedrock
Use the edition button in the top-right corner (or View › Switch edition) to flip between Java and Bedrock. The whole app adapts to the active edition:
  •  Commands — Java-only commands (like /attribute, /function, /datapack, /tick) are hidden in Bedrock, and Bedrock-only commands (like /camera, /mobevent, /replaceitem, /allowlist, /music) appear instead.
  •  Gamerules — Java uses snake_case (keep_inventory) while Bedrock uses camelCase (keepInventory); the gamerule builder swaps its list to match.
  •  Syntax — differences are handled for you, e.g. /effect give (Java) vs /effect (Bedrock), the /playsound source argument, particle arguments, and gamemode numbers (0/1/2).
  •  Selectors — sort options adjust per edition.
Attributes are a Java-only system, so that category is empty in Bedrock.

Search & filter
Type in the search box (Ctrl+F jumps to it). Use the Type dropdown to focus a category: Commands, Attributes, Mobs, Effects, Enchantments, Particles, Sounds, Biomes, Blocks or Items. Toggle ★ Favorites to show only starred entries. Big lists show the first 250 matches — refine your search to see the rest.

Build & copy
Click any entry to open its builder on the right. Fields update the preview live; press Copy command to send it to your clipboard. Every kind builds the right command automatically — a block becomes /setblock (or /fill or /give), an item /give, an effect /effect, an enchant /enchant, a mob /summon, a biome /locate, and so on.

Smart fields (searchable)
ID and Target fields have a built-in search-as-you-type dropdown. Start typing an Item, Block, Entity, Effect or Enchantment ID and matching options appear below the box — click one, or use ↑/↓ and Enter, to fill it in. You can still type any value by hand.
Target fields suggest the common selectors with a short note on each: @p (nearest player), @a (all players), @r (random player), @s (yourself), @e (all entities), plus filtered examples like @e[distance=..10] or @a[gamemode=survival]. Only the selector is inserted — the description is just a hint. You can search by meaning too (type “gamemode” or “within” to find the matching selectors).

Favorites & history
Click the ☆ star on any entry to favorite it; the ★ Favorites filter shows just those. Every command you copy is saved in History (Edit › History), where you can re-copy or clear it.

Sequences & .mcfunction export
Use “Add to sequence” on any command to stage several together. Open the Sequence builder (top-right or Edit menu) to reorder-by-removing, copy all, or export them as a .mcfunction file (leading slashes are stripped, one command per line) via the button there or File › Export.

Special builders
•  /execute has a stackable builder — tick the subcommands you need (as, at, positioned, if block, if entity, and more) and they chain in order before your run command.
•  Target selector — search “selector” to build an @e[type=…,distance=…,limit=…,sort=…] argument and copy it.
•  Command block helper — on any command, use “▦ Command block” to copy it without the leading slash (paste-ready into a command block) or grab a /give command-block item.

Themes, keyboard & saved settings
Switch dark/light with the top-right toggle or the View menu. Keyboard: Ctrl+F focus search  ·  ↑/↓ move through results  ·  Ctrl+C copy the current command. Your theme, edition, window size, favorites, history and sequence are saved automatically in commandstone_settings.json next to the app.

Good to know
Data reflects Java 26.2 and Bedrock 26.33. The block and item lists cover the common several-hundred IDs rather than the entire registry, and a few IDs differ between editions. Minecraft changes fast — in-game tab-completion is always the final word for your exact version.

