import sys
sys.path.insert( 0, '/home/emigdan/gitlab/pylab_evaluation/examples' )
import lab_babyesp 

lab = lab_babyesp.EvalBabyESP( '/home/emigdan/gitlab/pylab_evaluation/tests/baby_esp22/lab/lastname3,_firstname3_5696540_assignsubmission_file_', '/home/emigdan/gitlab/pylab_evaluation/tests/test_single_lab/ref', json_score_list='/home/emigdan/gitlab/pylab_evaluation/tests/baby_esp22/lab_grade_list.json', lab_id='zzz3104' )
lab.eval_py() 
