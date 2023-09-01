

lab_eval  evaluate python scripts submitted by student. 
The use case is as follows: 
Students have top complete a laboratory that includes python scripts. 
Each students submits the scripts and a report using (for example) moodle. 

This scripts takes the submission of the students and test automatically the scripts against those of the instructor. 
The evaluation results in a grade being assigned to each student as well as a log file that can be helpful to the student for debugging. 

# Installation

```
pip install eval_lab
```

```
$ git clone 
$ cd lab_eval
$ python3 -m build && pip3 install --force-reinstall dist/pylab_eval-0.0.2.tar.gz
```

# Usage Example

## Evaluating a single Labs

Evaluation of the caesar of the student

```
lab_eval_lab  --conf ~/gitlab/lab_eval/examples/lab_caesar.cfg ./labs/Firstname,_Lastname_5698747_assignsubmission_file_
```
In order to specify the output log file (toto.log):
Note that we assume that the lab_caesar.cfg specifies that output is placed in a log file by specifying the `log_dir`. This variable is usually commented, in which case, either we should uncomment it or specify it in the command line using `--log_dir <log_dir>`.

```
lab_eval_lab  --conf ~/gitlab/lab_eval/examples/lab_caesar.cfg --lab_id toto ./labs/Firstname,_Lastname_5698747_assignsubmission_file_
```
## Evaluation the class 

The configuration file is located in ~/gitlab/lab_eval/examples/lab_caesar.cfg and specifies the various locations of the necessary files:

* the instructir's python files (the solutions)
* the file that evaluates the student's scripts against the solutions lab_caesar.py
* the student database. The student data base is provided by moodle in "Participants" tab, "select all participants" export as JSON file.
* the labs submitted by the students "Consulted assignments" > "Download all assignments" - in our case  INF808-AI-Laboratoire1\ Attaques\ cryptographiques\ \(Remise\ des\ devoirs\)-2622297.zip


To run the evaluation from the moodle file


```
lab_eval_class  --conf ~/gitlab/lab_eval/examples/lab_caesar.cfg  --class_dir lab1   INF808-AI-Laboratoire1\ Attaques\ cryptographiques\ \(Remise\ des\ devoirs\)-2622297.zip 
```

In general, we expect that some question are evaluated manually. This can occurs when the lab combines code evaluation as well as a report evaluation. Once the report has been evaluated and the associated scores placed into the `score_list.json` file, we recompute the grades to consider the manually added scores as follows:

```
lab_finalize_grades  --conf ~/gitlab/lab_eval/examples/lab_caesar.cfg test_class_dir/score_list.json

```

# Configuration 

## Configuration file

Check the `lab_eval.git/examples/lab_caesar.cfg` as an example.

## StudentDB file



# Building the module to evaluate your own lab

please check `lab_eval.git/examples/lab_caesar.cfg` or `lab_eval.git/examples/lab_babyesp.cfg`





