# Conway
A Python implementation of Conway's game of life focusing on TDD and
OOP.  Influenced by portions of Corey Haine's ["Understanding the Four Rules of
Simple Design"](https://leanpub.com/4rulesofsimpledesign).

## Getting Started

1 - Build docker image:
```
docker build -t conway .
```

2 - Run bash on container instance:
```
docker run -v "$PWD":/conway -it conway bash
```

3 - Run unit tests:

```
python -m unittest
```

4 - Play a demo "Game of Life":

```
python play.py
```

## Example of play.py output:
![](./example.gif)
