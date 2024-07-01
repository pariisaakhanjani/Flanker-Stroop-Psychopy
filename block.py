import pandas as pd
from trial import StroopTrial, FlankerTrial, InstructionTrial
from psychopy import visual, event
from itertools import cycle, islice

class Block:
    def __init__(self, tr_list, instruction_text=None, window=None):
        self.trials= tr_list
        self.instruction = InstructionTrial(window, instruction_text) if instruction_text else None

    def run(self):
        if self.instruction:
            self.instruction.run()
        for trial in self.trials:
            trial.run()

    def to_dataframe(self):
        data = []
        for trial in self.trials:
            trial_data = {
                "Response": trial.response[0] if trial.response else None,
                "Correct value": trial.correct if hasattr(trial, 'correct') else None,
                "Right Answer": trial.rightAnswer,
                "Type": type(trial).__name__,
                "Text": getattr(trial, 'text', None),
                "Color": getattr(trial, 'color', None),
                "Trial Type": getattr(trial, 'trial_type', None),
                "Response Time": trial.response_time
            }
            data.append(trial_data)
        return pd.DataFrame(data)
    
    def roundrobin(*iterables):
        #"roundrobin('ABC', 'D', 'EF') --> A D E B F C"
        num_active = len(iterables)
        nexts = cycle(iter(it).__next__ for it in iterables)
        while num_active:
            try:
                for next in nexts:
                    yield next()
            except StopIteration:
                # Remove the iterator we just exhausted from the cycle.
                num_active -= 1
                nexts = cycle(islice(nexts, num_active))

    def load_Flanker_block(win, flanker_filename):
        myFlankerList = []
        flanker_data = pd.read_csv(flanker_filename)
        for index, row in flanker_data.iterrows():
            temp = FlankerTrial(win, row['correct'], row['type'])
            myFlankerList.append(temp)
        return Block(myFlankerList)
    
    def load_Stroop_block(win, stroop_filename):
        myStroopList = []
        stroop_data = pd.read_csv(stroop_filename)
        for index, row in stroop_data.iterrows():
            temp = StroopTrial(win, row['text'], row['color'])
            myStroopList.append(temp)
        return Block(myStroopList)
    
    def load_Blocks(win, flanker_filenames, stroop_filenames):
        flankerBlocks=[]
        for flankerFile in flanker_filenames:
            fblock = Block.load_Flanker_block(win,flankerFile)
            flankerBlocks.append(fblock)
        
        stroopBlocks=[]
        for stroopFile in stroop_filenames:
            sblock = Block.load_Stroop_block(win,stroopFile)
            stroopBlocks.append(sblock)

        allBlocks = []
        for block in Block.roundrobin(flankerBlocks, stroopBlocks):
            allBlocks.append(block)
        return allBlocks
