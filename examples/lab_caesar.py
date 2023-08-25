from pylab_evaluation import eval_lab
from os.path import join 
import random 
import sys

class EvalCaesarLab( eval_lab.EvalLab ):

  def __init__( self, lab_dir=None, ref_dir=None, json_score_list=None, lab_id=None ):
    """ Evaluates the Crypto Lab

    Args:
      lab_dir: the directory that contains the scripts to be 
        evaluated, that is the scripts provided by the student
      ref_dir: directory that contaims the reference scripts, 
        that is those of the instructor  
      json_score_list:
      lab_id: designates how we want to identify the instance 
        of the lab being evaluated. In many cases, this is the
        student name. When that argument is not provided, the 
        directory is used. to identify the lab.  

    Note: It is important to have the lab_dir and ref_dir to 
    be instantiated with a default value None. This makes it
    possible to instantiates the class without any argument.
    We need to do so when we evaluate the grades from the 
    scores as the grades are computed from the marking scheme.  
    """
    # questiuon number { 'pdf' : points associated to the report,
    #                    'py' : points associated to code }
    self.marking_scheme = {   1 :  {             'pdf' : 2 },
                              2 :  { 'py' : 3              },
                              3 :  { 'py' : 2              },
                              4 :  {             'pdf' : 4 },
                              5 :  { 'py' : 2.5, 'pdf' : 1 },
                              6 :  {             'pdf' : 3 },
                              7 :  {             'pdf' : 4 },
                              8 :  { 'py' : 4              },
                              9 :  { 'py' : 4              },
                              10 : {             'pdf' : 2 },
                              11 : { 'py' : 4              },
                              12 : {             'pdf' : 2 }, 
                              13 : {             'pdf' : 2 }}
    
    self.eval_scheme = { 2 : self.eval_q2,
                         3 : self.eval_q3,
                         5 : self.eval_q5,
                         8 : self.eval_q8,
                         9 : self.eval_q9,
                         11 : self.eval_q11 }
    super().__init__( lab_dir, ref_dir, \
                      json_score_list=json_score_list, lab_id=lab_id )

  def eval_q2( self ):
    import caesar 
    import caesar_solution
    score = 0
    print( f"\na) Testing lower case letter (a-z) encryption" )
    key = random.randint( 0, 25 )
    for clear_text in [ chr( ord( 'a' ) + i ) for i in range( 26 ) ]:
      score+= self.compare( caesar.encrypt(clear_text, key), \
                            caesar_solution.encrypt(clear_text, key), 1 / 26 )
  
    print( f"\nb) Testing upper case letter (A-Z) encryption" )
    key = random.randint( 0, 25 )
    for clear_text in [ chr( ord( 'A' ) + i ) for i in range( 26 ) ]:
      score+= self.compare( caesar.encrypt(clear_text, key), \
                            caesar_solution.encrypt(clear_text, key), 1 / 26 )

    print( f"\nc) Testing word encryption" )
    key = random.randint( 0, 25 )
    clear_text = "canada"
    score+= self.compare( caesar.encrypt(clear_text, key), \
                          caesar_solution.encrypt(clear_text, key), 1 )

    print( f"\nd) Testing text paragraph decryption" )
    key = random.randint( 0, 25 )
    clear_text = "Tous les êtres humains naissent libres et égaux en dignité et en droits. Ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité." 
    score+= self.compare( caesar.encrypt(clear_text, key), \
                          caesar_solution.encrypt(clear_text, key), 1 )
    return score

  def eval_q3( self ):
    ## 2 points over 8 tests   
    import caesar 
    import caesar_solution
    
    score = 0
    print( f"\na) Testing lower case letter (a-z) decryption" )
    key = random.randint( 0, 25 )
    for clear_text in [ chr( ord( 'a' ) + i ) for i in range( 26 ) ]:
      score+= self.compare( caesar.decrypt(clear_text, key), \
                            caesar_solution.decrypt( clear_text, key ),\
                            2 / 7 / 26 )

    print( f"\nb) Testing lower case letter (a-z) decryption(encryption) = identity" )
    for clear_text in [ chr( ord( 'a' ) + i ) for i in range( 26 ) ]:
      score+= self.compare( caesar.decrypt( \
                              caesar.encrypt( clear_text, key), key ),\
                            clear_text, 2 / 7 / 26 )

    print( f"\nc) Testing upper case letter (A-Z) decryption" )
    key = random.randint( 0, 25 )
    for clear_text in [ chr( ord( 'A' ) + i ) for i in range( 26 ) ]:
      score+= self.compare( caesar.decrypt( clear_text, key ), \
                            caesar_solution.decrypt( clear_text, key ), \
                            2 / 7 / 26 )

    print( f"\nd) Testing lower case letter (A-Z) decryption(encryption) = identity" )
    for clear_text in [ chr( ord( 'A' ) + i ) for i in range( 26 ) ]:
      score+= self.compare( caesar.decrypt( \
                              caesar.encrypt( clear_text, key ), key ),\
                            clear_text.lower(), 2 / 7 / 26 )

    print( f"\ne) Testing word decryption" )
    key = random.randint( 0, 25 )
    clear_text = "canada"
    score+= self.compare( caesar.decrypt(clear_text, key ), \
                          caesar_solution.decrypt(clear_text, key), 2 / 7  )

    print( f"\nf) Testing word encryption( decryption )" )
    score+= self.compare( caesar.decrypt( \
                            caesar.encrypt( clear_text, key ), key ),\
                          clear_text.lower(), 2 / 7  )

    print( f"\ng) Testing text paragraph decryption" )
    key = random.randint( 0, 25 )
    clear_text = "Tous les êtres humains naissent libres et égaux en dignité et en droits. Ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité."
    score+= self.compare( caesar.decrypt(clear_text, key), \
                          caesar_solution.decrypt( clear_text, key ), 2 / 7 )

