# 2D MOBA Game Design Document

## Overview
A 2D multiplayer online battle arena built with Godot 4. The game allows players to battle on multiple layered maps, including underground areas. Characters have unique abilities, and maps contain mobs, PVE quests, and bosses.

## Functional Requirements
- Multiple maps can be loaded simultaneously (e.g., surface and underground).
- Players control heroes with distinct abilities using keyboard input.
- Maps contain mobs that respawn.
- Mobs follow preset lanes and fight opposing forces automatically.
- Large maps may include PVE quests and boss encounters.
- Support for multiplayer matches.

## Non-Functional Requirements
- Built using Godot 4.
- Maintain 60 FPS on recommended hardware.
- Modular architecture to allow easy addition of maps and abilities.
- Basic cross-platform support (desktop as a priority).

## Architecture
- `Game` node orchestrates maps and players.
- `MapManager` handles switching and loading multiple maps.
- `Character` nodes represent heroes with a set of `Ability` resources.
- `Player` script adds keyboard control for a hero character.
- `Mob` scenes provide AI-controlled enemies.
- Quest and boss logic is contained in dedicated scripts within each map.

Project structure:
```
project.godot
scenes/
  Main.tscn
  maps/
    Overworld.tscn
    Underground.tscn
  player/
    Player.tscn
scripts/
  game.gd
  map_manager.gd
  character.gd
  ability.gd
  mob.gd
  player.gd
```
