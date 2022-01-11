# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    print_row.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jcollon <jcollon@student.42lyon.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/01/10 23:48:05 by jcollon           #+#    #+#              #
#    Updated: 2022/01/11 16:43:10 by jcollon          ###   ########lyon.fr    #
#                                                                              #
# **************************************************************************** #

from rich.console import Console

def space_user (user:str) -> str:
    if user == "1" or user == "2":
        return ("".center(8))
    return user.center(8)

def print_row(row:list[str], console:Console, reverse:bool=False, search:list[str]=None) -> None:
    if row == None:
        return
    if reverse:
        row.reverse()
    COLORS = ["[red]", "[green]", "[orange1]"]
    for i in range(3):
        for user in row:
            box = ["▛▀▀▀▀▀▀▀▀▜", f"▌{space_user(str(user))}▐", "▙▄▄▄▄▄▄▄▄▟"]
            if str(user) == "-1":
                console.print("   ", end='')
            elif str(user) == "0":
                console.print("██████████", end='')
            elif str(user) == "1":
                console.print(COLORS[1] + box[i], end='')
            elif str(user) == "2":
                console.print(COLORS[2] + box[i], end='')
            elif str(user) == "3":
                box = ["[white] ▄ ▄  ▄ ▄ ", "[white]  █    █  ", "[white] ▀ ▀  ▀ ▀ "]
                console.print(box[i], end='')
            else:
                if str(user) in search:
                    if i == 2:
                        search.pop(search.index(str(user)))
                    console.print("[cyan blink]" + box[i], end='')
                else:
                    console.print(COLORS[0] + box[i], end='')
        print()