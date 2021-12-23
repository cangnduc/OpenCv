import random
import time

def find_x():
	lists = []
	while True:
		
		i = random.randint(1,3)
		if i not in lists:
			lists.append(i)
			if len(lists) == 3:
				break
				#pass
		#time.sleep(2)
	return lists


new = find_x()

dic = {
		new[0] : "You found the treasure",
		new[1] : "You loose the game",
		new[2] : "You died fighting with the dragon"

	}
key_lists = sorted(dic.keys())
new_dic = {}
for key in key_lists:
	new_dic[key] = dic[key]

while True:
	user  = int(input("user: "))
	print(f"You enter door number {user}, {dic[user]}")