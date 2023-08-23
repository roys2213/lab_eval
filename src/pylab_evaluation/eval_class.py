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
import binascii
import math
import time
from pylab_evaluation import eval_lab

class EvalClass:

#  def __init__( self, moodle_dir, evaluation_dir, instructor_dir ):
#  def __init__( self, class_dir='./', instructor_dir=None, eval_lab_class=eval_lab.EvalLab, eval_lab_class_dir=None, student_db=None ):
  def __init__( self, class_dir='./', instructor_dir=None, eval_lab_class=eval_lab.EvalLab, eval_lab_class_dir=None, student_db=None ):
    """ evaluates the labs 

    This class assumes the following structure:
    project_dir:
      +- grade_list.json 
      +- moodle_dir
          +- student1-firstname__last_name
          +- student2-firstname__last_name
          +- student3-firstname__last_name
          +- student3-firstname__last_name
      +- lab_dir
        +- student1-firstname_last_name_id
        +- student2-firstname_last_name_id
        +- student3-firstname_last_name_id
        +- student3-firstname_last_name_id
      +- log_dir
        +- student1-firstname_last_name_id.log
    """

    self.class_dir = abspath( class_dir )
    self.json_lab_grade_list = join( self.class_dir, 'lab_grade_list.json' )
    self.moodle_dir = join( self.class_dir, 'moodle' )
    self.lab_dir = join( self.class_dir, 'lab' )
    self.eval_dir = join( self.class_dir, 'eval_dir' )
    self.instructor_dir = instructor_dir
    if self.instructor_dir is not None:
       self.instructor_dir = abspath( self.instructor_dir )
    self.eval_lab_class = eval_lab_class
    self.eval_lab_class_dir = eval_lab_class_dir
    if self.eval_lab_class_dir is not None:
      self.eval_lab_class_dir = abspath( self.eval_lab_class_dir )
    self.student_db = student_db
    

  def create_dir( self, directory, force=False ):
    """ remove existing dir and creates a clean directory """
    if isdir( directory ) is False:
      os.makedirs( directory )
    else: 
      if len(os.listdir( directory ) ) != 0:
        if force is False:
          raise ValueError( f"{directory} already exists -> re-creating it. "\
                            f"Please delete it. Note you can force the deletion "\
                            f"by setting force to True." )
        #raise ValueError( f" Testing {directory} already exists -> re-creating it."\
        #                f"TBD: activate shutil.rmtree( {directory} )" )
        shutil.rmtree( directory )
        os.makedirs( directory )

  def unzip_moodle( self, moodle_zip_file  ):
    """ created the moodle directory with all students submissions """
    if isfile( moodle_zip_file  ) is False:
      raise ValueError( "Unable to find {moodle_zip_file}" )
    self.create_dir( self.moodle_dir )
    pyunpack.Archive( moodle_zip_file ).extractall( self.moodle_dir )

  def lab_id_from_moodle_dir( self, dir_name ):
    if self.student_db is None :
      lab_id = dir_name
    else:
      lab_id = self.student_db.student_id_from_moodle_dir( dir_name )
    return lab_id


  def moodle_to_labs( self ):
    """ populates lab_dir from moodle_dir

    import considers the various ways a student can submit in moodle
    """
    ## Create the destination directory
    ## Note that import only works with empty destination directory because unziping th emoodle archive creates a directory which contains all student files and the files are then  moved to the expected destination.
    ## moodle.zip --> dst_dir/moodle/<all files>
    ## instead of moodle.zip --> dst_dir/<all files>
    ## We do not see this as an issue and create_dir takes this in charge. 
    ## If that were an issue we could: 
    ## - 1) identify dst_dir/moodle/ in a better way - even unzipping in /tmp. 
    ##  Currently it is identified as the unique directory which implies 
    ##  the initial destination directory is empty.
    ## - 2) see if extract does not hav eth eappropriated feature.
    ## create_dir
    self.create_dir( self.lab_dir )
    
    for dir_name in os.listdir( self.moodle_dir ):
      if isdir( join( self.moodle_dir, dir_name ) ) is False:
        continue
      #creating the same directory in lab_dir
      dst_dir = join( self.lab_dir, dir_name )
      os.makedirs( dst_dir )
      src_moodle_dir = join( self.moodle_dir, dir_name )
      moodle_file_list = os.listdir( src_moodle_dir )
      print( f"{src_moodle_dir} contains {moodle_file_list} " )
      if len( moodle_file_list ) == 1:
