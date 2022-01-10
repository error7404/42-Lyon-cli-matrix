# 42 Lyon cli matrix

A cli tool to show the connected users and search for your next correction. **with colors**

## install
you need [python3](https://www.python.org/downloads/) to be install with [request](https://pypi.org/project/requests/) and [rich](https://pypi.org/project/rich/) installed.  
```sh
python3 -m pip install requests rich
```
### to use you'll need an api key from 42 ([get api key](https://profile.intra.42.fr/oauth/applications/new)) and to put your UID and SECRET in the `settings.json` file

## help
for more detail run
```sh
python3 Matrix.py --help
```
```
Matrix print the 42 Lyon matrix to the screen with color based
   if the color is:
      green: the place is available
      red: the place is taken by a user
      orange: the place is available, but there is something special with this place
      blinking cyan: the place is taken by the user you are searching

   You can use some args to select the cluster that you want to show or to search a user:
      z1: select the z1 cluster
      z2: select the z2 cluster
      z3: select the z3 cluster
      z4: select the z4 cluster
      {login}: search for a user by their login (only 1 user can be search)
```

![image](https://user-images.githubusercontent.com/48163201/148853307-aabe2bbf-0d58-45de-b85f-233965702d77.png)
