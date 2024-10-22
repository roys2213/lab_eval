from lab_eval import eval_lab

class EvalBabyESPLab( eval_lab.EvalLab ):

  def __init__( self, lab_dir=None, ref_dir=None, json_score_list=None, lab_id=None ):

#  def __init__( self, lab_dir, ref_dir, json_score_list=None, lab_id=None ):
    # questiuon number { 'pdf' : points associated to the report, 
    #                    'py' : points associated to code } 
    self.marking_scheme = { 1 :  { 'py' : 2            }, 
                            2 :  {           'pdf' : 1 }, 
                            3 :  { 'py' : 4            }, 
                            4 :  { 'py' : 4            },
                            5 :  { 'py' : 1, 'pdf' : 1 }, 
                            6 :  {           'pdf' : 1 }, 
                            7 :  { 'py' : 2            },
                            8 :  { 'py' : 2            },
                            9 :  {           'pdf' : 1 },
                            10 : { 'py' : 4            }, 
                            11 : { 'py' : 2            } }
 
    self.eval_scheme = { 1 : self.eval_q1, 
                         3 : self.eval_q3, 
                         4 : self.eval_q4, 
                         5 : self.eval_q5, 
                         7 : self.eval_q7, 
                         8 : self.eval_q8, 
                         10 : self.eval_q10, 
                         11 : self.eval_q11 } 
    super().__init__( lab_dir, ref_dir, \
                      json_score_list=json_score_list, lab_id=lab_id )
                    
                        
  def eval_q1( self ):
    """ testing nonce_info """

    import aes_gcm     # import student script
    import ref_aes_gcm # import solution
    from Cryptodome.Cipher import AES
    from Cryptodome.Random import get_random_bytes

    key = get_random_bytes(16)
    alice_cipher = AES.new(key, AES.MODE_GCM,\
                       nonce=None, mac_len=16)
    nonce, nonce_len = aes_gcm.nonce_info( alice_cipher )
    ref_nonce, ref_nonce_len = ref_aes_gcm.nonce_info( alice_cipher )
    return  self.compare( nonce, ref_nonce, 1 ) +  self.compare( nonce_len, ref_nonce_len, 1 )
    
 

  def eval_q3( self ):
    """ testing encrypt_and_digest """

    import aes_gcm     # import student script
    import ref_aes_gcm # import solution
    from Cryptodome.Cipher import AES
    ## secret key shared by Alice and Bob
    key = b'\xf1\x6a\x93\x0f\x52\xa1\x9b\xbe\x07\x1c\x6d\x44\xb4\x24\xf3\x03'
    nonce_dict = {
      'nonce_0': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', \
      'nonce_1': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', \
      'nonce_2': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', \
      'nonce_3': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01' }
    clear_text = b"secret"
    output = aes_gcm.encrypt_and_digest( key, nonce_dict, clear_text )
    ref_output = ref_aes_gcm.encrypt_and_digest( key, nonce_dict, clear_text )
    return self.compare( output, ref_output, 4 )

  def eval_q4( self ):
    """ test show_nonce """
    import nonce
    import ref_nonce
    from Cryptodome.Random import get_random_bytes
    salt = get_random_bytes(4)
    score = 0
    seq_num = 0
    for ext_seq in [True, False]:
        byte_nonce, struct_nonce = nonce.show_nonce( salt, seq_num, ext_seq ) 
        ref_byte_nonce, ref_struct_nonce = ref_nonce.show_nonce( salt, seq_num, ext_seq )
        score += self.compare( byte_nonce, ref_byte_nonce, 1 ) 
        score += self.compare( struct_nonce, ref_struct_nonce, 1 )  
    return score


  def eval_q5( self ):
    """testing show_nonce 

    an additional point is provided in the report
    """
    import nonce
    import ref_nonce
    score = 0
    salt = b'\xf7\xca\x79\xfa'
    for seq_num in [5, 4294967295, 4294967296]:
      for ext_seq in [True, False]:
        byte_nonce, struct_nonce = nonce.show_nonce( salt, seq_num, ext_seq ) 
        ref_byte_nonce, ref_struct_nonce = ref_nonce.show_nonce( salt, seq_num, ext_seq )
        score += self.compare( byte_nonce, ref_byte_nonce, 1 )  
        score += self.compare( struct_nonce, ref_struct_nonce, 1 )  
    return score / 6.0 

  def eval_q7( self ):
    """ testing ciphers_obj """
    import cipher_obj
    import ref_cipher_obj

    key = b'\xf1\x6a\x93\x0f\x52\xa1\x9b\xbe\x07\x1c\x6d\x44\xb4\x24\xf3\x03'
    mac_len=16
    ext_seq_num_flag = False
    seq_num_counter = 5 
    salt = b'\xf7\xca\x79\xfa'
    alice = cipher_obj.ciphers_obj( key, mac_len, ext_seq_num_flag, seq_num_counter, salt ) 
    ref_alice = ref_cipher_obj.ciphers_obj( key, mac_len, ext_seq_num_flag, seq_num_counter, salt ) 
   
    alice_plaintext = b"yet another secret"
    ciphertext, icv = alice.encrypt_and_digest( alice_plaintext )
    ref_ciphertext, ref_icv = ref_alice.encrypt_and_digest( alice_plaintext )
