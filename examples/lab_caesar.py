
class EvalCryptoLab( EvalLab ):

  def __init__( self, student_name, student_dir, instructor_dir, score_list_file, student_id=None ):
    super().__init__( student_name, student_dir, instructor_dir, score_list_file, student_id=student_id )
    ## to include the intercepted message
    ## import of modules is not effective here and is performed during each evaluation
#    caesar_solution = import_module( 'caesar_solution' )
#    caesar = import_module( 'caesar' )
#    substitution_solution = import_module( 'substitution_solution' )
#    substitution = import_module( 'substitution' )
#    invalidate_caches()
    
    self.pdf_question_number_list = [ 1, 4, 6, 7, 10, 12, 13 ] # queston number expected in the PDF, i.e non python

  def eval_question( self, question_number, score=None ):
    """ set score to question question_number 
 
    When score is not set to None the score value is assigned otherise an evaluation is performed.

    Todo:
    This function shoudl be placed in the parent class and involve a dictionary of functions.
    """
    print( "-- Evaluation Question %s"%question_number )
    if score is None:
      if question_number == 2:
        try:
          with Timeout(5):
            score = self.eval_q2()
        except Exception:
          print( traceback.format_exc() )
          score = 0
      elif question_number == 3:
        try:
          with Timeout(5):
            score = self.eval_q3()
        except Exception:
          print( traceback.format_exc() )
          score = 0
      elif question_number == 5:
        try:
          with Timeout(5):
            score = self.eval_q5()
        except Exception:
          print( traceback.format_exc() )
          score = 0
      elif question_number == 8:
        try:
          with Timeout(5):
            score = self.eval_q8()
        except Exception:
          print( traceback.format_exc() )
          score = 0
      elif question_number == 9:
        try:
          with Timeout(5):
            score = self.eval_q9()
        except Exception:
          print( traceback.format_exc() )
          score = 0
      elif question_number == 11:
        try:
          with Timeout(5):
            score = self.eval_q11() 
        except Exception:
          print( traceback.format_exc() )
          score = 0
      else:
        try: # avoid overwriting if already set
          score = self.student_score[ "Question %i"%question_number ]
        except KeyError:
          score = None
    self.student_score[ "Question %i"%question_number ] = score
     
  def eval_q2( self ):
    max_points = 3
    import caesar 
