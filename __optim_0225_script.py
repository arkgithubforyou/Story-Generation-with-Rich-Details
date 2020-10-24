"""
optimization session 2020.02.25
Specifications:
    trick dis-aligning train / inference irregular events removed.

Zhai Fangzhou
"""

from optimization import FleshGenMetaOptimizer
#from globals import GlobalConstants
from flesh_model_s import AlternatingSeq2Seq
import datetime, os

class ExecutionSettings:
    ''''''
    class MetaOptimizationSettings:
        """
        settings concerning a specific execution of meta optimization. should only be accessed by the meta optimizer.
        """
        # fixme: should this be associated with the meta optimizer, instead of being a stupid, independent class here?
        #  yes; this is just data / argument, not really a class. yes this is ugly, but it cleanly separates and
        #  works atm.
        MODE = FleshGenMetaOptimizer.OPTIMIZATION_MODE
        if os.getcwd().__contains__('exe'):
            assert MODE == FleshGenMetaOptimizer.OPTIMIZATION_MODE
        '''-------------------------- hyper optimization specifications --------------------------'''
        param_domains = {'batch_size': [16, 511],
                         'ed_ncoder_size': [128, 2047],
                         'word_embedding_size': [128, 1023],
                         'event_embedding_size': [128, 1023],
                         'lr': [1e-5, 5e-3],
                         'percent_student': [1e-4, 0.5],
                         'l2': [1e-4, 5e-2],
                         'dropout': [0.05, 0.8],
                         'clip': [1, 10]}
        num_trials = 15
        DEVICE = 7
        TAG = 'BASE_OPTIM_{}'.format(str(datetime.date.today()))
        MAX_EPOCHS = 100
        PATIENCE = 30

        LOG_TO_TENSORBOARD = True


        '''-------------------------- training --------------------------'''
        SAMPLE_AGENDA_REGULAR = ['screv_bring_vehicle_grocery', 'screv_leave_grocery', 'screv_bring_vehicle_grocery']
        SAMPLE_AGENDA_IRREGULAR = ['screv_bring_vehicle_grocery', 'screv_leave_grocery', 'irregular_grocery',
                                   'screv_bring_vehicle_grocery']
        SAMPLE_AGENDA_S = [SAMPLE_AGENDA_REGULAR, SAMPLE_AGENDA_IRREGULAR]
        SAMPLE_SCENARIO = 'grocery'
        '''-------------------------- paths --------------------------'''
        if MODE == FleshGenMetaOptimizer.OPTIMIZATION_MODE:
            train_data_path = os.path.join('.', 'data_seg_train')
            val_data_path = os.path.join('.', 'data_seg_val')
        else:
            train_data_path = os.path.join('.', 'data_seg_train_toytoy')
            val_data_path = os.path.join('.', 'data_seg_val_toytoy')



    class ModelSpecifications:
        """
        settings that have nothing to do with a specific meta optimization session, but define the model structure to
        be optimized.
        """
        LOG_TO_TENSORBOARD = True
        SAVE_MODEL = True

        BEAM_SIZE = 19
        MAX_DECODING_LENGTH = 20
        '''-------------------------- model specifications --------------------------'''
        is_seq2seq_baseline = False
        MERGE_IRREGULAR_EVENTS = True
        USE_GLOVE = False
        SHARE_ENCODER = False


        ''' whether to include the MMI term during beam search. Note that it is tured OFF during training '''
        USE_MMI_SCORE = False

        ''' MMI_coefficient for the irregular decoder '''
        IRREGULAR_MMI_COEFFICIENT = 1.
        ''' MMI coefficient for the regular decoder '''
        REGULAR_MMI_COEFFICIENT = 0.



if __name__ == '__main__':
    meta_optimizer = FleshGenMetaOptimizer(
        domains=ExecutionSettings.MetaOptimizationSettings.param_domains,
        num_trials=ExecutionSettings.MetaOptimizationSettings.num_trials,
        tag=ExecutionSettings.MetaOptimizationSettings.TAG,
        model_def_function=AlternatingSeq2Seq.define_model,
        meta_optimization_settings=ExecutionSettings.MetaOptimizationSettings,
        model_specifications=ExecutionSettings.ModelSpecifications
    )
    meta_optimizer.search()