##    print( f"\nh) Testing word encryption( decryption )" )
##    This does not work because of the upper letters are converted 
##    to lower as well as bevause special characters are not considered.
##    score+= self.compare( caesar.decrypt( \
##                            caesar.encrypt( clear_text, key), key ),\
##                          clear_text, 2 / 8 )
    return score


  def eval_q5( self ):
    import caesar 
    import caesar_solution
    intercepted_message = caesar_solution.intercepted_message
    ref_brute_force_dict = caesar_solution.brute_force( intercepted_message )
    brute_force_dict = caesar.brute_force( intercepted_message )
    print( f"brute_force dictionary: {brute_force_dict}" )
    return self.compare( brute_force_dict, ref_brute_force_dict, 2.5)

  def eval_q8( self ):
    import substitution
    import substitution_solution
    with open( join( self.ref_dir, 'clear_text_hugo.txt' ), 'rt', encoding="utf8" ) as f:
      clear_text_hugo = f.read()
    score = 0
    freq = substitution.freq_text( clear_text_hugo )[:10]
    ref_freq = substitution_solution.freq_text( clear_text_hugo )[:10]
    return self.compare( freq , ref_freq, 4 )

  def eval_q9( self ):
    import substitution
    import substitution_solution
    with open( join( self.ref_dir, 'cipher_text_1.bin' ), 'rb', encoding=None ) as f:
      cipher_text_1 = f.read()
    score = 0
    freq = substitution.freq_cipher( cipher_text_1 )[:10]
    ref_freq = substitution_solution.freq_cipher( cipher_text_1 )[:10]
    return self.compare( freq , ref_freq, 4 )

  def eval_q11( self ):
    import substitution
    import substitution_solution
    with open( join( self.ref_dir, 'clear_text_hugo.txt' ), 'rt', encoding="utf8" ) as f:
      clear_text_hugo = f.read()
    with open( join( self.ref_dir, 'cipher_text_1.bin' ), 'rb', encoding=None ) as f:
      cipher_text_1 = f.read()
    score = 0
    key_size=5
    freq_clear_text = substitution_solution.freq_text( clear_text_hugo )[:15]
    freq_cipher_text = substitution_solution.freq_cipher( cipher_text_1 )[:15]
    decryption_key = substitution.build_decryption_key( freq_clear_text, freq_cipher_text , key_size=key_size )
    ref_decryption_key = substitution_solution.build_decryption_key( freq_clear_text, freq_cipher_text, key_size=key_size )
    print( f"\na) Testing decryption key" )
    print( f"decryption key: {decryption_key}" )
    score +=  self.compare( decryption_key, ref_decryption_key, 1 )

    if decryption_key == ref_decryption_key : 
      score += 1
      print( "  - SUCCESS: test successfully passed - 1 points" )
    else:
      print( f"  - ERROR:  decryption_key")
##    ref_decryption_key = substitution_solution.build_decryption_key( freq_clear_text, freq_cipher_text, key_size=key_size )
    clear_text = substitution.guess_clear_text( cipher_text_1, ref_decryption_key ) 
    ref_clear_text = substitution_solution.guess_clear_text( cipher_text_1, ref_decryption_key ) 
#    ref_clear_text2 = substitution_solution.guess_clear_text2( cipher_text_1, ref_decryption_key ) 
#    print( f"clear_text: {ref_clear_text}" )
    print( f"\nb) Testing clear_text" )
    q_score =  self.compare( clear_text, ref_clear_text, 4 )
    score += q_score
    if q_score != 4 :
      max_error = 10
      error_counter = 0 
      print( f"The following {max_error} are unexpected:" ) 
      for i in range( len( clear_text ) ):
        if clear_text[ i ] != ref_clear_text[ i ] :
          error_counter += 1
          if error_counter > max_error :
            break
          print( f" character {clear_text[ i ]} at position {i} is unexpected - expecting {ref_clear_text[ i ]}" )  
    return score
     
##  def eval_py( self ):
##    """ proceeds to the evaluation and pre-filled the evaluation file
##
##    We need to move up this function and define appropriated environement variables.
##    We do not need to differentiate between pdf and py related question.
##    As modules are imported for every question, this will generate an exception and a 0 score. 
##    """
##    for question_nbr in range( 13 ):
##      self.eval_question( question_nbr + 1) 
##   
##    try : ## import is limited to the function and is not share in the environment
##      caesar = __import__( 'caesar' )
##    except Exception as e:
##      print( "  - ERROR: Unable to import caesar module -- %s"%e )
##      for question_nbr in range( 6 ):
##        question_nbr += 1
##        if question_nbr in self.pdf_question_number_list:
##          self.eval_question( question_nbr ) # so PDF are created and set to None
##        else:
##          self.eval_question( question_nbr, score=0 ) # score set to 0
##        
##    else:
##      for question_nbr in range( 6 ):
##        self.eval_question( question_nbr + 1) 
##    try :
##      substitution = __import__( 'substitution' )
##    except Exception as e:
##      print( "  - ERROR: Unable to import substitution module -- %s"%e )
##      for question_nbr in range( 7 ):
##        question_nbr += 7
##        if question_nbr in self.pdf_question_number_list:
##          self.eval_question( question_nbr ) # so PDF are created and set to None
##        else:
##          self.eval_question( question_nbr, score=0 ) # score set to 0
##    else:
##      for question_nbr in range( 7 ):
##        self.eval_question( 7 + question_nbr ) 

