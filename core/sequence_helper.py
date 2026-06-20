import numpy as np

def create_lstm_sequences(X_scaled, y_scaled, n_steps):

    X_seq = []
    y_seq = []
    
    for i in range(len(X_scaled) - n_steps):
        X_seq.append(X_scaled[i:i + n_steps])
        y_seq.append(y_scaled[i + n_steps])
        
    return np.array(X_seq), np.array(y_seq)