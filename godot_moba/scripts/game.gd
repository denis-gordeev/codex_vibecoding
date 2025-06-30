extends Node2D

var map_manager: Node
var player: Node

func _ready():
    map_manager = MapManager.new()
    add_child(map_manager)
    var overworld = map_manager.load_map("res://scenes/maps/Overworld.tscn")
    map_manager.load_map("res://scenes/maps/Underground.tscn")
    _spawn_player(overworld)

func _spawn_player(map: Node) -> void:
    var scene = load("res://scenes/player/Player.tscn")
    player = scene.instantiate()
    map.add_child(player)
    player.global_position = Vector2(100, 100)
