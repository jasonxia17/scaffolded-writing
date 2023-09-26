## Using Context-Free Grammars to Scaffold and Automate Feedback in Precise Mathematical Writing

This repo contains the implementation of tool described in this [paper](https://zilles.cs.illinois.edu/papers/xia_CFG_writing_grading_sigcse23.pdf).

If you want to try out the tool without running this code locally, you can do so on this [website](https://scaffoldedwriting.pythonanywhere.com/).

We also have a [video presentation](https://dl.acm.org/doi/10.1145/3545945.3569728#sec-supp) that demonstrates how a student would use the tool.

### Abstract

In technical writing, certain statements must be written very carefully in order to clearly and precisely communicate an idea. Students are often asked to write these statements in response to an open-ended prompt, making them difficult to autograde with traditional methods. We present what we believe to be a novel approach for autograding these statements by restricting students' submissions to a pre-defined context-free grammar (configured by the instructor). In addition, our tool provides instantaneous feedback that helps students improve their writing, and it scaffolds the process of constructing a statement by reducing the number of choices students have to make compared to free-form writing. We evaluated our tool by deploying it on an assignment in an undergraduate algorithms course. The assignment contained five questions that used the tool, preceded by a pre-test and followed by a post-test. We observed a statistically significant improvement from the pre-test to the post-test, with the mean score increasing from 7.2/12 to 9.2/12.

### Setup for Local Development

You'll need Python 3.9 to run this locally.

Clone the repository, then run `pip install -r requirements.txt`. Next, run `python3.9 server.py`, go to http://localhost:5000/, and you should be able to start playing with the tool. Enjoy!