#        if moodle_file_list[ 0 ] is zipfile:
        src_moodle = join( src_moodle_dir, moodle_file_list [ 0 ] )
        if isfile( src_moodle ) and ( '.gzip' in src_moodle or \
                                      '.zip' in src_moodle or \
                                      '.tar' in src_moodle or \
                                      '.gz' in src_moodle or \
                                      '.rar' in src_moodle ): # a archive file gzip, tar, tar.gz, rar...
          pyunpack.Archive( src_moodle ).extractall( dst_dir )
          ## creates an additional directory
          ## moodle.zip --> dst_dir/moodle/<all files>
          ## instead of moodle.zip --> dst_dir/<all files>
          dst_file_list = os.listdir( dst_dir ) 
          unzip_dir = join( dst_dir, dst_file_list[ 0 ] ) 
          if len( dst_file_list ) == 1 and isdir( unzip_dir ):
            for file_name in os.listdir( unzip_dir ) :  
              shutil.move( join( unzip_dir, file_name ), join( dst_dir, file_name ) )
            print( f"{unzip_dir}: shutil.rmtree( unzip_dir )" )
#            shutil.rmtree( unzip_dir )
        elif isfile( src_moodle ) and ( '.py' in src_moodle or '.pdf' in src_moodle ):
          shutil.copy( src_moodle ,dst_dir )
        
        elif isdir( src_moodle ): # a directory that contains the files 
          for student_file_name in os.listdir( src_moodle ):
            shutil.copy( join( src_moodle, student_file_name ), 
                       join( dst_dir, student_file_name ) )
        else: 
          raise ValueError( f"{src_moodle} is not a file nor a directory" )
      else: # files are directly provided
        for file_name in moodle_file_list:
          if '.pdf' in file_name or '.py' in file_name:
            shutil.copy( join( src_moodle_dir, file_name ), 
                       join( dst_dir, file_name ) )

  def eval_py( self, force=False):
    if isfile( self.json_lab_grade_list ) is True:
      if force is True :
        raise ValueError( f"{self.json_lab_grade_list}: os.remove( self.json_lab_grade_list )" ) 
      else:
        response = input( f"Grades have already been recorded in the file "\
                          f"{self.json_lab_grade_list}.\n"\
                          f"To remove and re-run the evaluation type R.\n"\
                          f"Otherwise the evaluation will skip evaluation "\
                          f"aleary performed." )
        if response == 'R':
          raise ValueError( f"{self.json_lab_grade_list}: os.remove( self.json_lab_grade_list )" ) 
#          os.remove( self.json_lab_grade_list )

    if isdir( self.lab_dir ) is False:
      raise ValueError( f"Cannot perform lab evaluation lab_dir "\
        f"{self.lab_dir} not found." )
    for dir_name in os.listdir( self.lab_dir ):
      ## It seems that run_eval_py does not wait to be finished
#      time.sleep( 7 )
      lab = self.eval_lab_class( join( self.lab_dir, dir_name), \
                          self.instructor_dir, \
                          json_score_list=self.json_lab_grade_list, \
                          lab_id=self.lab_id_from_moodle_dir( dir_name ) )
      lab.run_eval_py( eval_dir=self.eval_dir, module_dir=self.eval_lab_class_dir )
      cmd = "lab_eval --conf conf_file"
      if 
