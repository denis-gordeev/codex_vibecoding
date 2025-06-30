extends CharacterBody2D

# Basic lane-following mob that can attack other mobs.

var health: int = 100
var damage: int = 10
var attack_range: float = 32.0
var attack_cooldown: float = 1.0
var _cooldown_timer: float = 0.0

var lane: Array[Vector2] = []
var lane_index: int = 0
var team: int = 0
var target: Node = null

func _ready():
    add_to_group("mobs")

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        queue_free()

func _physics_process(delta: float) -> void:
    _cooldown_timer = max(_cooldown_timer - delta, 0.0)

    if target and is_instance_valid(target) and target.health > 0:
        var dist = global_position.distance_to(target.global_position)
        if dist <= attack_range:
            if _cooldown_timer <= 0.0:
                _attack(target)
        else:
            _move_towards(target.global_position)
    else:
        target = _find_target()
        if not target:
            _follow_lane()

func _move_towards(position: Vector2) -> void:
    var dir = (position - global_position).normalized()
    velocity = dir * 50
    move_and_slide()

func _follow_lane() -> void:
    if lane.size() == 0:
        return
    var point = lane[lane_index]
    if global_position.distance_to(point) < 4:
        lane_index = min(lane_index + 1, lane.size() - 1)
        point = lane[lane_index]
    _move_towards(point)

func _find_target() -> Node:
    var mobs = get_tree().get_nodes_in_group("mobs")
    for m in mobs:
        if m == self:
            continue
        if m.team == team:
            continue
        if global_position.distance_to(m.global_position) <= attack_range:
            return m
    return null

func _attack(enemy: Node) -> void:
    enemy.take_damage(damage)
    _cooldown_timer = attack_cooldown
