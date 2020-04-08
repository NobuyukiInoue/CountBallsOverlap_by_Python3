# CountBallsOverlap

Count the number of times the balls overlap like a virus infection..

This program is based on the following articles.

Why outbreaks like coronavirus spread exponentially, and how to “flatten the curve”
[https://www.washingtonpost.com/graphics/2020/world/corona-simulator/](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/)


## DEMO

```
$ python CountBallsOverlap.py patterns/pattern_balls300_heal100_with_bar_height220.txt
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
MAX_WIDTH = 800
MAX_HEIGHT = 480
MAX_BALLS = 300
RADIUS = 3
MOVEMENT = (-5, 5, 1)
SLEEP_SEC = 0.000000
CHART_HEIGHT = 300
TURNS_REQUIRED_FOR_HEAL = 100
RATIO_OF_BALLS_STOPPED = 0.0
ENABLE_BAR = True
BAR.POS_X = 200, BAR.HEIGHT = 220, BAR.WIDTH = 5

turn:contact,infected,healed,remaining
23:2,2,0,298
43:3,3,0,297
54:4,3,0,296
55:4,4,0,296
57:5,5,0,295
79:6,5,0,294
80:6,6,0,294
...
...
515:271,3,268,29
521:271,2,269,29
553:271,1,270,29
578:271,0,271,29
End ... The infected ball is gone.
```

![ScreenShot](https://github.com/NobuyukiInoue/CountBallsOverlap_by_Python3/blob/master/ScreenShot/running_balls300.png "running balls 300")


## Requirement

Python 3.x 

This program requires the pygame module.

* Windows
```
> pip install pygame
```

* macOS
```bash
$ python3 -m pip install pygame --pre --user
```


### Support OS
- MS-Windows
- macOS
- Linux

## Usage

1. Prepare a pattern file.

```
$ cat patterns/pattern_balls300_heal100_with_bar_height220.txt
# This is pattern file.

# start_wait = 10     # second.
max_width = 800
max_height = 480
max_balls = 300
radius = 2
# sleep_sec = 0.01
bar = 200, 220, 5   # pos_x, bar_height, bar_width
heal = 100
```

2. Exexute python script.

```
$ python CountBallsOverlap.py patterns/pattern_balls300_heal100_with_bar_height220.txt
```


## Licence

[MIT](https://github.com/NobuyukiInoue/CountBallsOverlap_by_Python3/blob/master/LICENSE)


## Author

[Nobuyuki Inoue](https://github.com/NobuyukiInoue/)