#    time.sleep( 2 ) # ensures the lad_grade_list file is updated

  def detect_same_files( self,  file_name_list=[] ):
    """ reports identical files with same hash 
    args:
      file_name_list: contains a list of files that should be looked at. 
      By default all files are considered whic may include input files 
      present in multiple if not all directories. Such files are not subject 
      to duplicate detection.  
    """
    hash_dict = {} 
    for student_dir in os.listdir( self.lab_dir ):
      student_file_list = os.listdir( join( self.lab_dir, student_dir) )
      if file_name_list == []:
        file_name_list = student_file_list
      for file_name in student_file_list:
        if file_name not in file_name_list:
          continue
        with open( join( self.lab_dir, student_dir, file_name), 'rb' ) as f:
          digest = hashes.Hash(hashes.SHA256())
          digest.update( f.read() )
          h = digest.finalize()
          meta_data = { 'name' : student_dir, 'file' : file_name } 
          if h in hash_dict.keys():
            hash_dict[ h ].append( meta_data )
          else: 
            hash_dict[ h ] = [ meta_data ]
    ## removing hash with no collision
    for h in list( hash_dict.keys() ):
      if len( hash_dict[ h ] ) == 1 :
        del hash_dict[ h ]
    if len( hash_dict.keys() ) == 0:
      print( "No collisions detected: all files seems different" )
    else:
      print( "Some collisions between files have been detected" )
#      print( hash_dict )
      ## json does not take bytes
      print_hash_dict = {}
      for k in hash_dict.keys() :
        print_hash_dict[ f"{binascii.hexlify( k, sep=' ' )}"  ] = hash_dict[ k ] 
      print( json.dumps( print_hash_dict, indent=2 ) )
        


  def init_from_archive( self, moodle_zip_file ):
     """ create and overwritte the project 

     This is usually the step performed upon receiving scripts from the students.
     This steps is usually followed by an manual correction of evaluation of the
     grades - typically from a report. 
     """
     if isfile( moodle_zip_file ) is False:
       raise ValueError( f"Unexpected {moodle_zip_file}\n Expecting file." )

     self.create_dir( self.class_dir, force=True )
     for directory in [ self.class_dir, self.moodle_dir, \
                        self.lab_dir, self.eval_dir ]:
       if isdir( directory ) is False:
         os.makedirs( directory )
     self.unzip_moodle( moodle_zip_file )
     self.moodle_to_labs( )
     self.detect_same_files()
     self.eval_py( self.eval_lab_class )


  def load_grade_list( self) :
    print( f"self.json_lab_grade_list: {self.json_lab_grade_list} ")
    with open( self.json_lab_grade_list, 'r', encoding='utf8' ) as f:
      content = json.loads( f.read() )
#    time.sleep( 2 )
    return content

  def record_grade_list( self, grade_list ):
    with open( self.json_lab_grade_list, 'w', encoding='utf8' ) as f:
      f.write( json.dumps( grade_list, indent=2 ) )
    time.sleep( 2 )

  def get_min_max_mean_grade( self ):

    grade_list = self.load_grade_list( )

    max_grade = 0
    min_grade = 0
    mean_grade = 0
    for lab_id in list( grade_list.keys() ):
      grade = grade_list[ lab_id ] 
      #lab = self.eval_lab_class( join( self.lab_dir, dir_name), \
      lab = self.eval_lab_class( None, None, \
#                          self.instructor_dir, \
                          json_score_list=self.json_lab_grade_list, \
                          lab_id=lab_id )
      lab.compute_total_score( )
      grade_list[ lab_id ] = lab.score  
      total_grade = grade[ "grade (total)" ]
      max_grade = max( total_grade, max_grade ) 
      min_grade = min( total_grade, min_grade ) 
      mean_grade += total_grade
    self.record_grade_list( grade_list )
    mean_grade /= len( grade_list )
    return min_grade, max_grade, mean_grade



  def finalize( self, h_mean=3.2/5*100, h_std=1 ):
    """Finalizes the grades and provides an estimation so grades have the
       specified mean value.
    
    """
    min_grade, max_grade, mean_grade = self.get_min_max_mean_grade()
    print( f"min: {min_grade}, max: {max_grade}, mean: {mean_grade}" )
