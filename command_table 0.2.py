#!/usr/bin/env python3
"""
Commandstone - Minecraft Java Edition command reference & builder.

Version 1.0
Created by Michael van der Meijden.

A single-window desktop app (Tkinter, standard library only).
Search on the left; click any command, attribute, or mob and its builder
opens on the right with a live, copyable command.

Run:   python command_table.py    (Windows)
       python3 command_table.py   (macOS / Linux)
Needs: Python 3.8+  (Tkinter ships with the standard python.org installer)
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

# ============================================================================
# Theme  (two palettes; set_theme swaps the module-level colors live)
# ============================================================================
THEMES = {
    "dark": dict(
        BG="#0f1319", SIDEBAR="#141a22", CARD="#1a212b", CARD_HOV="#222b38",
        CARD_SEL="#26313f", FIELD="#0f1319", BORDER="#2a3542",
        TEXT="#e9eef4", TEXT_DIM="#95a3b4", TEXT_FAINT="#5d6b7c",
        ACCENT="#57d364", ACCENT_INK="#06210c", ACCENT_HOV="#6ee27a", CODE="#8fe3ff",
        CMD_CAT_COLOR={"Items": "#f0c14b", "Entities": "#7ee787", "World": "#7fb3c9",
                       "Player": "#58c4dd", "Communication": "#c792ea", "Server": "#e5735b",
                       "Admin": "#e39a4a"},
        ENT_CAT_COLOR={"Hostile": "#e5735b", "Neutral": "#e0b34a",
                       "Passive": "#7ee787", "Boss": "#c792ea"},
        ATTR_COLOR="#c792ea",
    ),
    "light": dict(
        BG="#eef1f6", SIDEBAR="#e3e8f0", CARD="#ffffff", CARD_HOV="#eef3f9",
        CARD_SEL="#dbe8f6", FIELD="#ffffff", BORDER="#ccd5e0",
        TEXT="#1b2028", TEXT_DIM="#55606f", TEXT_FAINT="#8b97a6",
        ACCENT="#41b551", ACCENT_INK="#06210c", ACCENT_HOV="#57c866", CODE="#0e6ea6",
        CMD_CAT_COLOR={"Items": "#b07d0a", "Entities": "#2e9e44", "World": "#3a7ca5",
                       "Player": "#1493b8", "Communication": "#8a4fd0", "Server": "#cc4a35",
                       "Admin": "#c8791f"},
        ENT_CAT_COLOR={"Hostile": "#cc4a35", "Neutral": "#b07d0a",
                       "Passive": "#2e9e44", "Boss": "#8a4fd0"},
        ATTR_COLOR="#8a4fd0",
    ),
}

# Module-level colors (populated by set_theme). Declared here for clarity.
BG = SIDEBAR = CARD = CARD_HOV = CARD_SEL = FIELD = BORDER = ""
TEXT = TEXT_DIM = TEXT_FAINT = ACCENT = ACCENT_INK = ACCENT_HOV = CODE = ""
CMD_CAT_COLOR = ENT_CAT_COLOR = {}
ATTR_COLOR = ""


def set_theme(name):
    global BG, SIDEBAR, CARD, CARD_HOV, CARD_SEL, FIELD, BORDER
    global TEXT, TEXT_DIM, TEXT_FAINT, ACCENT, ACCENT_INK, ACCENT_HOV, CODE
    global CMD_CAT_COLOR, ENT_CAT_COLOR, ATTR_COLOR
    t = THEMES[name]
    BG, SIDEBAR, CARD, CARD_HOV = t["BG"], t["SIDEBAR"], t["CARD"], t["CARD_HOV"]
    CARD_SEL, FIELD, BORDER = t["CARD_SEL"], t["FIELD"], t["BORDER"]
    TEXT, TEXT_DIM, TEXT_FAINT = t["TEXT"], t["TEXT_DIM"], t["TEXT_FAINT"]
    ACCENT, ACCENT_INK, ACCENT_HOV, CODE = t["ACCENT"], t["ACCENT_INK"], t["ACCENT_HOV"], t["CODE"]
    CMD_CAT_COLOR, ENT_CAT_COLOR, ATTR_COLOR = t["CMD_CAT_COLOR"], t["ENT_CAT_COLOR"], t["ATTR_COLOR"]


set_theme("dark")

APP_NAME = "Commandstone"
APP_VERSION = "1.0"
APP_AUTHOR = "Michael van der Meijden"
APP_TAGLINE = "A searchable reference & command builder for Minecraft: Java Edition."


def pick(families, *cands, default="TkDefaultFont"):
    for c in cands:
        if c in families:
            return c
    return default


# ============================================================================
# DATA  (current Java Edition, 26.x)
# ============================================================================
# command: id, name, syntax, desc, cat
COMMANDS = [
    ("give", "/give", "/give <target> <item>[components] [count]", "Gives an item stack to a player (items use [component] data).", "Items"),
    ("clear", "/clear", "/clear [target] [item] [maxCount]", "Clears items from a player's inventory.", "Items"),
    ("item", "/item", "/item replace|modify entity|block <target> <slot> ...", "Replaces or modifies items in inventories and containers.", "Items"),
    ("enchant", "/enchant", "/enchant <target> <enchantment> [level]", "Adds an enchantment to the targeted entity's held item.", "Items"),
    ("loot", "/loot", "/loot <target> <source>", "Drops or gives loot generated from a loot table.", "Items"),
    ("recipe", "/recipe", "/recipe give|take <target> <recipe|*>", "Gives or takes known recipes for a player.", "Items"),
    ("summon", "/summon", "/summon <entity> [x y z] [nbt]", "Spawns an entity at a given position.", "Entities"),
    ("kill", "/kill", "/kill [target]", "Kills entities instantly.", "Entities"),
    ("data", "/data", "/data get|merge|modify|remove block|entity|storage ...", "Gets, merges, modifies or removes NBT data.", "Entities"),
    ("attribute", "/attribute", "/attribute <target> <attribute> get|base|modifier ...", "Queries or modifies an entity attribute.", "Entities"),
    ("damage", "/damage", "/damage <target> <amount> [type] [at|by ...]", "Deals a set amount of damage to an entity.", "Entities"),
    ("ride", "/ride", "/ride <target> mount|dismount [vehicle]", "Mounts or dismounts one entity onto another.", "Entities"),
    ("rotate", "/rotate", "/rotate <target> <rotation|facing>", "Rotates an entity to face a direction or target.", "Entities"),
    ("tag", "/tag", "/tag <target> add|remove|list [name]", "Adds, removes or lists custom entity tags.", "Entities"),
    ("spreadplayers", "/spreadplayers", "/spreadplayers <center> <spread> <range> [teams] <targets>", "Teleports entities to random spread-out spots.", "Entities"),
    ("teleport", "/teleport (/tp)", "/teleport <target> <destination|x y z> [rotation|facing]", "Teleports entities to a location, entity, or facing.", "World"),
    ("setblock", "/setblock", "/setblock <x y z> <block> [destroy|keep|replace]", "Changes a single block to another block.", "World"),
    ("fill", "/fill", "/fill <from> <to> <block> [mode] [filter]", "Fills a region with a specified block.", "World"),
    ("clone", "/clone", "/clone <begin> <end> <destination> [mode]", "Copies blocks from one region to another.", "World"),
    ("fillbiome", "/fillbiome", "/fillbiome <from> <to> <biome> [replace <filter>]", "Sets the biome for blocks within a region.", "World"),
    ("locate", "/locate", "/locate structure|biome|poi <id>", "Finds the nearest structure, biome, or point of interest.", "World"),
    ("place", "/place", "/place feature|jigsaw|structure|template ...", "Places a configured feature, structure, or template.", "World"),
    ("worldborder", "/worldborder", "/worldborder add|set|center|damage|warning|get <args>", "Manages the world border.", "World"),
    ("forceload", "/forceload", "/forceload add|remove|query <from> [to]", "Forces chunks to stay loaded.", "World"),
    ("setworldspawn", "/setworldspawn", "/setworldspawn [x y z] [angle]", "Sets the world spawn point.", "World"),
    ("time", "/time", "/time set|add|query <value>", "Changes or queries the day-night cycle.", "World"),
    ("weather", "/weather", "/weather clear|rain|thunder [duration]", "Sets the weather.", "World"),
    ("seed", "/seed", "/seed", "Displays the world seed.", "World"),
    ("gamemode", "/gamemode", "/gamemode <survival|creative|adventure|spectator> [target]", "Sets a player's game mode.", "Player"),
    ("defaultgamemode", "/defaultgamemode", "/defaultgamemode <mode>", "Sets the default game mode for new players.", "Player"),
    ("effect", "/effect", "/effect give|clear <target> [effect] [sec] [amp] [hideParticles]", "Adds or removes a status effect.", "Player"),
    ("xp", "/experience (/xp)", "/experience add|set|query <target> <amount> [points|levels]", "Adds, sets or queries player experience.", "Player"),
    ("spawnpoint", "/spawnpoint", "/spawnpoint [target] [x y z] [angle]", "Sets a player's personal spawn point.", "Player"),
    ("spectate", "/spectate", "/spectate [target] [player]", "Makes a spectator spectate an entity.", "Player"),
    ("title", "/title", "/title <target> title|subtitle|actionbar|clear|reset|times ...", "Controls text shown on player screens.", "Communication"),
    ("tellraw", "/tellraw", "/tellraw <target> <json>", "Sends a JSON-formatted message to players.", "Communication"),
    ("say", "/say", "/say <message>", "Broadcasts a message to all players.", "Communication"),
    ("msg", "/msg (/tell, /w)", "/msg <target> <message>", "Sends a private message to a player.", "Communication"),
    ("teammsg", "/teammsg (/tm)", "/teammsg <message>", "Sends a message to your team only.", "Communication"),
    ("me", "/me", "/me <action>", "Broadcasts an action-style message about yourself.", "Communication"),
    ("playsound", "/playsound", "/playsound <sound> <source> <target> [pos] [vol] [pitch] [min]", "Plays a sound audible to targets.", "Communication"),
    ("stopsound", "/stopsound", "/stopsound <target> [source] [sound]", "Stops a playing sound for targets.", "Communication"),
    ("particle", "/particle", "/particle <name> [pos] [delta] [speed] [count] [mode] [viewers]", "Spawns particle effects.", "Communication"),
    ("bossbar", "/bossbar", "/bossbar add|remove|set|get|list <id> <args>", "Creates and manages custom boss bars.", "Communication"),
    ("gamerule", "/gamerule", "/gamerule <rule> [value]", "Sets or queries a game rule (snake_case names in 26.x).", "Server"),
    ("difficulty", "/difficulty", "/difficulty <peaceful|easy|normal|hard>", "Sets the game difficulty.", "Server"),
    ("scoreboard", "/scoreboard", "/scoreboard objectives|players <args>", "Manages scoreboard objectives, scores and display.", "Server"),
    ("team", "/team", "/team add|remove|empty|join|leave|list|modify <args>", "Manages teams and team membership.", "Server"),
    ("execute", "/execute", "/execute <subcommand...> run <command>", "Chains conditions and modifiers before running a command.", "Server"),
    ("function", "/function", "/function <namespace:path> [args]", "Runs a function defined in a datapack.", "Server"),
    ("schedule", "/schedule", "/schedule function <name> <time> [append|replace]", "Delays execution of a function.", "Server"),
    ("datapack", "/datapack", "/datapack enable|disable|list <name>", "Manages loaded datapacks.", "Server"),
    ("advancement", "/advancement", "/advancement grant|revoke <target> everything|only|from|through|until ...", "Grants or revokes advancements.", "Server"),
    ("trigger", "/trigger", "/trigger <objective> [add|set <value>]", "Sets a trigger-type objective (usable by non-ops).", "Server"),
    ("tick", "/tick", "/tick query|rate|step|sprint|freeze|unfreeze <args>", "Controls the game tick rate: speed up, slow, freeze or step.", "Server"),
    ("random", "/random", "/random value|roll|reset <args>", "Rolls or seeds random values for use in commands.", "Server"),
    ("return", "/return", "/return <value> | run <command> | fail", "Returns a value early from a function.", "Server"),
    ("reload", "/reload", "/reload", "Reloads datapacks (functions, loot tables, etc.).", "Server"),
    ("debug", "/debug", "/debug start|stop|function <args>", "Starts/stops a profiling report or traces a function.", "Server"),
    ("transfer", "/transfer", "/transfer <hostname> [port] [players]", "Transfers players to another server.", "Server"),
    ("publish", "/publish", "/publish [allowCommands] [gamemode] [port]", "Opens a singleplayer world to LAN.", "Server"),
    ("help", "/help", "/help [command]", "Lists commands or shows usage for one.", "Server"),
    ("op", "/op", "/op <player>", "Grants operator status to a player.", "Admin"),
    ("deop", "/deop", "/deop <player>", "Revokes operator status.", "Admin"),
    ("whitelist", "/whitelist", "/whitelist add|remove|on|off|list|reload [player]", "Manages the server whitelist.", "Admin"),
    ("ban", "/ban", "/ban <player> [reason]", "Adds a player to the server ban list.", "Admin"),
    ("ban-ip", "/ban-ip", "/ban-ip <address|player> [reason]", "Bans an IP address from the server.", "Admin"),
    ("banlist", "/banlist", "/banlist [players|ips]", "Lists banned players or IPs.", "Admin"),
    ("pardon", "/pardon", "/pardon <player>", "Removes a player from the ban list.", "Admin"),
    ("pardon-ip", "/pardon-ip", "/pardon-ip <address>", "Removes an IP from the ban list.", "Admin"),
    ("kick", "/kick", "/kick <player> [reason]", "Removes a player from the server.", "Admin"),
    ("list", "/list", "/list [uuids]", "Lists online players.", "Admin"),
    ("setidletimeout", "/setidletimeout", "/setidletimeout <minutes>", "Sets how long before idle players are kicked.", "Admin"),
    ("save-all", "/save-all", "/save-all [flush]", "Saves the server world to disk.", "Admin"),
    ("save-off", "/save-off", "/save-off", "Disables automatic world saving.", "Admin"),
    ("save-on", "/save-on", "/save-on", "Re-enables automatic world saving.", "Admin"),
    ("stop", "/stop", "/stop", "Stops the server.", "Admin"),
    ("perf", "/perf", "/perf start|stop", "Captures a 10-second performance/debug report.", "Admin"),
    ("jfr", "/jfr", "/jfr start|stop", "Starts/stops a Java Flight Recorder profiling run.", "Admin"),
]

# attribute: id (flattened), default, min, max, desc
ATTRIBUTES = [
    ("armor", 0, 0, 30, "Armor points reducing incoming damage."),
    ("armor_toughness", 0, 0, 20, "Reduces the effect of high-damage hits against armor."),
    ("attack_damage", 1, 0, 2048, "Base melee attack damage."),
    ("attack_knockback", 0, 0, 5, "Extra knockback dealt by melee attacks."),
    ("attack_speed", 4, 0, 1024, "Attacks per second for the wielder."),
    ("block_break_speed", 1, 0, 1024, "Multiplier for how fast a player breaks blocks."),
    ("block_interaction_range", 4.5, 0, 64, "Max distance for interacting with blocks."),
    ("burning_time", 1, 0, 1024, "Multiplier for how long the entity stays on fire."),
    ("entity_interaction_range", 3, 0, 64, "Max distance for interacting with entities."),
    ("explosion_knockback_resistance", 0, 0, 1, "Fraction of explosion knockback ignored (0-1)."),
    ("fall_damage_multiplier", 1, 0, 100, "Multiplier applied to fall damage taken."),
    ("flying_speed", 0.4, 0, 1024, "Flight speed multiplier (e.g. parrots)."),
    ("follow_range", 32, 0, 2048, "Distance at which mobs can target/track an entity."),
    ("gravity", 0.08, -1, 1, "Downward acceleration applied each tick."),
    ("jump_strength", 0.42, 0, 32, "Jump height strength (horses jump higher)."),
    ("knockback_resistance", 0, 0, 1, "Fraction of knockback ignored (0-1)."),
    ("luck", 0, -1024, 1024, "Affects loot-table rolls for the entity."),
    ("max_absorption", 0, 0, 2048, "Maximum absorption (yellow) hearts allowed."),
    ("max_health", 20, 1, 1024, "Maximum health of a living entity."),
    ("mining_efficiency", 0, 0, 1024, "Flat mining-speed bonus, mainly from tools."),
    ("movement_efficiency", 0, 0, 1, "How well the entity moves over difficult terrain."),
    ("movement_speed", 0.1, 0, 1024, "Base ground movement speed."),
    ("oxygen_bonus", 0, 0, 1024, "Extends time before an entity starts drowning."),
    ("safe_fall_distance", 3, -1024, 1024, "Blocks an entity can fall before taking damage."),
    ("scale", 1, 0.0625, 16, "Overall visual and hitbox scale of the entity."),
    ("sneaking_speed", 0.3, 0, 1, "Movement-speed multiplier while sneaking."),
    ("spawn_reinforcements", 0, 0, 1, "Chance a zombie calls zombie reinforcements."),
    ("step_height", 0.6, 0, 10, "Height an entity can step up without jumping."),
    ("submerged_mining_speed", 0.2, 0, 20, "Mining-speed multiplier while underwater."),
    ("sweeping_damage_ratio", 0, 0, 1, "Fraction of damage dealt by a sweep attack."),
    ("water_movement_efficiency", 0, 0, 1, "How well the entity moves through water."),
]

# entity: id, category, hp, attack, desc
ENTITIES = [
    ("zombie", "Hostile", "20", "3", "Basic undead that burns in daylight."),
    ("skeleton", "Hostile", "20", "bow", "Ranged undead; burns in daylight."),
    ("creeper", "Hostile", "20", "explosion", "Silent mob that explodes near a target."),
    ("spider", "Neutral", "16", "2", "Climbs walls; hostile in darkness."),
    ("enderman", "Neutral", "40", "7", "Teleports; hostile when looked at."),
    ("witch", "Hostile", "26", "potions", "Throws harmful splash potions."),
    ("slime", "Hostile", "1-16", "size", "Splits into smaller slimes on death."),
    ("phantom", "Hostile", "20", "2", "Spawns near players who haven't slept."),
    ("drowned", "Hostile", "20", "3", "Underwater zombie; can throw tridents."),
    ("pillager", "Hostile", "24", "crossbow", "Crossbow raider from patrols/outposts."),
    ("vindicator", "Hostile", "24", "13", "Axe raider with strong melee."),
    ("blaze", "Hostile", "20", "fireball", "Flying Nether mob that shoots fireballs."),
    ("ghast", "Hostile", "10", "fireball", "Large flyer firing explosive fireballs."),
    ("guardian", "Hostile", "30", "6", "Aquatic mob with a laser beam."),
    ("elder_guardian", "Hostile", "80", "8", "Monument boss; inflicts Mining Fatigue."),
    ("silverfish", "Hostile", "8", "1", "Hides in infested stone blocks."),
    ("magma_cube", "Hostile", "1-16", "size", "Nether slime; jumps and splits."),
    ("husk", "Hostile", "20", "3", "Desert zombie; doesn't burn in daylight."),
    ("stray", "Hostile", "20", "bow", "Cold skeleton; arrows cause Slowness."),
    ("wither_skeleton", "Hostile", "20", "8", "Melee inflicts the Wither effect."),
    ("piglin_brute", "Hostile", "50", "13", "Always-hostile axe piglin variant."),
    ("hoglin", "Hostile", "40", "6", "Aggressive Nether mob; fears warped fungus."),
    ("zoglin", "Hostile", "40", "6", "Undead hoglin hostile to everything."),
    ("shulker", "Hostile", "30", "4", "Fires levitation projectiles."),
    ("warden", "Hostile", "500", "30", "Blind; senses vibrations and smell."),
    ("ender_dragon", "Boss", "200", "10", "Boss fought in the End."),
    ("wither", "Boss", "300", "8", "Summoned boss firing explosive skulls."),
    ("cow", "Passive", "10", "0", "Drops leather and beef; can be milked."),
    ("pig", "Passive", "10", "0", "Rideable with a saddle and carrot stick."),
    ("sheep", "Passive", "8", "0", "Provides wool; regrows after shearing."),
    ("chicken", "Passive", "4", "0", "Lays eggs and drops feathers."),
    ("horse", "Passive", "15-30", "0", "Rideable; variable speed and jump."),
    ("rabbit", "Passive", "3", "0", "Fast hopper; killer bunny is hostile."),
    ("villager", "Passive", "20", "0", "Trades goods by profession and level."),
    ("cat", "Passive", "10", "3", "Scares away creepers and phantoms."),
    ("fox", "Passive", "10", "2", "Forages at night, sleeps in the day."),
    ("panda", "Passive", "20", "6", "Jungle mob with personality genes."),
    ("turtle", "Passive", "30", "0", "Lays eggs on home beaches; drops scute."),
    ("axolotl", "Passive", "14", "2", "Aquatic ally that plays dead."),
    ("frog", "Passive", "10", "0", "Eats small slimes; three variants."),
    ("allay", "Passive", "20", "0", "Collects duplicate items for you."),
    ("camel", "Passive", "32", "0", "Tall desert mount for two riders."),
    ("sniffer", "Passive", "14", "0", "Ancient mob that digs up seeds."),
    ("copper_golem", "Passive", "20", "0", "Sorts items; slowly oxidizes over time."),
    ("wolf", "Neutral", "8", "4", "Tameable ally that attacks threats."),
    ("bee", "Neutral", "10", "2", "Pollinates flowers; stings when provoked."),
    ("piglin", "Neutral", "16", "5", "Barters gold ingots for items."),
    ("polar_bear", "Neutral", "30", "6", "Aggressive when cubs are nearby."),
    ("llama", "Neutral", "15-30", "spit", "Pack animal; equip carpet and chest."),
    ("goat", "Neutral", "10", "2", "Rams entities and jumps high."),
    ("dolphin", "Neutral", "10", "3", "Guides players to nearby structures."),
    ("iron_golem", "Neutral", "100", "7-21", "Defends villages from hostiles."),
]

GAMERULES = [
    "keep_inventory", "advance_time", "advance_weather", "mob_griefing",
    "spawn_monsters", "spawn_phantoms", "random_tick_speed", "show_death_messages",
    "command_block_output", "players_sleeping_percentage",
    "fire_spread_radius_around_player", "natural_regeneration", "fall_damage",
    "fire_damage", "drowning_damage", "do_insomnia", "do_immediate_respawn",
    "reduced_debug_info", "send_command_feedback", "do_entity_drops",
    "do_tile_drops", "do_mob_loot", "max_command_chain_length", "spawn_radius",
]

# Builders keyed by command id. Field: (key, label, kind, default, options)
#   kind: text | int | float | choice(fixed) | combo(editable) | bool
BUILDERS = {
    "give": dict(fields=[("target", "Target", "text", "@p", None),
                         ("item", "Item ID", "text", "minecraft:diamond_sword", None),
                         ("count", "Count", "int", "1", None)],
                 gen=lambda f: f"/give {f['target']} {f['item']} {f['count']}"),
    "enchant": dict(fields=[("target", "Target", "text", "@s", None),
                            ("enchant", "Enchantment", "text", "minecraft:sharpness", None),
                            ("level", "Level", "int", "1", None)],
                    gen=lambda f: f"/enchant {f['target']} {f['enchant']} {f['level']}"),
    "loot": dict(fields=[("target", "Target", "text", "@p", None),
                         ("table", "Loot table", "text", "minecraft:chests/simple_dungeon", None)],
                 gen=lambda f: f"/loot give {f['target']} loot {f['table']}"),
    "clear": dict(fields=[("target", "Target", "text", "@p", None),
                          ("item", "Item (optional)", "text", "", None),
                          ("count", "Max count (optional)", "text", "", None)],
                  gen=lambda f: ("/clear " + f['target'] + (f" {f['item']}" if f['item'] else "")
                                 + (f" {f['count']}" if f['item'] and f['count'] else "")).rstrip()),
    "summon": dict(fields=[("entity", "Entity ID", "text", "minecraft:zombie", None),
                           ("x", "X", "text", "~", None), ("y", "Y", "text", "~", None), ("z", "Z", "text", "~", None),
                           ("nbt", "NBT (optional)", "text", "", None)],
                   gen=lambda f: f"/summon {f['entity']} {f['x']} {f['y']} {f['z']}" + (f" {f['nbt']}" if f['nbt'] else "")),
    "kill": dict(fields=[("target", "Target", "text", "@e[type=minecraft:zombie]", None)],
                 gen=lambda f: f"/kill {f['target']}"),
    "attribute": dict(fields=[("target", "Target", "text", "@s", None),
                              ("attr", "Attribute", "combo", "minecraft:max_health", ["minecraft:" + a[0] for a in ATTRIBUTES]),
                              ("action", "Action", "choice", "base set", ["base set", "base get", "get"]),
                              ("value", "Value", "float", "20", None)],
                      gen=lambda f: (f"/attribute {f['target']} {f['attr']} base set {f['value']}" if f['action'] == "base set"
                                     else f"/attribute {f['target']} {f['attr']} base get" if f['action'] == "base get"
                                     else f"/attribute {f['target']} {f['attr']} get")),
    "damage": dict(fields=[("target", "Target", "text", "@e[type=minecraft:zombie]", None),
                           ("amount", "Amount", "float", "5", None)],
                   gen=lambda f: f"/damage {f['target']} {f['amount']}"),
    "ride": dict(fields=[("target", "Rider", "text", "@s", None),
                         ("action", "Action", "choice", "mount", ["mount", "dismount"]),
                         ("vehicle", "Vehicle (if mount)", "text", "@e[type=minecraft:horse,limit=1]", None)],
                 gen=lambda f: (f"/ride {f['target']} dismount" if f['action'] == "dismount"
                                else f"/ride {f['target']} mount {f['vehicle']}")),
    "rotate": dict(fields=[("target", "Target", "text", "@s", None),
                           ("rotation", "Rotation (yaw pitch)", "text", "90 0", None)],
                   gen=lambda f: f"/rotate {f['target']} {f['rotation']}"),
    "teleport": dict(fields=[("target", "Target", "text", "@p", None),
                             ("x", "X", "text", "~", None), ("y", "Y", "text", "~", None), ("z", "Z", "text", "~", None)],
                     gen=lambda f: f"/teleport {f['target']} {f['x']} {f['y']} {f['z']}"),
    "setblock": dict(fields=[("x", "X", "text", "~", None), ("y", "Y", "text", "~", None), ("z", "Z", "text", "~", None),
                             ("block", "Block ID", "text", "minecraft:diamond_block", None),
                             ("mode", "Mode", "choice", "replace", ["replace", "keep", "destroy"])],
                     gen=lambda f: f"/setblock {f['x']} {f['y']} {f['z']} {f['block']} {f['mode']}"),
    "fill": dict(fields=[("x1", "X1", "text", "~", None), ("y1", "Y1", "text", "~", None), ("z1", "Z1", "text", "~", None),
                         ("x2", "X2", "text", "~10", None), ("y2", "Y2", "text", "~10", None), ("z2", "Z2", "text", "~10", None),
                         ("block", "Block ID", "text", "minecraft:stone", None),
                         ("mode", "Mode", "choice", "replace", ["replace", "keep", "outline", "hollow", "destroy"])],
                 gen=lambda f: f"/fill {f['x1']} {f['y1']} {f['z1']} {f['x2']} {f['y2']} {f['z2']} {f['block']} {f['mode']}"),
    "clone": dict(fields=[("x1", "From X1", "text", "~", None), ("y1", "Y1", "text", "~", None), ("z1", "Z1", "text", "~", None),
                          ("x2", "To X2", "text", "~10", None), ("y2", "Y2", "text", "~10", None), ("z2", "Z2", "text", "~10", None),
                          ("dx", "Dest X", "text", "~", None), ("dy", "Dest Y", "text", "~20", None), ("dz", "Dest Z", "text", "~", None)],
                  gen=lambda f: f"/clone {f['x1']} {f['y1']} {f['z1']} {f['x2']} {f['y2']} {f['z2']} {f['dx']} {f['dy']} {f['dz']}"),
    "locate": dict(fields=[("type", "Type", "choice", "structure", ["structure", "biome", "poi"]),
                           ("id", "ID", "text", "minecraft:village_plains", None)],
                   gen=lambda f: f"/locate {f['type']} {f['id']}"),
    "time": dict(fields=[("value", "Value", "combo", "day", ["day", "night", "noon", "midnight", "0", "6000", "13000", "18000"])],
                 gen=lambda f: f"/time set {f['value']}"),
    "weather": dict(fields=[("type", "Type", "choice", "clear", ["clear", "rain", "thunder"]),
                            ("duration", "Duration s (optional)", "text", "", None)],
                    gen=lambda f: f"/weather {f['type']}" + (f" {f['duration']}" if f['duration'] else "")),
    "gamemode": dict(fields=[("mode", "Mode", "choice", "creative", ["survival", "creative", "adventure", "spectator"]),
                             ("target", "Target (optional)", "text", "@p", None)],
                     gen=lambda f: f"/gamemode {f['mode']}" + (f" {f['target']}" if f['target'] else "")),
    "effect": dict(fields=[("target", "Target", "text", "@p", None),
                           ("effect", "Effect ID", "text", "minecraft:speed", None),
                           ("seconds", "Duration s", "int", "30", None),
                           ("amp", "Amplifier", "int", "0", None),
                           ("hide", "Hide particles", "bool", "false", None)],
                   gen=lambda f: f"/effect give {f['target']} {f['effect']} {f['seconds']} {f['amp']} {f['hide']}"),
    "xp": dict(fields=[("action", "Action", "choice", "add", ["add", "set", "query"]),
                       ("target", "Target", "text", "@p", None),
                       ("amount", "Amount", "int", "10", None),
                       ("unit", "Unit", "choice", "points", ["points", "levels"])],
               gen=lambda f: f"/experience {f['action']} {f['target']} {f['amount']} {f['unit']}"),
    "title": dict(fields=[("target", "Target", "text", "@a", None),
                          ("action", "Type", "choice", "title", ["title", "subtitle", "actionbar"]),
                          ("text", "Text", "text", "Hello!", None)],
                  gen=lambda f: f'/title {f["target"]} {f["action"]} {{"text":"{f["text"]}"}}'),
    "tellraw": dict(fields=[("target", "Target", "text", "@a", None),
                            ("text", "Message", "text", "Hello, world!", None)],
                    gen=lambda f: f'/tellraw {f["target"]} {{"text":"{f["text"]}"}}'),
    "playsound": dict(fields=[("sound", "Sound ID", "text", "minecraft:entity.experience_orb.pickup", None),
                              ("source", "Source", "choice", "master",
                               ["master", "music", "record", "weather", "block", "hostile", "neutral", "player", "ambient", "voice"]),
                              ("target", "Target", "text", "@a", None),
                              ("volume", "Volume", "float", "1", None),
                              ("pitch", "Pitch", "float", "1", None)],
                      gen=lambda f: f"/playsound {f['sound']} {f['source']} {f['target']} ~ ~ ~ {f['volume']} {f['pitch']}"),
    "particle": dict(fields=[("particle", "Particle ID", "text", "minecraft:flame", None),
                             ("x", "X", "text", "~", None), ("y", "Y", "text", "~", None), ("z", "Z", "text", "~", None),
                             ("count", "Count", "int", "10", None)],
                     gen=lambda f: f"/particle {f['particle']} {f['x']} {f['y']} {f['z']} 0 0 0 1 {f['count']}"),
    "gamerule": dict(fields=[("rule", "Rule (26.x snake_case)", "combo", "keep_inventory", GAMERULES),
                             ("value", "Value", "text", "true", None)],
                     gen=lambda f: f"/gamerule {f['rule']} {f['value']}"),
    "difficulty": dict(fields=[("level", "Level", "choice", "normal", ["peaceful", "easy", "normal", "hard"])],
                       gen=lambda f: f"/difficulty {f['level']}"),
    "tick": dict(fields=[("action", "Action", "choice", "rate", ["rate", "freeze", "unfreeze", "step", "sprint", "query"]),
                         ("value", "Value (rate/step/sprint)", "text", "20", None)],
                 gen=lambda f: (f"/tick {f['action']}" if f['action'] in ("freeze", "unfreeze", "query")
                                else f"/tick {f['action']} {f['value']}")),
    "tag": dict(fields=[("target", "Target", "text", "@s", None),
                        ("action", "Action", "choice", "add", ["add", "remove", "list"]),
                        ("name", "Tag name", "text", "myTag", None)],
                gen=lambda f: (f"/tag {f['target']} list" if f['action'] == "list"
                               else f"/tag {f['target']} {f['action']} {f['name']}")),
    "scoreboard": dict(fields=[("name", "Objective", "text", "kills", None),
                               ("criteria", "Criteria", "text", "dummy", None),
                               ("display", "Display name (optional)", "text", "", None)],
                       gen=lambda f: f"/scoreboard objectives add {f['name']} {f['criteria']}" + (f' "{f["display"]}"' if f['display'] else "")),
    "advancement": dict(fields=[("action", "Action", "choice", "grant", ["grant", "revoke"]),
                                ("target", "Target", "text", "@p", None),
                                ("scope", "Scope", "choice", "everything", ["everything", "only"]),
                                ("adv", "Advancement (if only)", "text", "minecraft:story/mine_stone", None)],
                        gen=lambda f: (f"/advancement {f['action']} {f['target']} everything" if f['scope'] == "everything"
                                       else f"/advancement {f['action']} {f['target']} only {f['adv']}")),
    "execute": dict(fields=[("as_", "as (selector)", "text", "@a", None),
                            ("at", "at (selector)", "text", "@s", None),
                            ("run", "Run command", "text", "say hi", None)],
                    gen=lambda f: f"/execute as {f['as_']} at {f['at']} run {f['run']}"),
    "function": dict(fields=[("name", "Function ID", "text", "namespace:path", None)],
                     gen=lambda f: f"/function {f['name']}"),
    "transfer": dict(fields=[("host", "Hostname", "text", "play.example.net", None),
                             ("port", "Port", "int", "25565", None),
                             ("players", "Players", "text", "@a", None)],
                     gen=lambda f: f"/transfer {f['host']} {f['port']} {f['players']}"),
    "whitelist": dict(fields=[("action", "Action", "choice", "add", ["add", "remove", "on", "off", "list", "reload"]),
                              ("player", "Player (add/remove)", "text", "Steve", None)],
                      gen=lambda f: (f"/whitelist {f['action']}" if f['action'] in ("on", "off", "list", "reload")
                                     else f"/whitelist {f['action']} {f['player']}")),
    "kick": dict(fields=[("player", "Player", "text", "Steve", None),
                         ("reason", "Reason (optional)", "text", "", None)],
                 gen=lambda f: f"/kick {f['player']}" + (f" {f['reason']}" if f['reason'] else "")),
    "op": dict(fields=[("action", "Action", "choice", "op", ["op", "deop"]),
                       ("player", "Player", "text", "Steve", None)],
               gen=lambda f: f"/{f['action']} {f['player']}"),
}


# ============================================================================
# Small rounded button on a Canvas
# ============================================================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, fill, fg, hover, font,
                 width=150, height=40, radius=10):
        super().__init__(parent, width=width, height=height,
                         bg=parent.cget("bg"), highlightthickness=0, bd=0)
        self.command, self.fill, self.hover = command, fill, hover
        self._shape = self._round(2, 2, width - 2, height - 2, radius, fill=fill)
        self._text = self.create_text(width / 2, height / 2, text=text, fill=fg, font=font)
        self.configure(cursor="hand2")
        self.bind("<Enter>", lambda e: self.itemconfig(self._shape, fill=self.hover))
        self.bind("<Leave>", lambda e: self.itemconfig(self._shape, fill=self.fill))
        self.bind("<Button-1>", lambda e: self.command())

    def _round(self, x1, y1, x2, y2, r, **kw):
        pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
               x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(pts, smooth=True, **kw)

    def set(self, text=None, fill=None, hover=None, fg=None):
        if text is not None:
            self.itemconfig(self._text, text=text)
        if fg is not None:
            self.itemconfig(self._text, fill=fg)
        if fill is not None:
            self.fill = fill
            self.itemconfig(self._shape, fill=fill)
        if hover is not None:
            self.hover = hover


# ============================================================================
# App
# ============================================================================
class CommandTable(tk.Tk):
    def __init__(self):
        super().__init__()
        self.theme_name = "dark"
        set_theme(self.theme_name)
        self.title("Commandstone")
        self.geometry("1000x680")
        self.minsize(880, 600)
        self.configure(bg=BG)

        fams = set(tkfont.families())
        ui = pick(fams, "Segoe UI", "Helvetica Neue", "Arial")
        mono = pick(fams, "Consolas", "JetBrains Mono", "Menlo", "Courier New")
        self.F_TITLE = (ui, 17, "bold")
        self.F_SUB = (ui, 9)
        self.F_H = (ui, 14, "bold")
        self.F_NAME = (ui, 11, "bold")
        self.F_DESC = (ui, 9)
        self.F_LABEL = (ui, 8, "bold")
        self.F_PILL = (mono, 8)
        self.F_MONO = (mono, 11)
        self.F_MONO_S = (mono, 10)
        self.F_BTN = (ui, 10, "bold")

        self.active_filter = "all"
        self._restore_sel = None
        self._build_ui()

    def _build_ui(self):
        for w in self.winfo_children():
            w.destroy()
        self.configure(bg=BG)
        self._style()
        self._build_menu()
        self.rows = []
        self.selected_row = None
        self.detail_vars = {}
        self.detail_gen = None

        self._build_header()
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=(6, 12))
        self._build_sidebar(body)
        self._build_detail(body)

        self._rebuild_list()
        if self._restore_sel:
            want, self._restore_sel = self._restore_sel, None
            for ro in self.rows:
                it = ro["item"]
                if (it["kind"], it["id"]) == want:
                    self._select(ro)
                    return
        self._show_empty_detail()

    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        set_theme(self.theme_name)
        if self.selected_row:
            it = self.selected_row["item"]
            self._restore_sel = (it["kind"], it["id"])
        self._build_ui()

    def _style(self):
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("TCombobox", fieldbackground=FIELD, background=CARD,
                     foreground=TEXT, arrowcolor=TEXT_DIM, bordercolor=BORDER,
                     lightcolor=BORDER, darkcolor=BORDER, selectbackground=FIELD,
                     selectforeground=TEXT, padding=4)
        st.map("TCombobox", fieldbackground=[("readonly", FIELD)],
               foreground=[("readonly", TEXT)])
        self.option_add("*TCombobox*Listbox.background", CARD)
        self.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", ACCENT_INK)
        st.configure("Vertical.TScrollbar", background=CARD, troughcolor=BG,
                     arrowcolor=TEXT_FAINT, bordercolor=BG, relief="flat")

    # ---- header --------------------------------------------------------
    def _build_header(self):
        h = tk.Frame(self, bg=BG)
        h.pack(fill="x", padx=16, pady=(14, 4))
        self._grass_icon(h).pack(side="left", padx=(0, 12))
        col = tk.Frame(h, bg=BG)
        col.pack(side="left")
        tk.Label(col, text="Commandstone", bg=BG, fg=TEXT, font=self.F_TITLE).pack(anchor="w")
        tk.Label(col, text=f"{len(COMMANDS)} commands  \u00b7  {len(ATTRIBUTES)} attributes  \u00b7  {len(ENTITIES)} mobs",
                 bg=BG, fg=TEXT_DIM, font=self.F_SUB).pack(anchor="w")
        # top-right controls
        self._theme_toggle(h).pack(side="right", ipadx=11, ipady=6)
        tk.Label(h, text="Java 26.x", bg=CARD, fg=TEXT_DIM, font=self.F_PILL).pack(
            side="right", padx=(0, 10), ipadx=8, ipady=6)

    def _grass_icon(self, parent, size=42):
        """Draw an original isometric grass-block cube (not the Minecraft logo)."""
        c = tk.Canvas(parent, width=size, height=size, bg=BG, highlightthickness=0, bd=0)
        top, top_hi = "#7bc74d", "#93d964"
        left, right = "#7a5a3a", "#5f4630"
        grass_l, grass_r = "#5aa838", "#4a8c2c"
        cx = size / 2

        def poly(pts, fill):
            c.create_polygon([v for xy in pts for v in xy], fill=fill, outline="")

        poly([(6, 13), (cx, 22), (cx, size - 4), (6, size - 13)], left)       # left face
        poly([(size - 6, 13), (cx, 22), (cx, size - 4), (size - 6, size - 13)], right)  # right face
        poly([(6, 13), (cx, 22), (cx, 27), (6, 18)], grass_l)                 # grass fringe L
        poly([(size - 6, 13), (cx, 22), (cx, 27), (size - 6, 18)], grass_r)   # grass fringe R
        poly([(cx, 4), (size - 6, 13), (cx, 22), (6, 13)], top)               # top face
        poly([(cx, 8), (cx + 7, 13), (cx, 18), (cx - 7, 13)], top_hi)         # top highlight
        return c

    def _theme_toggle(self, parent):
        dark = self.theme_name == "dark"
        text = "\u2600  Light" if dark else "\u263D  Dark"
        lbl = tk.Label(parent, text=text, bg=CARD, fg=TEXT_DIM, font=self.F_PILL, cursor="hand2")
        lbl.bind("<Button-1>", lambda e: self._toggle_theme())
        lbl.bind("<Enter>", lambda e: lbl.configure(bg=CARD_HOV, fg=TEXT))
        lbl.bind("<Leave>", lambda e: lbl.configure(bg=CARD, fg=TEXT_DIM))
        return lbl

    # ---- menu bar & dialogs -------------------------------------------
    def _build_menu(self):
        mb = tk.Menu(self)
        filem = tk.Menu(mb, tearoff=0)
        filem.add_command(label="Quit", command=self.destroy)
        mb.add_cascade(label="File", menu=filem)

        viewm = tk.Menu(mb, tearoff=0)
        other = "light" if self.theme_name == "dark" else "dark"
        viewm.add_command(label=f"Switch to {other} mode", command=self._toggle_theme)
        mb.add_cascade(label="View", menu=viewm)

        helpm = tk.Menu(mb, tearoff=0)
        helpm.add_command(label=f"How to use {APP_NAME}", command=self._show_help)
        helpm.add_separator()
        helpm.add_command(label=f"About {APP_NAME}", command=self._show_about)
        mb.add_cascade(label="Help", menu=helpm)

        self.config(menu=mb)

    def _dialog(self, title, width, height):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=BG)
        win.resizable(False, False)
        win.transient(self)
        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - width) // 2
        y = self.winfo_rooty() + (self.winfo_height() - height) // 3
        win.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")
        win.grab_set()
        win.bind("<Escape>", lambda e: win.destroy())
        return win

    def _show_about(self):
        win = self._dialog(f"About {APP_NAME}", 420, 340)
        wrap = tk.Frame(win, bg=BG)
        wrap.pack(fill="both", expand=True, padx=26, pady=22)
        self._grass_icon(wrap, size=54).pack()
        tk.Label(wrap, text=APP_NAME, bg=BG, fg=TEXT, font=self.F_TITLE).pack(pady=(10, 0))
        tk.Label(wrap, text=f"Version {APP_VERSION}", bg=BG, fg=ACCENT, font=self.F_PILL).pack(pady=(2, 12))
        tk.Label(wrap, text=APP_TAGLINE, bg=BG, fg=TEXT_DIM, font=self.F_DESC,
                 wraplength=360, justify="center").pack()
        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x", pady=16)
        tk.Label(wrap, text="Created by", bg=BG, fg=TEXT_FAINT, font=self.F_LABEL).pack()
        tk.Label(wrap, text=APP_AUTHOR, bg=BG, fg=TEXT, font=self.F_NAME).pack(pady=(2, 0))
        tk.Label(wrap, text="Reference data reflects Minecraft Java Edition 26.x.",
                 bg=BG, fg=TEXT_FAINT, font=self.F_PILL, wraplength=360, justify="center").pack(pady=(14, 12))
        RoundedButton(wrap, "Close", win.destroy, ACCENT, ACCENT_INK, ACCENT_HOV,
                      self.F_BTN, width=120, height=38).pack()

    def _show_help(self):
        win = self._dialog(f"How to use {APP_NAME}", 560, 520)
        head = tk.Frame(win, bg=BG)
        head.pack(fill="x", padx=24, pady=(20, 6))
        self._grass_icon(head, size=34).pack(side="left", padx=(0, 10))
        tk.Label(head, text=f"How to use {APP_NAME}", bg=BG, fg=TEXT, font=self.F_H).pack(side="left")

        body = tk.Frame(win, bg=FIELD, highlightthickness=1, highlightbackground=BORDER)
        body.pack(fill="both", expand=True, padx=24, pady=8)
        txt = tk.Text(body, bg=FIELD, fg=TEXT_DIM, font=self.F_DESC, relief="flat",
                      wrap="word", padx=16, pady=14, highlightthickness=0, spacing1=1, spacing3=5)
        txt.pack(fill="both", expand=True)

        txt.tag_configure("h", foreground=TEXT, font=self.F_NAME, spacing1=8, spacing3=3)
        txt.tag_configure("accent", foreground=ACCENT, font=self.F_DESC)

        def line(text, tag=None):
            txt.insert("end", text + "\n", tag or ())

        line(f"{APP_NAME} is a searchable reference and command builder for Minecraft: Java Edition. "
             "Everything runs offline in this window.")
        line("")
        line("Search", "h")
        line("Type in the search box to filter across every command, entity attribute, and mob at once. "
             "Use the All / Commands / Attributes / Mobs chips to narrow what's listed. "
             "The result count updates as you type.")
        line("")
        line("Build a command", "h")
        line("Click any item in the list and it opens on the right:")
        line("  \u2022  Commands open a builder \u2014 fill in the fields and the finished command updates "
             "live in the preview. Press Copy command to send it to your clipboard.")
        line("  \u2022  Attributes become a ready /attribute \u2026 base set \u2026 command.")
        line("  \u2022  Mobs become a /summon \u2026 command with editable coordinates.")
        line("Commands without a dedicated builder show an editable syntax line you can tweak and copy.")
        line("")
        line("Themes", "h")
        line("Use the toggle in the top-right corner, or the View menu, to switch between dark and light. "
             "Your current selection is kept when you switch.")
        line("")
        line("Good to know", "h")
        line("Data reflects current Java Edition (26.x). Attribute IDs are flattened (for example "
             "minecraft:max_health) and gamerules use snake_case names. Minecraft changes quickly \u2014 "
             "in-game tab-completion is always the final word for your exact version.")
        txt.configure(state="disabled")

        btn = tk.Frame(win, bg=BG)
        btn.pack(fill="x", padx=24, pady=(6, 18))
        RoundedButton(btn, "Close", win.destroy, ACCENT, ACCENT_INK, ACCENT_HOV,
                      self.F_BTN, width=120, height=38).pack(side="right")

    # ---- sidebar (search + filters + list) -----------------------------
    def _build_sidebar(self, parent):
        side = tk.Frame(parent, bg=SIDEBAR, width=350)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        # search
        sb = tk.Frame(side, bg=FIELD, highlightthickness=1,
                      highlightbackground=BORDER, highlightcolor=ACCENT)
        sb.pack(fill="x", padx=14, pady=(14, 10))
        tk.Label(sb, text="\U0001F50D", bg=FIELD, fg=TEXT_FAINT, font=(self.F_SUB[0], 10)).pack(side="left", padx=(10, 4))
        self.query = tk.StringVar()
        self.query.trace_add("write", lambda *_: self._rebuild_list())
        e = tk.Entry(sb, textvariable=self.query, bg=FIELD, fg=TEXT, font=self.F_MONO_S,
                     relief="flat", insertbackground=TEXT)
        e.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))
        self._placeholder(e, "Search commands, attributes, mobs")

        # filters
        fr = tk.Frame(side, bg=SIDEBAR)
        fr.pack(fill="x", padx=10)
        self.filter_btns = {}
        for key, label, count in [("all", "All", len(COMMANDS) + len(ATTRIBUTES) + len(ENTITIES)),
                                  ("command", "Commands", len(COMMANDS)),
                                  ("attribute", "Attributes", len(ATTRIBUTES)),
                                  ("entity", "Mobs", len(ENTITIES))]:
            b = self._filter_button(fr, key, label, count)
            b.pack(side="left", padx=4)

        # count line
        self.count_lbl = tk.Label(side, text="", bg=SIDEBAR, fg=TEXT_FAINT, font=self.F_PILL, anchor="w")
        self.count_lbl.pack(fill="x", padx=18, pady=(8, 2))

        # scrollable list
        lw = tk.Frame(side, bg=SIDEBAR)
        lw.pack(fill="both", expand=True, padx=(8, 6), pady=(0, 10))
        self.canvas = tk.Canvas(lw, bg=SIDEBAR, highlightthickness=0)
        sc = ttk.Scrollbar(lw, orient="vertical", command=self.canvas.yview)
        self.list_inner = tk.Frame(self.canvas, bg=SIDEBAR)
        self.list_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.win = self.canvas.create_window((0, 0), window=self.list_inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.canvas.configure(yscrollcommand=sc.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")
        # scoped mousewheel
        self.canvas.bind("<Enter>", lambda e: self._wheel(True))
        self.canvas.bind("<Leave>", lambda e: self._wheel(False))

    def _filter_button(self, parent, key, label, count):
        active = key == self.active_filter
        holder = tk.Frame(parent, bg=SIDEBAR)
        chip = tk.Label(holder, text=f"{label} {count}", bg=(CARD_SEL if active else CARD),
                        fg=(TEXT if active else TEXT_DIM), font=self.F_PILL, cursor="hand2")
        chip.pack(ipadx=9, ipady=5)
        chip.bind("<Button-1>", lambda e, k=key: self._set_filter(k))
        chip.bind("<Enter>", lambda e: chip.configure(bg=CARD_HOV) if self.active_filter != key else None)
        chip.bind("<Leave>", lambda e: chip.configure(bg=(CARD_SEL if self.active_filter == key else CARD)))
        self.filter_btns[key] = chip
        return holder

    def _set_filter(self, key):
        self.active_filter = key
        for k, chip in self.filter_btns.items():
            on = k == key
            chip.configure(bg=(CARD_SEL if on else CARD), fg=(TEXT if on else TEXT_DIM))
        self._rebuild_list()

    def _wheel(self, on):
        if on:
            self.canvas.bind_all("<MouseWheel>", self._on_wheel)
            self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
            self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
        else:
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")

    def _on_wheel(self, e):
        self.canvas.yview_scroll(-1 if e.delta > 0 else 1, "units")

    def _placeholder(self, entry, text):
        entry.insert(0, text)
        entry.configure(fg=TEXT_FAINT)
        entry._ph_on = True

        def fin(_):
            if getattr(entry, "_ph_on", False):
                entry.delete(0, "end"); entry.configure(fg=TEXT); entry._ph_on = False

        def fout(_):
            if not entry.get():
                entry.insert(0, text); entry.configure(fg=TEXT_FAINT); entry._ph_on = True

        entry.bind("<FocusIn>", fin)
        entry.bind("<FocusOut>", fout)

    # ---- build the searchable list -------------------------------------
    def _q(self):
        q = self.query.get().strip().lower()
        return "" if getattr(self, "_ph_guard", False) or q == "search commands, attributes, mobs" else q

    def _items(self):
        q = self._q()
        out = []
        f = self.active_filter
        if f in ("all", "command"):
            for cid, name, syntax, desc, cat in COMMANDS:
                if not q or q in name.lower() or q in syntax.lower() or q in desc.lower() or q in cat.lower():
                    out.append(dict(kind="command", id=cid, name=name, badge=cat,
                                    color=CMD_CAT_COLOR.get(cat, TEXT_DIM), desc=desc,
                                    syntax=syntax, cat=cat))
        if f in ("all", "attribute"):
            for aid, dflt, mn, mx, desc in ATTRIBUTES:
                if not q or q in aid.lower() or q in desc.lower():
                    out.append(dict(kind="attribute", id=aid, name="minecraft:" + aid, badge="attribute",
                                    color=ATTR_COLOR, desc=desc, default=dflt, mn=mn, mx=mx))
        if f in ("all", "entity"):
            for eid, cat, hp, dmg, desc in ENTITIES:
                if not q or q in eid.lower() or q in desc.lower() or q in cat.lower():
                    out.append(dict(kind="entity", id=eid, name="minecraft:" + eid, badge=cat,
                                    color=ENT_CAT_COLOR.get(cat, TEXT_DIM), desc=desc, hp=hp, dmg=dmg, cat=cat))
        return out

    def _rebuild_list(self):
        for w in self.list_inner.winfo_children():
            w.destroy()
        self.rows = []
        self.selected_row = None
        items = self._items()
        self.count_lbl.configure(text=f"{len(items)} result" + ("" if len(items) == 1 else "s"))
        if not items:
            tk.Label(self.list_inner, text="No matches.\nTry another term.", bg=SIDEBAR,
                     fg=TEXT_FAINT, font=self.F_DESC, justify="left").pack(anchor="w", padx=12, pady=20)
            return
        for it in items:
            self._make_row(it)

    def _make_row(self, item):
        row = tk.Frame(self.list_inner, bg=CARD, cursor="hand2")
        row.pack(fill="x", pady=2)
        stripe = tk.Frame(row, bg=CARD, width=3)
        stripe.pack(side="left", fill="y")
        inner = tk.Frame(row, bg=CARD)
        inner.pack(side="left", fill="both", expand=True, padx=(9, 10), pady=7)
        top = tk.Frame(inner, bg=CARD)
        top.pack(fill="x")
        name = tk.Label(top, text=item["name"], bg=CARD, fg=TEXT, font=self.F_NAME, anchor="w")
        name.pack(side="left")
        pill = tk.Label(top, text=item["badge"].lower(), bg=CARD, fg=item["color"], font=self.F_PILL)
        pill.pack(side="right")
        desc = tk.Label(inner, text=item["desc"], bg=CARD, fg=TEXT_DIM, font=self.F_DESC,
                        anchor="w", justify="left")
        desc.pack(fill="x", pady=(1, 0))

        bgw = [row, inner, top, name, desc]
        ro = dict(frame=row, stripe=stripe, bgw=bgw, pill=pill, accent=item["color"],
                  item=item, selected=False)

        def paint(bg):
            for w in bgw:
                w.configure(bg=bg)
            pill.configure(bg=bg)

        ro["paint"] = paint

        def enter(_):
            if not ro["selected"]:
                paint(CARD_HOV); stripe.configure(bg=ro["accent"])

        def leave(_):
            if not ro["selected"]:
                paint(CARD); stripe.configure(bg=CARD)

        def click(_):
            self._select(ro)

        for w in (row, inner, top, name, desc, pill, stripe):
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)
            w.bind("<Button-1>", click)
        self.rows.append(ro)

    def _select(self, ro):
        if self.selected_row and self.selected_row is not ro:
            self.selected_row["selected"] = False
            self.selected_row["paint"](CARD)
            self.selected_row["stripe"].configure(bg=CARD)
        ro["selected"] = True
        ro["paint"](CARD_SEL)
        ro["stripe"].configure(bg=ro["accent"])
        self.selected_row = ro
        self._render_detail(ro["item"])

    # ---- detail panel --------------------------------------------------
    def _build_detail(self, parent):
        wrap = tk.Frame(parent, bg=BG)
        wrap.pack(side="left", fill="both", expand=True, padx=(14, 0))
        self.detail = tk.Frame(wrap, bg=BG)
        self.detail.pack(fill="both", expand=True)

    def _clear_detail(self):
        for w in self.detail.winfo_children():
            w.destroy()

    def _show_empty_detail(self):
        self._clear_detail()
        box = tk.Frame(self.detail, bg=BG)
        box.place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(box, text="\u2039  /  \u203a", bg=BG, fg=BORDER, font=(self.F_TITLE[0], 40, "bold")).pack()
        tk.Label(box, text="Pick something on the left", bg=BG, fg=TEXT_DIM, font=self.F_H).pack(pady=(10, 4))
        tk.Label(box, text="Commands open a builder. Attributes and mobs\nturn into a ready-to-copy command too.",
                 bg=BG, fg=TEXT_FAINT, font=self.F_DESC, justify="center").pack()

    def _spec_for(self, item):
        """Return (subtitle, meta, fields, gen) for the detail form."""
        if item["kind"] == "command":
            cid = item["id"]
            bid = "op" if cid == "deop" else cid
            if bid in BUILDERS:
                b = BUILDERS[bid]
                fields = list(b["fields"])
                gen = b["gen"]
                # default deop action
                if cid == "deop":
                    fields = [("action", "Action", "choice", "deop", ["op", "deop"]) if f[0] == "action" else f
                              for f in fields]
                return item["syntax"], None, fields, gen
            # fallback: editable syntax line
            return (item["syntax"], None,
                    [("cmd", "Command (edit, then copy)", "text", item["syntax"], None)],
                    lambda f: f["cmd"])
        if item["kind"] == "attribute":
            meta = f"default {item['default']}    \u00b7    min {item['mn']}    \u00b7    max {item['mx']}"
            fields = [("target", "Target", "text", "@s", None),
                      ("action", "Action", "choice", "base set", ["base set", "base get", "get"]),
                      ("value", "Value", "float", str(item["default"]), None)]
            aid = "minecraft:" + item["id"]

            def gen(f, aid=aid):
                if f["action"] == "base set":
                    return f"/attribute {f['target']} {aid} base set {f['value']}"
                if f["action"] == "base get":
                    return f"/attribute {f['target']} {aid} base get"
                return f"/attribute {f['target']} {aid} get"
            return "/attribute " + aid + " ...", meta, fields, gen
        # entity
        meta = f"health {item['hp']}    \u00b7    attack {item['dmg']}    \u00b7    {item['cat']}"
        eid = "minecraft:" + item["id"]
        fields = [("x", "X", "text", "~", None), ("y", "Y", "text", "~", None), ("z", "Z", "text", "~", None),
                  ("nbt", "NBT (optional)", "text", "", None)]

        def gen(f, eid=eid):
            return f"/summon {eid} {f['x']} {f['y']} {f['z']}" + (f" {f['nbt']}" if f['nbt'] else "")
        return "/summon " + eid + " ...", meta, fields, gen

    def _render_detail(self, item):
        self._clear_detail()
        subtitle, meta, fields, gen = self._spec_for(item)
        self.detail_gen = gen

        pad = tk.Frame(self.detail, bg=BG)
        pad.pack(fill="both", expand=True, padx=6, pady=2)

        # header
        head = tk.Frame(pad, bg=BG)
        head.pack(fill="x", pady=(6, 2))
        tk.Label(head, text=item["name"], bg=BG, fg=TEXT, font=self.F_H).pack(side="left")
        tk.Label(head, text=item["badge"].lower(), bg=CARD, fg=item["color"],
                 font=self.F_PILL).pack(side="left", padx=10, ipadx=8, ipady=3)

        tk.Label(pad, text=item["desc"], bg=BG, fg=TEXT_DIM, font=self.F_DESC,
                 anchor="w", justify="left", wraplength=560).pack(fill="x", pady=(4, 6))
        if subtitle:
            tk.Label(pad, text=subtitle, bg=FIELD, fg=CODE, font=self.F_MONO_S,
                     anchor="w", justify="left", wraplength=560).pack(fill="x", ipady=7, ipadx=10)
        if meta:
            tk.Label(pad, text=meta, bg=BG, fg=TEXT_FAINT, font=self.F_PILL, anchor="w").pack(fill="x", pady=(8, 0))

        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=12)

        # fields grid
        self.detail_vars = {}
        grid = tk.Frame(pad, bg=BG)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1, uniform="c")
        grid.columnconfigure(1, weight=1, uniform="c")
        full = len(fields) == 1
        for i, (key, label, kind, default, options) in enumerate(fields):
            r, c = (i, 0) if full else divmod(i, 2)
            cell = tk.Frame(grid, bg=BG)
            cell.grid(row=r, column=(0 if full else c), columnspan=(2 if full else 1),
                      sticky="ew", padx=6, pady=6)
            tk.Label(cell, text=label.upper(), bg=BG, fg=TEXT_FAINT, font=self.F_LABEL).pack(anchor="w", pady=(0, 3))
            var = tk.StringVar(value=default)
            if kind in ("choice", "bool", "combo"):
                vals = ["false", "true"] if kind == "bool" else options
                state = "normal" if kind == "combo" else "readonly"
                cb = ttk.Combobox(cell, textvariable=var, values=vals, state=state, font=self.F_MONO_S)
                cb.pack(fill="x", ipady=3)
                cb.bind("<<ComboboxSelected>>", lambda e: self._update_preview())
                if kind == "combo":
                    cb.bind("<KeyRelease>", lambda e: self._update_preview())
            else:
                box = tk.Frame(cell, bg=FIELD, highlightthickness=1,
                               highlightbackground=BORDER, highlightcolor=ACCENT)
                box.pack(fill="x")
                ent = tk.Entry(box, textvariable=var, bg=FIELD, fg=TEXT, font=self.F_MONO_S,
                               relief="flat", insertbackground=TEXT)
                ent.pack(fill="x", ipady=6, padx=8)
                var.trace_add("write", lambda *_: self._update_preview())
            self.detail_vars[key] = var

        # preview
        tk.Label(pad, text="GENERATED COMMAND", bg=BG, fg=TEXT_FAINT, font=self.F_LABEL).pack(anchor="w", pady=(16, 5))
        pv = tk.Frame(pad, bg=FIELD, highlightthickness=1, highlightbackground=BORDER)
        pv.pack(fill="x")
        self.preview = tk.Text(pv, height=3, bg=FIELD, fg=CODE, font=self.F_MONO, relief="flat",
                               wrap="word", padx=12, pady=10, highlightthickness=0)
        self.preview.pack(fill="x")
        self.preview.configure(state="disabled")

        row = tk.Frame(pad, bg=BG)
        row.pack(fill="x", pady=12)
        self.copy_btn = RoundedButton(row, "Copy command", self._copy, ACCENT, ACCENT_INK,
                                      ACCENT_HOV, self.F_BTN, width=160, height=42)
        self.copy_btn.pack(side="left")
        self._update_preview()

    def _values(self):
        return {k: v.get() for k, v in self.detail_vars.items()}

    def _current(self):
        try:
            return self.detail_gen(self._values())
        except Exception as exc:
            return f"# {exc}"

    def _update_preview(self):
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", self._current())
        self.preview.configure(state="disabled")

    def _copy(self):
        self.clipboard_clear()
        self.clipboard_append(self._current())
        self.copy_btn.set(text="Copied!", fill="#3aa348", hover="#3aa348")
        self.after(1200, lambda: self.copy_btn.set(text="Copy command", fill=ACCENT, hover=ACCENT_HOV))


if __name__ == "__main__":
    CommandTable().mainloop()