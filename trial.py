from psychopy import visual, event
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.event import waitKeys
from psychopy.core import Clock

class Trial:
    def __init__(self, window):
        self.window = window
        self.rightAnswer = None
        self.response_time = None
        self.clock = Clock()

    def draw(self):
        self.stim.draw()

    def run(self):
        self.draw()
        self.window.flip()
        self.response = event.waitKeys(keyList=['f', 'j', 'b', 'r', 'y', 'g'])
        self.response_time = self.clock.getTime()
        self.validate_response()
    
    def validate_response(self):
        pass


class StroopTrial(Trial):
    def __init__(self, window, text=None, color=None):
        super().__init__(window)
        self.word = text
        self.color = color

        self.stim = TextStim(self.window, text=self.word, color=self.color)

    def draw(self):
        self.stim.draw()

    def validate_response(self):
        if len(self.response) != 1:
            self.rightAnswer = False
        else:
            response_key = self.response[0]
            corrct_key = self.color[0]
            self.rightAnswer = response_key = corrct_key


class FlankerTrial(Trial):
    def __init__(self, window, correct=None, type=None, image_name= 'flanker_arrow.png'):
        super().__init__(window)
        self.type = type
        self.correct = correct
        image_path = image_name
        
        
        #initialize imagestim
        self.stim1 = ImageStim(self.window, image_path, units='pix', size=[100, 100], pos=(0, 0))
        self.stim2 = ImageStim(self.window, image_path, units='pix', size=[100, 100], pos=(100, 0))
        self.stim3 = ImageStim(self.window, image_path, units='pix', size=[100, 100], pos=(-100, 0))
        self.stim4 = ImageStim(self.window, image_path, units='pix', size=[100, 100], pos=(200, 0))
        self.stim5 = ImageStim(self.window, image_path, units='pix', size=[100, 100], pos=(-200, 0))
    
        if self.correct == 'left':
            self.stim1.flipHoriz = True

        if self.type == 'congruent':
            self.stim2.flipHoriz = self.stim1.flipHoriz
            self.stim3.flipHoriz = self.stim1.flipHoriz
            self.stim4.flipHoriz = self.stim1.flipHoriz
            self.stim5.flipHoriz = self.stim1.flipHoriz
        elif self.type == 'incongruent':
            self.stim2.flipHoriz = not self.stim1.flipHoriz
            self.stim3.flipHoriz = not self.stim1.flipHoriz
            self.stim4.flipHoriz = not self.stim1.flipHoriz
            self.stim5.flipHoriz = not self.stim1.flipHoriz
        
    def draw(self):
        if self.type =='neutral':
            self.stim1.draw()
        else:
            self.stim1.draw()
            self.stim2.draw()
            self.stim3.draw()
            self.stim4.draw()
            self.stim5.draw()

    def validate_response(self):
        if len(self.response) != 1:
            self.is_correct = False
        else:
            response_key = self.response[0]
            correct_key = 'f' if self.correct == 'left' else 'j'
            self.is_correct = response_key == correct_key

class InstructionTrial(Trial):
    def __init__(self, window, instruction_text, color = 'white'):
        super().__init__(window)
        self.instruction_text = instruction_text
        self.color = color
        self.stimN = TextStim(self.window, text=self.instruction_text, color=self.color)

    def draw(self):
        self.stimN.draw()

