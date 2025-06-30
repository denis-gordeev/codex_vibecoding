extends "res://scripts/character.gd"

var speed: float = 100.0

func _physics_process(delta: float) -> void:
    var direction = Vector2.ZERO
    if Input.is_action_pressed("ui_right"):
        direction.x += 1
    if Input.is_action_pressed("ui_left"):
        direction.x -= 1
    if Input.is_action_pressed("ui_down"):
        direction.y += 1
    if Input.is_action_pressed("ui_up"):
        direction.y -= 1
    velocity = direction.normalized() * speed
    move_and_slide()

    if Input.is_action_just_pressed("ui_accept"):
        use_ability(0)
