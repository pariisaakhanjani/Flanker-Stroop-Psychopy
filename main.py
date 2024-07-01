import psychopy.event
from psychopy.visual import Window
from psychopy.event import waitKeys
from trial import FlankerTrial, StroopTrial, InstructionTrial
from block import Block
import pandas as pd
import os
from psychopy.gui import Dlg

def draw_flip_wait(window, trial):
    trial.draw()
    window.flip()
    waitKeys()

def dump_data(block, filename, participant_id, participant_type):
    data = block.to_dataframe()
    # Add participant information to the DataFrame
    data['Participant ID'] = participant_id
    data['Participant Type'] = participant_type
    # Check if the file already exists
    include_header = not os.path.isfile(filename)
    data.to_csv(filename, mode='a', header=include_header, index=False)


if __name__ == '__main__':
    # Create a dialog box for participant information
    gui = Dlg(title="Stroop / Flanker study")
    gui.addText('Participant Information')
    gui.addField('Participant ID:')
    gui.addField('Participant type:', choices=['main', 'pilot'])
    gui.show()

    if gui.OK:
        participant_id = gui.data[0]
        participant_type = gui.data[1]
    else:
        print("User cancelled the experiment.")
        exit()

    window = Window(fullscr=False, units='pix', size = [640, 480])

    instruction_text = "Now the next block is starting!"
    instruction_color = 'black'

    # flanker_filenames=[]
    # flanker_file1 = "C:/Users/pkhan/Desktop/Kaiserslautern/4th semester/Experiments with Python/Archive/ft_b1.csv"
    # flanker_file2 = "C:/Users/pkhan/Desktop/Kaiserslautern/4th semester/Experiments with Python/Archive/ft_b2.csv"
    # flanker_file3 = "C:/Users/pkhan/Desktop/Kaiserslautern/4th semester/Experiments with Python/Archive/ft_b3.csv"
    # flanker_filenames.extend([flanker_file1, flanker_file2, flanker_file3])
    flanker_filenames=["ft_b1.csv", "ft_b2.csv", "ft_b3.csv"]

    # stroop_filenames = []
    # stroop_file1 = "C:/Users/pkhan/Desktop/Kaiserslautern/4th semester/Experiments with Python/Archive/st_b1.csv"
    # stroop_file2 = "C:/Users/pkhan/Desktop/Kaiserslautern/4th semester/Experiments with Python/Archive/st_b2.csv"
    # stroop_file3 = "C:/Users/pkhan/Desktop/Kaiserslautern/4th semester/Experiments with Python/Archive/st_b3.csv"
    # stroop_filenames.extend([stroop_file1, stroop_file2, stroop_file3])
    stroop_filenames = ["st_b1.csv", "st_b2.csv", "st_b3.csv"]
    
    roundrobined_Blocks = Block.load_Blocks(window,flanker_filenames,stroop_filenames)

    for block in roundrobined_Blocks:
        block.instruction = InstructionTrial(window, instruction_text, color=instruction_color)


    for block in roundrobined_Blocks:
        block.run()
        output_file = f"output_{participant_type}.csv"
        dump_data(block, output_file, participant_id, participant_type)

    
    window.close()