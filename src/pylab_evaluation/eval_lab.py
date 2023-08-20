import random
import os
from os.path import join, isdir, isfile, getsize, abspath
import sys
import json
import pyunpack
import shutil
from importlib import import_module, invalidate_caches, reload
import traceback
from cryptography.hazmat.primitives import hashes
import json
import signal, time
import subprocess
import shlex

class Timeout():
  """Timeout class using ALARM signal"""
  class Timeout(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    signal.alarm(0) # disable alarm

  def raise_timeout(self, *args):
    raise Timeout.Timeout()


class EvalLab:

  """ This class evaluates a student script from student_dir versus 
      a reference script from instructor_dir 

  """

  def __init__( self, lab_dir=None, ref_dir=None, json_score_list=None, lab_id=None ):

    self.init_lab_id( lab_id, lab_dir )
   
    ## file name where all scores are stored
    self.json_score_list = json_score_list
    if json_score_list is not None:
      self.json_score_list = abspath( json_score_list )
    
    ## dictionary listing the speicif cevaluation function for each 
    ## question usually of the the form:
    ## { 1 : self.eval_q1, 
    ##   3 : self.eval_q3, 
    ##   4 : self.eval_q4, ...
    if hasattr( self, 'eval_scheme' ) is False:
      self.eval_scheme  = { }
    ## { 1 :  { 'py' : 2            },
    ##   2 :  {           'pdf' : 1 },
    ##   3 :  { 'py' : 4            },
    ##   4 :  { 'py' : 4            },
    if hasattr( self, 'marking_scheme' ) is False:
      self.marking_scheme = {}

    ## initializes score and score list
    self.init_score( )
    
    ## update the path search so modules can be searched in 
    ## the appropriated directory.
    ## To avoid confusion we expect to have modules in the lab_dir
    ## and the ref_dir to have different names. 
    if lab_dir is not None:
      self.lab_dir = abspath( lab_dir )
      sys.path.insert(0, lab_dir)
    if ref_dir is not None:
      self.ref_dir = abspath( ref_dir )
      sys.path.insert(0, ref_dir)
    
  def init_lab_id( self, lab_id, lab_dir ):
    ## identifying the lab ( it is expected to identify the lab with the 
    ## studnet name but otherwise lab_dir can be used.
    if lab_id is not None:
      self.lab_id = lab_id
    else :
      self.lab_id = lab_dir
      if isinstance( self.lab_id, str ):
        self.lab_id = self.lab_id.replace( '/', '.' )
        for c in [ '{', '}', '(', ')', ' ', '[', ']', '!', '@',\
                   '#', '$', '%', '^', '&', '*' ]:
          self.lab_id = self.lab_id.replace( c , '' )


  def init_score( self ):
    """ initializes self.score_list and self.score """
    self.score_list = {}
    self.score = {}
    for key in self.marking_scheme.keys():
      self.score[ key ] = None

    ## if defined take values from the json file
    if self.json_score_list is not None:
      if isfile( self.json_score_list ):
        if getsize( self.json_score_list ) > 0:
          with open( self.json_score_list, 'r', encoding='utf8' ) as f:
            self.score_list = json.loads( f.read() )
          if self.lab_id in self.score_list.keys():
            score = self.score_list[ self.lab_id ] 
            ## kes of a json dictionary are keys while we are using 
            ## int top manipulate the question number.
            ## other keys are ignored
            for k, v in score.items():
              try:
                self.score[ int( k ) ] = v 
              except ValueError:
                pass

##  def eval_question( self, question_number ):
##    self.score[ "Question %i"%question_number ] = None

##  def eval_py( self ):
##    """ eval all questions involving python scripts """
##    pass

##  def dump_score( self ):
  def record_score( self ):
    self.score_list[ self.lab_id ] = self.score 
    with open( self.json_score_list, 'w' ) as f:
      f.write( json.dumps( self.score_list, indent=2 ) )
#    time.sleep( 2 )


  def compute_total_score( self ):
    """compute total score of the student (total and %) 
    """
    total_score = 0
##    print( f"self.score: {self.score}" )
    for k in list( self.score.keys() ):
      ## if not a question number ( total grade for example )
      if isinstance( k, int) is False:
        continue
      if self.score[ k ] is None:
        continue
      total_score += self.score[ k ]

    self.score[ "grade (total)" ] = total_score
##    print( f"self.score: {self.score}" )
    max_score = 0
    for q_nbr in self.marking_scheme.keys():
      if 'py' in self.marking_scheme[ q_nbr ] :
        max_score += self.marking_scheme[ q_nbr ][ 'py' ]
      if 'pdf' in self.marking_scheme[ q_nbr ] :
        max_score += self.marking_scheme[ q_nbr ][ 'pdf' ]

    if max_score != 0:
      self.score[ "grade (%)" ] = total_score / max_score * 100
    else:
      if  "grade (%)" in list( self.score.keys() ): 
        del self.score[ "grade (%)" ] 
      

  ## functions usefull to evaluate the script of the student 

  def log_error( self, msg ):
    """ print an error message """

    print( f"  - ERROR: {msg}" )

  def log_success( self, score=None ):
    """ print an success message """

    if score is None:
      print( f"  - SUCCESS: test successfully passed." )
    else: 
      print( f"  - SUCCESS: test successfully passed. You got {score} points" )


  def debug_dict( self, lab_dict, ref_dict ):
    """ perform specific test between dictionary objects  """
#    if ref_dict == lab_dict :
#      self.log_success( score=score )
#    else:
#      self.log_error( f"The tested dict is not as expected. "\
#                      f"Your score is 0 / {score} points. "\
#                      f"Please see details below.\n" \
#                      f"Tested dictionary: {lab_dict}" )
#      score = 0
    if len( ref_dict ) != len( lab_dict ) :
      self.log_error( f"    Tested dictionnary has an unexpected length" )
    ref_value_type = type( list( ref_dict.values() )[ 0 ] )
    value_type = type( list( lab_dict.values() )[ 0 ] ) 
    if ref_value_type != value_type :
      self.log_error( f"    Tested dictionary values have unexpected type (expecting {ref_value_type})" )
    ref_key_type = type( list( ref_dict.keys() )[ 0 ] )
    key_type = type( list( lab_dict.keys() )[ 0 ] )
    if ref_key_type != key_type :
      self.log_error( f"    Tested dictionary keys have unexpected type (expecting {ref_key_type})" )
#    return score

  def debug_list( self, lab_list, ref_list ): 
    """ performs specific tests for list, tuple """
    if len( ref_list ) != len( lab_list ) :
      self.log_error( f"    Tested List has an unexpected length" )
       

  def compare( self, obj, ref_obj, score, inspection_level=1):
    """ compare two objects and returns score if they match, 0 otherwise """
    indent = " " * 2 * inspection_level
    print( f"{indent}Evaluation {obj} versus the expected response (not revealed)" )
    ## printing inspection levl only when th elevel is >= 1
    if inspection_level != 1:
      print( f"{indent}Inspection level {inspection_level}" )
    if obj == ref_obj :
      if inspection_level == 1:
        self.log_success( score=score )
    else:
      if inspection_level == 1:
        self.log_error( f"{indent}The object is not as expected. "\
                        f"Your score is 0 / {score} points. "\
                        f"Please see details below.\n" \
                        f"Tested Object: {obj}" )
      score = 0
      if type( obj ) != type( ref_obj ):
        self.log_error( f"{indent}    Tested Object has unexpected type - "\
                        f"expecting {type(ref_obj)}" )
      else:
        if isinstance( obj, dict ):
          self.debug_dict( obj, ref_obj )
        elif isinstance( obj, ( list, tuple ) ) :
          self.debug_list( obj, ref_obj )
          for i in range( max( len( obj ), len( ref_obj ) ) ):
            self.compare( obj[ i ], ref_obj[ i ], silent_mode=True )
    return score


  def eval_single_py( self, question_number ):
    """ executes eval_q and report the question credit to the lab score
    sets an environement so the evalutaion of the question (eval_q)
    can be executed and the credit associated to the question reported
    """
    if isinstance( self.score[ question_number ], ( int, float ) ) is False: 
      print( f"\n### Evaluation of Question {question_number}###\n" )
      try:
        with Timeout(5):
           score = self.eval_scheme[ question_number ]() 
      except Exception:
        print( traceback.format_exc() )
        score = 0
      self.score[  question_number ] = score

  def eval_py( self ):
    """ evaluates all lab scripts """
    for q_nbr in self.eval_scheme.keys() :
      self.eval_single_py( q_nbr )
    self.compute_total_score(  )
    self.record_score( )
    print( f"\n\n ## Temporary score: ##" )
    print( self.score )

  def run_eval_py( self, eval_dir='./', module_dir=None ):
    """ write and run a script that performs eval_py 
 
    It basically consists in recreating it self into a separte process.
    The main problem we want to solve here is to run in a new environement 
    eval_py to ensure that appropriated modules have been loaded. 
    
    at the time of writting, we were not entirely sure that:
      1) forking even in a spawn mode does not inherit from loaded modules as being loaded in some context. This should not be the case.
      2) sys.path is not inherited. Inherited or not, it did not appear obvious to insert he propoer value in the child process - and eventually removing such initialization from the __init__ function.
    """
      
    pyfile = join( eval_dir, f"{self.lab_id}_eval.py" )
    logfile = join( eval_dir, f"{self.lab_id}_eval.log" )
#    print( f"Evaluating {student_name} - {filename}" )
    ## because we import modules for each student and it is messy to 
    ## reload different version of the module, we generate a python file
    ## to get a clean environment
    with open( pyfile, 'wt', encoding="utf8" ) as f:
      if module_dir is not None:
        f.write("import sys\n" )
        f.write(f"sys.path.insert( 0, '{module_dir}' )\n" )
      ## this is were we currenlty have the evaluation modules 
      ## should be removed at some point
      f.write( f"import {self.__module__} \n\n" )
      f.write( f"lab = {self.__module__}.{self.__class__.__name__}( '{self.lab_dir}', '{self.ref_dir}', json_score_list='{self.json_score_list}', lab_id='{self.lab_id}' )\n" )
      f.write( "lab.eval_py() \n")
    ## execute python3 pyfile
    try:
      p = subprocess.Popen( f"python3 {pyfile} > {logfile}", shell=True )
##    time.sleep( 1 )  
#      p.wait( timeout=5 )
#      p.communicate( timeout=5 )
#      while p.returncode is None: # not terminated
#        time.sleep( 2 )
      p.wait()
      time.sleep( 1 )
#      subprocess.run( shlex.split( f"python3 -m {pyfile} > {logfile}" ), shell=True, timeout=5 )
#      p.run( timeout=5 )     
    except subprocess.TimeoutExpired:
      pass
#    time.sleep( 2 )