#    print( "\n ### Testing alice.encrypt_and_digest( plaintext ): \n" )
#    print( f"  - ciphertext: {ciphertext}" )
#    print( f"  - icv: {icv}" )
#    print( f"  - ref_ciphertext: {ref_ciphertext}" )
#    print( f"  - ref_icv: {ref_icv}" )
    return self.compare( ( ciphertext, icv ), ( ref_ciphertext, ref_icv ), 2 )


  def eval_q8 (self ):
    import sa
    from binascii import hexlify
    ## The SA is instantiated both Alice and Bob
    alice_sa = sa.SA()
    ## AES_GCM_16_IIV related shared context between Alice and Bob
    alice_sa.esp_enc_alg = "ENCR_AES_GCM_16_IIV"
    alice_sa.esp_enc_key = b'\xf1\x6a\x93\x0f\x52\xa1\x9b\xbe\x07\x1c\x6d\x44\xb4\x24\xf3\x03'
    alice_sa.ext_seq_num_flag = False
    alice_sa.seq_num_counter = 5
    
    bob_sa = sa.SA()
    ## AES_GCM_16_IIV related shared context between Alice and Bob
    bob_sa.esp_enc_alg = "ENCR_AES_GCM_16_IIV"
    bob_sa.esp_enc_key = b'\xf1\x6a\x93\x0f\x52\xa1\x9b\xbe\x07\x1c\x6d\x44\xb4\x24\xf3\x03'
    bob_sa.ext_seq_num_flag = False
    bob_sa.seq_num_counter = 5
    
    
    ## Alice
    alice_plaintext = b"yet another secret"
    print("Alice plaintext is: %s"%alice_plaintext)
    alice_cipher = alice_sa.ciphers_obj()[0]
    ## encryption, authentication
    ciphertext, icv = \
      alice_cipher.encrypt_and_digest(alice_plaintext)
    nonce = alice_cipher.nonce
    print("The encrypted message sent by Alice to Bob is:")
    print(" - (nonce [%s]: %s,"%(len(nonce), hexlify(nonce)))
    print(" - ciphertext: %s"%hexlify(ciphertext))
    print("icv[%s]: %s"%(len(icv), hexlify(icv)))
    
    
    ## Bob
    bob_cipher = bob_sa.ciphers_obj()[0]
    ## encryption, authentication
    ### verification, decryption
    bob_plaintext = \
    bob_cipher.decrypt_and_verify(ciphertext, icv)
    print("Bob plaintext is: %s"%bob_plaintext )
    return self.compare( bob_plaintext, alice_plaintext, 2 )

  def eval_q10( self ):
    import pad    
    import ref_pad   
    score = 0 
    data_len_list = [ 1, 2, 3, 4, 32, 33, 34, 35 ]
    for data_len in data_len_list:
      print(f" expected response: {ref_pad.pad( data_len )}" ) 
      score += self.compare( pad.pad( data_len ), ref_pad.pad( data_len ), 1 )
    return score / len( data_len_list ) * 4.0

  def eval_q11( self ):
    import ref_sa
    import ref_esp
    import binascii

    sa = ref_sa.SA()
    ref_esp = ref_esp.ESP(sa)

    alice_inner_ip_pkt = b'inner_ip6_packet'

    ## evaluating the ESP clear text packet
    ref_pad = ref_esp.pad(len(alice_inner_ip_pkt))
    ref_alice_clear_text_esp = {\
      'data':alice_inner_ip_pkt,\
      'pad':ref_pad,\
      'pad_len':len( ref_pad ), \
      'next_header':'IPv6'}
#    print( f"ref_alice_clear_text_esp: {ref_alice_clear_text_esp}")

    ## we import esp here because esp executes some scripts at the importation
    ## we shoudl update esp with th eif __na__ == '__main__'
    print( "loading the module esp" )
    import esp
    print( "loading esp succeeded" )

    score = 0

    esp = esp.ESP(sa)
    
    ## Alice inner packet
    #print("-- Alice Data payload")
    alice_inner_ip_pkt = b'inner_ip6_packet'
    #print("data payload: %s"%alice_inner_ip_pkt)
        
    ## Encapsulation of the inner packet in to ESP 
    #print("-- Alice Clear text ESP payload")
    pad = esp.pad(len(alice_inner_ip_pkt))
    alice_clear_text_esp = {\
      'data':alice_inner_ip_pkt,\
      'pad':pad,\
      'pad_len':len(pad), \
      'next_header':'IPv6'}
    #print(alice_clear_text_esp)
   
    score += self.compare( alice_clear_text_esp, ref_alice_clear_text_esp, 1 )

    #print("-- Alice Encrypting clear text " +\
    #      "and concatenating with ESP header")
    alice_esp = esp.pack(alice_inner_ip_pkt)
    #print(alice_esp)
    
    #print("-- Alice sending ESP in byte format:")
    bytes_esp = esp.to_bytes(alice_esp)
    #print("  esp: %s"%hexlify(bytes_esp))
    
    #print("-- Bob receives the packet")
    bob_esp = esp.from_bytes(bytes_esp)
    #print(bob_esp)
    
    #print("-- Bob decrypts the encrypted part")
    encrypted_esp = {\
      'encrypted_payload': bob_esp['encrypted_payload'],\
      'icv': bob_esp['icv']}
    bob_clear_text_esp = esp.unpack(encrypted_esp)
    #print(bob_clear_text_esp)
    
    #print("-- Bob extracts the Data payload")
    #print(bob_clear_text_esp['data'])
    
    
    #print("The short version would be:")
    #print("    - pack:%s"%esp.pack(alice_inner_ip_pkt))
    #print("    - unpack:%s"\
    #  %esp.unpack(esp.pack(alice_inner_ip_pkt)))
    esp_unpack = esp.unpack(esp.pack(alice_inner_ip_pkt))
    score += self.compare( esp_unpack[ 'data' ],  b'inner_ip6_packet', 1 )
    return score
