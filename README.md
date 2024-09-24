# How to Use the Switch Challenge Solver

There are two ways of using the solver

1.  Drag and Click through the Graphical User Interface (GUI), which is potentially slower. This works only for the `GUI.py` or `GUI.exe`.

2.  Enter the full formula, which can be faster when you are more familiar as you have done more assessments (very bad humour). This is available on a [web app](https://rubuky.com/tool/2024-09-23-SwitchChallenge/) and works for both `GUI` and `command_line`.

If you have python on you computer, you can run the `GUI.py` or `command_line.py` directly. Note that you have to use this way if you are running on a MacOS or Linux machine, since I have only built executables for Windows.

If you are running on Windows and you are uncomfortable with running Python, you can use the `GUI.exe` or `command_line.exe` directly, after downloading from the [Release](https://github.com/kv9898/switch_challenge_solver/releases) page.

Please give me a star🌟 if you find this useful.

# Using Drag and Click through GUI

Similar to the problems, the GUI has two rows of "shapes", the row at the top is the inputs while the other one at the bottom is the outputs. There are two ways of rearranging them:

1.  Dragging: this will *swap* the two shapes.

2.  Clicking: this will move the clicked shape to the *end*. This allows for the order of your 4 clicks to be the final order of the four shapes.

For the easiest problems (as the one below), you just need to hit `enter`，and the answer will be displayed below the line edit:

![Easy problem](img/level1.png)

*PS: to clear the formula and answer, hit `Tab`*

For the harder question, you may need to enter the formula (from level 4 onward?) and hit `Enter`. In the formula, you need to replace the options with `x`：

![Medium problem](img/level4.png)

The solver can handle x in any position:

![Hard problem](img/level9.png)

For the hardest questions with two choices, you need to make a guess about the first choice, and let the solver find the second choice. If the answer is not correct, you need to try again. You may need to try 3 times at most:

![Hardest problem](img/level11.png)

In this case, the third option of the first choice is the correct answer. This implies that you need to try 3 times if you do from left to right.

# Using the full formula

There are two ways of using the full formula, long form and short form. In both cases, ignore the shapes in the solver, they don't do anything. Both forms work for the GUI, command line and [web app](https://rubuky.com/tool/2024-09-23-SwitchChallenge/).

In the long form, you enter the input and output colors.

Let's use the hard case as an example, the formula would be:

`ybgr+1324+x+3241=gbyr`

![Long Formula with GUI](img/lf.png)

The gist of the short formula form is that you encode the outcome (number after `=`) in such a way that it is a single switch from the input to the output. Note that you cannot use the short formula for the easiest problems (you solve it with your brain).

Let's use the hard case as an example:

![Short Formula with GUI](img/ff_GUI.png)

As the shapes are now redundant, you may want to use the command line, which is more light-weight:

![Short Formula with command line](img/ff_cl.png)

You can also access the web app! [Click here](https://rubuky.com/tool/2024-09-23-SwitchChallenge/)

![Short Formula with web app](img/ff_web.png)

