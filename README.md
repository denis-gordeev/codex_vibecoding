# Codex VibeCoding

This repository contains a Godot 4 project skeleton for a 2D MOBA prototype. Mobs follow simple lanes and engage enemies automatically, and a player can directly control a hero. See `docs/design.md` for the design document.

## Running

1. Install [Godot 4](https://godotengine.org/download). The community version or official binary both work.
2. Launch the editor and open the `godot_moba` folder as an existing project.
3. Run the project from the editor or execute `godot4 --path godot_moba` if you have the command-line tool installed.

The main scene is `scenes/Main.tscn`, which will load the maps and spawn a controllable hero.
