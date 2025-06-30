extends Node

var maps := []

func load_map(path: String) -> Node:
    var scene = load(path)
    var instance = scene.instantiate()
    add_child(instance)
    maps.append(instance)
    return instance
