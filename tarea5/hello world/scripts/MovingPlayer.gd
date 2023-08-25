extends Node2D

signal touch()

@export var amplitude=500
@export var speed=1.0
var accum_time = 0.0
var next_pos_x
var offset=Vector2(200, 100)
var moveLength=5
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_button_pressed():
	rotate(0.1)


func _on_rotate_left_pressed():
	rotate(-0.1)# Replace with function body.

func _on_up_pressed():
	position.y-=moveLength

func _on_down_pressed():
	position.y+=moveLength # Replace with function body.


func _on_right_pressed():
	position.x+=moveLength
	
	

func _on_left_pressed():
	position.x-=moveLength
