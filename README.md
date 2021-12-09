## Automated Feedback on English Statements in Precise Mathematical Writing

### Motivation

The problem that I am solving is building automated systems that can grade and give feedback on precise mathematical statements/definitions inputted by students. This skill is extremely important in theoretical computer science classes such as CS 374 (the required undergraduate Algorithms & Models of Computation course at UIUC).

As part of the course staff for CS 374, I have been working on developing exercises that guide students through the problem-solving process for many different types of problems. However, one major limitation we have run into is that we aren’t able to give students any agency in writing these statements themselves. (Students do get practice writing these statements in a freeform environment on written homework assignments. However, it takes ~2 weeks for students to receive grades and feedback on these assignments, which is not optimal for being able to iterate and improve based on feedback.)

This is a pretty big shortcoming, because being able to formulate these statements clearly and precisely is a crucial part of the problem-solving process that sheds clarity on the rest of the solution. Without this step, it’s impossible to reason through the correctness of the solution. That's why I want to build a system which can help students learn this skill.

### Demo Video

https://www.youtube.com/watch?v=x4u1wt93Le4

### Setup

You'll need Python 3.9 to run this locally. (Earlier versions of Python might work too, but I haven't tested them myself.)

Clone the repository, then run `pip install -r requirements.txt`. Next, run `python3.9 server.py`, go to http://localhost:5000/, and you should be able to start playing with the tool. Enjoy!