#    with open( self.json_lab_grade_list, 'r', encoding='utf8' ) as f:
#      score_list = json.loads( f.read() )
    grade_list = self.load_grade_list( )
#    elab = eval_lab.EvalLab( )
    std = 0
    std_perc = 0
    mean_grade_perc = 0
    for lab_id in list( grade_list.keys() ):
      grade = grade_list[ lab_id ] 
      #lab = self.eval_lab_class( join( self.lab_dir, dir_name), \
#      lab = self.eval_lab_class( None, None, \
##                          self.instructor_dir, \
#                          json_score_list=self.json_lab_grade_list, \
#                          lab_id=lab_id )
#      lab.compute_total_score( )
#      print( f"score: {score}" )
#      score_list[ lab_id ] = lab.score  
      if "grade (%)" not in list( grade.keys() ):
        grade[ "grade (%)" ] = grade[ "grade (total)" ] / max_grade * 100.0
      mean_grade_perc += grade[ "grade (%)" ]
      std += grade[ "grade (total)" ] ** 2
      std_perc += grade[ "grade (%)" ] ** 2
      grade_list[ lab_id ] = grade

    n = len ( list( grade_list.keys() ) )
    mean_grade_perc /= n
    std -= mean_grade ** 2
    std_perc -= mean_grade_perc ** 2
    std = math.sqrt( std )
    std_perc = math.sqrt( std_perc )
    if n != 1: 
      std /=  n - 1
      std_perc /= n - 1

    for lab_id in list( grade_list.keys() ):
      if std != 0:
        grade = grade_list[ lab_id ]
        grade[ "h grade (total)" ] = h_std / std * ( grade[ "grade (total)" ] - mean_grade ) + h_mean
        grade[ "h grade (%)" ] = h_std / std * ( grade[ "grade (%)" ] - mean_grade_perc ) + h_mean
        grade_list[ lab_id ] = grade
    self.record_grade_list( grade_list )

  ## It would be good to define some functions to return:
  ## - the grades in an excel sheet (the specific format may be defined
  ##   from the one used by Genote)
  ## -  a report (pdf) 
  ## - plot the distribution ( frequencies, histograms)
  ## - handle operations between classes.
  ## Note that all these function actually work on the json file
  def xls( self, student_list:list=[] ):
    pass

  def notify_students( self, ):
    pass  

class StudentDB:
   
  def __init__( self, json_file_name ):
    """ student DB can be extracted in a json format from moodle """
    self.json_file_name = json_file_name
    if isfile( json_file_name ):
      with open( json_file_name, 'rt', encoding='utf8' ) as f:
       ## the list of student  extracted by moodle is actually a list of list
       ## [[ {student_1}, {student_2},... ]] so we take the the first element.
        self.db = json.loads( f.read( ) )[ 0 ] 
#        print( f"student_db: {self.db}" ) 
 
  def search( self, first_name=None, last_name=None ):
    for student in self.db :
      if student[ 'firstname' ] == first_name and student[ 'lastname' ] == last_name:
        return student
    raise ValueError( f"Student with firstname {first_name} and lastname"\
                      f" {last_name} not found." )

  def student_id_from_moodle_dir( self, dir_name ):
    """ provides a unique id associated to the student given a 
        student directory assigned by moodle 
    """
    dir_name = dir_name.split( ',' )
    last_name = dir_name[ 0 ].replace( '_', ' ' )
    last_name = last_name.strip( )
    reminder = dir_name[ 1 ][ 1 : ].split( '_' )[ : -4 ]
    first_name = reminder[ 0 ]
    if len( reminder ) > 1 :
      for s in reminder [ 1 : ]:
        first_name += f" {s}"
    first_name.strip() 
    student = self.search( first_name=first_name, last_name=last_name )
    return student[ 'username' ]



