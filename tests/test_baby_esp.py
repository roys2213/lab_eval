import json 

def test_singlelab( ):
  """Testing evaluation of a single lab """
  import sys
  sys.path.insert(0, '../examples' )
  import lab_babyesp
  lab = lab_babyesp.EvalBabyESP( \
    ## directory where the students' scripts are located
    './test_single_lab/student', \
    ## directory where the instructor's scripts are located 
    './test_single_lab/ref', \
    ## file that centralizes (all students) evaluation 
    json_score_list='./test_single_lab/score_list.json', \
    ## lab identifier (or student username)
    lab_id='john_doe' )
  #lab.eval_py( )
  lab.run_eval_py( eval_dir='./test_single_lab/evaluation', module_dir='../examples' )



def test_class( ):
  """Testing evaluation of a class"""

  from pylab_evaluation import eval_class
  import sys
  sys.path.insert(0, '../examples' )
  import lab_babyesp

  ## instantiate the student db: This is usefull to be able to 
  ## bind properly the lab to a student. 
  ## It would be good the log can be sent to the student (by email)
  student_db = eval_class.StudentDB( './test_class/courseid_29228_participants.json')
  eval_class = eval_class.EvalClass( \
    ## the main directory with all information
    './baby_esp22', 
    ## directory where the instructor's scripts are located 
    './test_single_lab/ref',\
    ## The class that defines the lab
    lab_babyesp.EvalBabyESP, \
    ## directory where the module can be found - only usefull when 
    ## the class cannot be found by python
    eval_lab_class_dir = '../examples',
    ## student DB
    student_db=student_db )
 
  ## evaluates all python3 scripts
  eval_class.init_from_archive( './test_class/moodle_archive.zip' )
  ## Eventually edit './baby_esp22/score_list.json' to manualy adjust the 
  ## grades or perform questions that are not related to the script evaluations
  ## like evaluation of the report.
  ## BEGIN simulating manual revision:
  with open( './baby_esp22/lab_grade_list.json', 'r', encoding='utf8' ) as f:
    score_list = json.loads( f.read() )
  for lab_id in score_list.keys():
    for k in list( score_list[ lab_id ].keys() ):
      if score_list[ lab_id ][ k ] is None:
        score_list[ lab_id ][ k ] = 0
  with open( './baby_esp22/lab_grade_list.json', 'w', encoding='utf8' ) as f:
    f.write( json.dumps( score_list, indent=2 ) )
  ## END simulating manual revision:

  eval_class.finalize( )


if __name__ == '__main__' :
#  test_singlelab( )
  test_class( )
