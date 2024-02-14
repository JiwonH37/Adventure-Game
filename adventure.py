import json
import random
import os.path

'''
Allows the user to navigate around a (text based) world.
Data comes from adventure.json
'''
START = 'Kungfu'
FINISH = "Universal Globe"
user_list = []
special_list = []
count_num = 0

def describe(data, room):
	"""
	This function returns a sentence where it tells the user's current location and the objects in the room

	Param1: (nested dictionary) data
	Param2: (dictionary) room, which is the current location
	Returns: (string) 

	"""
	string1 = "\n" + data[room]['text'] + "\n"
	object_lst = []
	if 'objects' in data[room]:
		for object in data[room]['objects']:
			object_lst.append(object["name"])
			multiple = ' and '.join(object_lst)
			if object["type"] == "special":
				special_list.append(object["name"])

		string1 += f"You see {multiple}."
	string1 += "\n\nYour options are:\n"
	for key in data[room]['moves']:
		string1 += f"'{key}' to go to {data[room]['moves'][key]}\n"
	return string1

def user_save(username, current, item, userdata):
	"""
	This function gets the username, user's current location, the items that the users have, 
	and the dictionary that is saved already. 

	Param1: (string) username
	Param2: (dictionary) current
	Param3: (string) item
	Param4: (dictionary) userdata

	Returns:
	None
	"""
	save_dict = {username: {"location": current, "special item": item}}
	userdata.update(save_dict)
	dumping = json.dumps(userdata)
	with open('location.json', 'w') as file:
		file.write(dumping)

def main():
	data = json.load(open('custom.json'))
	play_game(data)
	
def play_game(data):
	"""
	This function has all the code for running the game. It takes the nested dictionary and runs until the user inputs quit or exit.

	Param1: (nested dictionary) data
	"""
	print('Welcome to the ICS 31 Adventure Game:\n')
	# TODO: your code here
	global count_num
	global user_list 
	end = 0
	user_name = input('Enter your name: ')
	userdata = {}
	
	# the code below is to open a json file, if it does not exist already, to save the data of the user. 
	if os.path.isfile('user.json'):
		f = open('user.json')
		userdata = json.load(f)
		f.close()
	
	# if the user inputs quit or exit, it makes the variable end to 1

	key_list = []
	for key in data.keys():
		if key != "Universal Globe":
			key_list.append(key)
	if count_num == 0:
		current_location = START
	else:
		# This is to generate the random location, excluding the final location
		current_location = random.choice(key_list)
	if end == 0:
		print_room_description(data,current_location)

	user_input = input('Your move: ').lower()

	# while the user does not input quit or exit and the is not in the FINISH room, it moves to the next room. If the user finds out the FINISH, it breaks.
	while user_input not in ['quit', 'exit'] and current_location != FINISH:
		print()
		if user_input in data[current_location]["moves"]:
			current_location = data[current_location]["moves"][user_input]
			if current_location == FINISH:
				print(f"{data[current_location]['text']}. {user_name}, you found the {FINISH}:)")
				user_list.append(user_name)
				count_num += 1
				break
			else:
				print_room_description(data,current_location)
	#if the user enters an input that is not in the moves, it tells the user to input another one
		else:
			print("Invalid move. Please choose a valid direction.")
		user_input = input('Your move: ').lower()
	if current_location == FINISH:
		play_game(data)

	else:
		print("Game Ended")
	user_save(user_name, current_location, special_list, userdata)
	# print(data)


def move_user(data, current, move):
	"""
	This function checks if the user's input is in the "moves" and if it is, it moves the user to that location

	Param1: (nested dictionary) data
	Param2: (dictionary) current
	Param3: (dictionary) move

	Return: new index
	"""
	if current in data and "moves" in data[current] and move in data[current]["moves"]:
		return data[current]['moves'][move]
	return current

def print_room_description(data, current):
	print(describe(data, current))
	
if __name__ == '__main__':
	main()