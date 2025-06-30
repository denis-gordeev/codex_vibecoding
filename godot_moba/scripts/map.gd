extends Node2D

export var mobs := []

func spawn_mob(scene_path: String, position: Vector2, lane: Array, team: int):
    var scene = load(scene_path)
    var mob = scene.instantiate()
    add_child(mob)
    mob.global_position = position
    mob.lane = lane
    mob.team = team
    mobs.append(mob)

func _ready():
    # Spawn example mobs for two opposing teams following simple lanes.
    var lane_a = [Vector2(50, 100), Vector2(300, 100), Vector2(550, 100)]
    var lane_b = [Vector2(550, 120), Vector2(300, 120), Vector2(50, 120)]
    spawn_mob("res://scenes/mobs/Mob.tscn", lane_a[0], lane_a, 0)
    spawn_mob("res://scenes/mobs/Mob.tscn", lane_b[0], lane_b, 1)
