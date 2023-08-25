extends Node2D

const MAX_SPEED = 80
var health=10
var target_position = Vector2.ZERO
@export var init_speed=10
# Called when the node enters the scene tree for the first time.
func _ready():
	print(":)") # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	position = target_position

func _input(event):
	if event is InputEventMouseMotion:
		print(event.position)
		target_position=event.position
	if (event is InputEventKey and event.pressed and event.as_text_key_label() == "R"):
		rotate(0.1)
