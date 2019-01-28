# OBJ Viewer

[![GitHub issue author](https://img.shields.io/badge/author-DaeIn%20Lee-blue.svg)](https://github.com/LazyRen)



## How to Run

from terminal,

` python3 objviewer.py`

drag & drop any obj file you want to view.



## Implementation

drop_callback() function can load one obj file at a time.<br/>
Note that drop_callback function return immediately  if you try

1. drop more than one file at a time
2. drop the same obj file that is being rendered at the moment
3. drop file that does not have 'obj' file extension

If the action does not match any of them above, function will starts to parse information from the file line by line.



## ScreenShots

![ScreenShot1](./assets/ScreenShot-01.png)

![ScreenShot2](./assets/ScreenShot-02.png)

![ScreenShot3](./assets/ScreenShot-03.png)

![ScreenShot4](./assets/ScreenShot-04.png)

