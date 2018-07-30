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



![ScreenShot1](./assets/Screen Shot 2018-07-30 at 3.09.03 PM.png)

![ScreenShot2](./assets/Screen Shot 2018-06-11 at 4.17.55 PM.png)

![ScreenShot3](./assets/Screen Shot 2018-06-11 at 4.17.34 PM.png)

