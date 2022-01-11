# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Matrix.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jcollon <jcollon@student.42lyon.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/01/10 23:47:56 by jcollon           #+#    #+#              #
#    Updated: 2022/01/11 17:40:21 by jcollon          ###   ########lyon.fr    #
#                                                                              #
# **************************************************************************** #

import requests
import json
import sys
from rich import print
from rich.console import Console
import re

from print_row import print_row

try:
	with open("settings.json") as f:
		settings = json.load(f)
		CLIENT_ID = settings["CLIENT_ID"]
		CLIENT_SECRET = settings["CLIENT_SECRET"]
except FileNotFoundError:
	print("settings.json not found", file=sys.stderr)
	exit(1)
except KeyError:
	print("CLIENT_ID or CLIENT_SECRET not in settings.json", file=sys.stderr)
	exit(1)

API_ENDPOINT = "https://api.intra.42.fr"

def parse_location(location:str) -> dict:
	z = re.split(r"r", re.split(r"z", location)[1])[0]
	r = re.split(r"p", re.split(r"r", location)[1])[0]
	p = re.split(r"p", location)[1]
	return {"z": z, "r": r, "p": p}

def gen_token():
	data = {
		"grant_type": "client_credentials",
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET
	}
	r = requests.post(API_ENDPOINT + '/oauth/token', data=data)
	try:
		return r.json()['access_token']
	except KeyError:
		print("cannot get acces token, make sure your CLIENT_ID and CLIENT_SECRET are set in settings.json, they can be found at https://profile.intra.42.fr/oauth/applications", file=sys.stderr)
		exit(1)

def user_in_users(user:str, users:list[str]):
	for usr in users:
		if user in usr:
			return False
	return True

def add_tab(tab1:list[str], tab2:list[str]) -> list[str]:
	ret = []
	t1_len = 0
	t2_len = 0
	for row in tab1:
		t1_len = max(t1_len, len(row))
	for row in tab2:
		t2_len = max(t2_len, len(row))
	for i in range(max(len(tab1), len(tab2))):
		temp = []
		for j in range(t1_len):
			try:
				temp.append(tab1[i][j])
			except:
				temp.append("0")
		temp.append("-1")
		for j in range(t2_len):
			try:
				temp.append(tab2[i][j])
			except:
				temp.append("0")
		ret.append(temp)
	return ret

def print_help():
	print("""Matrix print the 42 Lyon matrix to the screen with color based
   if the color is:
      [green]green[white]: the place is available
      [red]red[white]: the place is taken by a user
      [orange1]orange[white]: the place is available, but there is something special with this place
      [blink cyan]blinking cyan""", end='')
	print("""[white]: the place is taken by the user you are searching (if using iterm2 enable blink text in the settings)

   You can use some args to select the cluster that you want to show or to search a user:
      z1: select the z1 cluster
      z2: select the z2 cluster
      z3: select the z3 cluster
      z4: select the z4 cluster
      {login}: search for a user by their login""")

if __name__ == "__main__":
	if "--help" in sys.argv:
		print_help()
		exit(0)
	console = Console()
	with open("z1.json") as f1, open("z2.json") as f2, open("z3.json") as f3, open("z4.json") as f4:
		z1 = json.load(f1)
		z2 = json.load(f2)
		z3 = json.load(f3)
		z4 = json.load(f4)

	token = gen_token()

	locations:list = requests.get(API_ENDPOINT + "/v2/campus/9/locations", data={"access_token":token}, params={"per_page":100}).json()
	for i in range(7 - 1):
		for user in requests.get(API_ENDPOINT + "/v2/campus/9/locations", data={"access_token":token}, params={"per_page":100, "page": i}).json():
			locations.append(user)

	users = []
	for user in locations:
		if user["user"]["location"] and user_in_users(user["user"]["login"], users):
			users.append((user["user"]["login"], re.sub(r"\.(.*)", "", user["user"]["location"])))
			location = parse_location(users[-1][1])
			try:
				# set the login of the user for the variable z1 or z2 or z3 or z4 at the right place
				locals()["z" + location["z"]][int(location["r"]) - 1][int(location["p"]) - 1] = users[-1][0]
			except:
				pass
	
	render1 = [None]
	render2 = [None]

	if "z1" in sys.argv:
		if "z2" in sys.argv:
			render1 = (add_tab(z1, z2), ("z1", "z2"), (len(z1[0]), len(z2[0])))
		else:
			render1 = (z1, ("z1",), (len(z1[0]),))
	elif "z2" in sys.argv:
		render1 = (z2, ("z2",), (len(z2[0]),))

	if "z3" in sys.argv:
		if "z4" in sys.argv:
			render2 = (add_tab(z3, z4), ("z3", "z4"), (len(z3[0]), len(z4[0])))
		else:
			render2 = (z3, ("z3",), (len(z3[0]),))
	elif "z4" in sys.argv:
		render2 = (z4, ("z4",), (len(z4[0]),))

	for z in ["z1", "z2", "z3", "z4"]:
		try:
			sys.argv.pop(sys.argv.index(z))
		except ValueError:
			pass

	if not (render1[0] or render2[0]):
		render1 = (add_tab(z1, z2), ("z1", "z2"), (len(z1[0]), len(z2[0])))
		render2 = (add_tab(z3, z4), ("z3", "z4"), (len(z3[0]), len(z4[0])))

	sys.argv.pop(0)	
	
	if render1[0]:
		for col in render1[0]:
			print_row(col, console, True, sys.argv)
		for i in range(len(render1[1]) - 1, -1, -1):
			print("[white b]" + render1[1][i].center(10 * render1[2][i]), end="   ")

	if render1[0] and render2[0]:
		print("\n")

	if render2[0]:
		for col in render2[0]:
			print_row(col, console, True, sys.argv)
		for i in range(len(render2[1]) - 1, -1, -1):
			print("[white b]" + render2[1][i].center(10 * render2[2][i]), end="   ")

	print()
	print(len(users), f"user{'s' if len(users) > 1 else ''}")
	if sys.argv:
		print("could not found " + ", ".join(sys.argv))
		for user in sys.argv:
			if not user_in_users(user, add_tab(add_tab(z1, z2), add_tab(z3, z4))):
				print(f"[red blink]{user}[white] is in another cluster")