##    reload( caesar )
    import caesar_solution
    print( "\n# Q2:\n")
    print( f"q2 caesar : {caesar.__file__}" )
    print( f"q2 caesar_solution : {caesar_solution.__file__}" )
    score = 0
    print( f"\na) Testing lower case letter encryption" )
    try: 
      key = random.randint( 0, 25 )
      for clear_text in [ chr( ord( 'a' ) + i ) for i in range( 26 ) ]:
        if caesar_solution.encrypt(clear_text, key) != caesar.encrypt(clear_text, key):
          raise ValueError( "encrypt does not decrypt correctly %s"%clear_text )
    except Exception as e:
      print( "  - ERROR: unable to encrypt a-z with key: %s --%s"%( key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    ## testing A-Z letters encryption
    print( f"\nb) Testing lower case letter encryption" )
    try: 
      key = random.randint( 0, 25 )
      for clear_text in [ chr( ord( 'A' ) + i ) for i in range( 26 ) ]:
        print( f"clear_text: {clear_text} with key {key}"
               f" solution: {caesar_solution.encrypt(clear_text, key)}\n"
               f" test: {caesar.encrypt(clear_text, key)} " ) 
        if caesar_solution.encrypt(clear_text, key) != caesar.encrypt(clear_text, key):
          raise ValueError( "encrypt does not decrypt correctly %s"%clear_text )
    except Exception as e:
      print( "  - ERROR: unable to encrypt A-Z with key: %s --%s"%( key, e ) )
    else:
      score += 1 * max_points / 4
      print( "  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    ## testing word encryption
    print( f"\nc) Testing word encryption" )
    try: 
      key = random.randint( 0, 25 )
      clear_text = "europe" 
      if caesar_solution.encrypt(clear_text, key) != caesar.encrypt(clear_text, key):
        raise ValueError( "encrypt does not decrypt correctly %s"%clear_text )
    except Exception as e:
      print( "  - ERROR: unable to encrypt \' %s\'  with key: %s --%s"%( clear_text, key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    ## testing text encryption with not a-Z characteres
    print( f"\nd) Testing text paragraph decryption" )
    try: 
      key = random.randint( 0, 25 )
      clear_text = "Tous les êtres humains naissent libres et égaux en dignité et en droits. Ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité." 
      if caesar_solution.encrypt(clear_text, key) != caesar.encrypt(clear_text, key):
        raise ValueError( "ERROR: encrypt does not decrypt correctly %s"%clear_text )
    except Exception as e:
      print( "  - ERROR: unable to encrypt \' %s\'  with key: %s --%s"%( clear_text, key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    return score

  def eval_q3( self ):
##    reload( caesar )
    import caesar 
    import caesar_solution
    max_points = 1
    score = 0
    print( "\n# Q3:\n")
    ## testing a-z letters encryption
    print( f"\na) Testing lower case letter decryption" )
    try:
      key = random.randint( 0, 25 )
      for clear_text in [ chr( ord( 'a' ) + i ) for i in range( 26 ) ]:
        if caesar_solution.decrypt(clear_text, key) != caesar.decrypt( clear_text, key ):
          raise ValueError( "decrypt does not decrypt correctly %s"%clear_text )
        if caesar.decrypt( caesar.encrypt( clear_text, key), key ) != clear_text :
          raise ValueError( "decrypt(encrypt) does not return original clear_text" )
    except Exception as e:
      print( "  - ERROR: unable to decrypt a-z with key: %s -- %s"%( key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    ## testing A-Z letters encryption
    print( f"\nb) Testing lower case letter decryption" )
    try: 
      key = random.randint( 0, 25 )
      for clear_text in [ chr( ord( 'A' ) + i ) for i in range( 26 ) ]:
        if caesar_solution.decrypt(clear_text, key) != caesar.decrypt(clear_text, key):
          raise ValueError( "decrypt does not decrypt correctly %s"%clear_text )
        if caesar.decrypt( caesar.encrypt( clear_text, key), key ) != clear_text.lower() :
          raise ValueError( "decrypt(encrypt) does not return original clear_text" )
    except Exception as e:
      print( "  - ERROR: unable to decrypt A-Z with key: %s --%s"%( key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    ## testing word encryption
    print( f"\nc) Testing word decryption" )
    try: 
      key = random.randint( 0, 25 )
      clear_text = "europe" 
      if caesar_solution.decrypt(clear_text, key) != caesar.decrypt(clear_text, key):
        raise ValueError( "encrypt does not decrypt correctly %s"%clear_text )
        if caesar.decrypt( caesar.encrypt( clear_text, key), key ) != clear_text.lower() :
          raise ValueError( "decrypt(encrypt) does not return original clear_text" )
    except Exception as e:
      print( f"  - ERROR: unable to decrypt \' %s\'  with key: %s --%s"%( clear_text, key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    ## testing text encryption with not paragraph
    print( f"\nd) Testing text paragraph decryption" )
    try: 
      key = random.randint( 0, 25 )
      clear_text = "Tous les êtres humains naissent libres et égaux en dignité et en droits. Ils sont doués de raison et de conscience et doivent agir les uns envers les autres dans un esprit de fraternité." 
      if caesar_solution.encrypt(clear_text, key) != caesar.encrypt(clear_text, key):
        raise ValueError( "encrypt does not decrypt correctly %s"%clear_text )
      if caesar.decrypt( caesar.encrypt( clear_text, key), key ) != clear_text.lower() :
        raise ValueError( "decrypt(encrypt) does not return original clear_text" )
    except Exception as e:
      print( "  - ERROR: unable to encrypt \' %s\'  with key: %s --%s"%( clear_text, key, e ) )
    else:
      score += 1 * max_points / 4
      print( f"  - SUCCESS: test successfully passed - {1 * max_points / 4} points" )
    return score


  def eval_q5( self ):
##    reload( caesar )
    import caesar 
    import caesar_solution
    intercepted_message = caesar_solution.intercepted_message
#    score = 0
    ref_brute_force_dict = caesar_solution.brute_force( intercepted_message )
    brute_force_dict = caesar.brute_force( intercepted_message )
#    print( f"ref_brute_force dictionary: {ref_brute_force_dict}\n" )
    print( "\n# Q5:\n")
    print( f"brute_force dictionary: {brute_force_dict}" )
    return self.compare_dict( ref_brute_force_dict , brute_force_dict, 2.5)
##    if ref_brute_force_dict == brute_force_dict :
##      score += 2.5
##      print( "  - SUCCESS: test successfully passed" )
##    return score
##    else:
##      print( f"  - ERROR:  brute_force_dict is not as expected.")
##      if len( ref_brute_force_dict ) != len( brute_force_dict ) :
##        print( f"    brute_force_dict has an unexpected length" )
##      if type( list( ref_brute_force_dict.values() )[ 0 ] ) != type( list( brute_force_dict.values() )[ 0 ] ) :
##        print( f"    brute_force_dict values have unexpected type (expecting {type( list( brute_force_dict.values() )[ 0 ] )})" )
##      if type( list( ref_brute_force_dict.keys() )[ 0 ] ) != type( list( brute_force_dict.keys() )[ 0 ] ) :
##        print( f"    brute_force_dict keys have unexpected type (expecting {type( list( brute_force_dict.keys() )[ 0 ] )})" )
##        
##    return score

  def eval_q8( self ):
##    reload( substitution )
    import substitution
    import substitution_solution
    print( "\n# Q8:\n")
    with open( join( self.instructor_dir, 'clear_text_hugo.txt' ), 'rt', encoding="utf8" ) as f:
      clear_text_hugo = f.read()
    score = 0
    freq = substitution.freq_text( clear_text_hugo )[:10]
    ref_freq = substitution_solution.freq_text( clear_text_hugo )[:10]
##    print( f"ref_frequence: {ref_freq}\n" 
##           f"frequence: {freq}"  )
    if freq == ref_freq :
      score += 4
      print( "  - SUCCESS: test successfully passed - 4 points" )
    else:
      print( f"  - ERROR:  freq[ :10] is not as expected - {freq[ :10]}. ")
    if len( freq ) != len( ref_freq ) :
      print( f"    unexpected length" )
    if type( freq[0] ) != type( ref_freq[ 0 ] ):
      print( f"    unexpected type element (expecting {type(ref_freq[ 0 ])})"\
             f"with ( {type(ref_freq[ 0 ][0])} , {type(ref_freq[ 0 ][1])})" )
   
##      if type( list( ref_brute_force_dict.values() )[ 0 ] ) != type( list( brute_force_dict.values() )[ 0 ] ) :

    return score

  def eval_q9( self ):
##    reload( substitution )
    import substitution
    import substitution_solution
    print( "\n# Q9:\n")
    with open( join( self.instructor_dir, 'cipher_text_1.bin' ), 'rb', encoding=None ) as f:
      cipher_text_1 = f.read()
    score = 0
    freq = substitution.freq_cipher( cipher_text_1 )[:10]
    ref_freq = substitution_solution.freq_cipher( cipher_text_1 )[:10]
#    print( f"frequence: {ref_freq}" )
    if freq == ref_freq :
      score += 4
      print( "  - SUCCESS: test successfully passed - 4 points" )
    else:
      print( f"  - ERROR:  freq[ :10] is not as expected - {freq[ :10]}. ")
    if len( freq ) != len( ref_freq ) :
      print( f"    unexpected length" )
    if type( freq[0] ) != type( ref_freq[ 0 ] ):
      print( f"    unexpected type element (expecting {type(ref_freq[ 0 ])})"\
             f"with ( {type(ref_freq[ 0 ][0])} , {type(ref_freq[ 0 ][1])})" )
    return score

  def eval_q11( self ):
##    reload( substitution )
    import substitution
    import substitution_solution
    with open( join( self.instructor_dir, 'clear_text_hugo.txt' ), 'rt', encoding="utf8" ) as f:
      clear_text_hugo = f.read()
    with open( join( self.instructor_dir, 'cipher_text_1.bin' ), 'rb', encoding=None ) as f:
      cipher_text_1 = f.read()
    score = 0
    key_size=5
    freq_clear_text = substitution_solution.freq_text( clear_text_hugo )[:15]
    freq_cipher_text = substitution_solution.freq_cipher( cipher_text_1 )[:15]
    decryption_key = substitution.build_decryption_key( freq_clear_text, freq_cipher_text , key_size=key_size )
    ref_decryption_key = substitution_solution.build_decryption_key( freq_clear_text, freq_cipher_text, key_size=key_size )
#    print( f"ref_decryption key: {ref_decryption_key}\n" 
    print( f"\na) Testing decryption key" )
    print( f"decryption key: {decryption_key}" )
    if decryption_key == ref_decryption_key : 
      score += 1
      print( "  - SUCCESS: test successfully passed - 1 points" )
    else:
      print( f"  - ERROR:  decryption_key")
    ref_decryption_key = substitution_solution.build_decryption_key( freq_clear_text, freq_cipher_text, key_size=key_size )
    clear_text = substitution.guess_clear_text( cipher_text_1, ref_decryption_key ) 
    ref_clear_text = substitution_solution.guess_clear_text( cipher_text_1, ref_decryption_key ) 
#    ref_clear_text2 = substitution_solution.guess_clear_text2( cipher_text_1, ref_decryption_key ) 
#    print( f"clear_text: {ref_clear_text}" )
    print( f"\nb) Testing clear_text" )
   
    if clear_text == ref_clear_text:
      print( "  - SUCCESS: test successfully passed - 4 points" )
      score += 4
    else: 
      print( f"  - ERROR:  unexpected clear_text: \n{clear_text}")
      if len( clear_text ) != len( ref_clear_text ):
        print( f"clear_text has an unexpected length" )
      if type( clear_text ) != type( ref_clear_text ):
        print( f"clear_text has an unexpected type (expecting {type( ref_clear_text )})" )
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
     
  def eval_py( self ):
    """ proceeds to the evaluation and pre-filled the evaluation file

    We need to move up this function and define appropriated environement variables.
    We do not need to differentiate between pdf and py related question.
    As modules are imported for every question, this will generate an exception and a 0 score. 
    """
    for question_nbr in range( 13 ):
      self.eval_question( question_nbr + 1) 
   
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

