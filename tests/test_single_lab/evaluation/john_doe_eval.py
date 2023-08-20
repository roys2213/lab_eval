import sys
sys.path.insert( 0, '../examples' )
import lab_babyesp 

lab = lab_babyesp.EvalBabyESP( '/home/emigdan/gitlab/pylab_evaluation/tests/test_single_lab/student', '/home/emigdan/gitlab/pylab_evaluation/tests/test_single_lab/ref', json_score_list='/home/emigdan/gitlab/pylab_evaluation/tests/test_single_lab/score_list.json', lab_id='john_doe' )
lab.eval_py() 
