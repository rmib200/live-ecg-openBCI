import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import brainflow
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams


def get_df(data):
    df = pd.DataFrame(data[:, [1,13]], columns=["ECG", "Time"])
    return df

def get_data(sfreq):
    try:
       while board.get_board_data_count() < sfreq:
           time.sleep(0.01)
    except Exception as e:
       raise(e)
    board_data = board.get_board_data()
    print(np.shape(board_data))
    df = get_df(np.transpose(board_data))
    return df

global board
params = BrainFlowInputParams ()
params.serial_port = "COM8"
board = BoardShim (BoardIds.GANGLION_BOARD.value, params)
board.prepare_session ()
board.start_stream ()
 
ecg = []
n = 250 #sfreq
plt.style.use("seaborn")
fig = plt.figure(figsize=(13,6))
ax = fig.add_subplot()
fig.show()
plt.title("LIVE ECG")
plt.ylabel("Amplitude (mV)", fontsize=15)
plt.xlabel("Time",
            fontsize=10,
        )
plt.ion() #interactive mode on
while True:
    df = get_data(n)
    ecg.extend(df.iloc[:,0].values)
    plt.autoscale(enable=True, axis="y", tight=True)
    ax.plot(ecg, color="r",linewidth=2)
    fig.canvas.draw()
    ax.set_xlim(left=n-250, right=n)
    n = n + 250
    plt.pause(0.01)
