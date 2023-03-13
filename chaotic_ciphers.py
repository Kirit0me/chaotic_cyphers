import numpy as np
import random


def pwlcm_cipher(message, key, encrypt = True):
    # Set the parameters of the PWLCM system
    m = key[0]
    c = key[1]
    gamma = key[2]
    delta = key[3]
    N = key[4]
    # Set the encryption parameters
    steps = len(message)
    # Generate the PWLCM map
    x = np.zeros(N)
    for i in range(1, N):
        x[i] = (m*x[i-1] + c ) % gamma
    # Divide the range of the map into segments
    segments = np.linspace(0, gamma, num=steps+1)
    # Encrypt the message using the PWLCM map
    result = []
    for i, char in enumerate(message):
        char_code = ord(char)
        segment = np.digitize(x[i % N], segments) - 1 # Determine which segment the current value of x falls into
        slope = (char_code - delta) / (segments[segment+1] - segments[segment]) # Determine the slope of the current segment
        intercept = char_code - slope*segments[segment] # Determine the intercept of the current segment
        
        if encrypt:
            encrypted_code = int(np.floor(slope*x[i % N] + intercept)) % 256 # Compute the encrypted code using the curBro encrypt my fucking textrent segment
            result.append(chr(encrypted_code))
        else: 
            decrypted_code = int(np.floor((char_code - intercept)/slope)) %256
            result.append(chr(decrypted_code))
            x[i % N] = (m*x[i % N] + c) % gamma

    return ''.join(result)

def lorenz_cipher(message, key, encrypt = True):
    # Set the parameters of the Lorenz system
    sigma = key[0]
    rho = key[1]
    beta = key[2]
    # Set the initial conditions of the Lorenz system
    x = key[3]
    y = key[4]
    z = key[5]
    # Set the encryption parameters
    dt = 0.01
    steps = 1000
    # Generate the cipher stream

    cipher = []
    for i in range(steps):
        dxdt = sigma*(y - x)
        dydt = x*(rho - z) - y
        dzdt = x*y - beta*z
        x += dxdt*dt
        y += dydt*dt
        z += dzdt*dt
        cipher.append(x)

    if encrypt:
        # Encrypt the message using the cipher stream
        encrypted = []
        for i, char in enumerate(message):
            char_code = ord(char)
            cipher_code = int(np.round((cipher[i % steps] - np.floor(cipher[i % steps]))*1000)) # Map the cipher stream to integers between 0 and 999
            encrypted_code = (char_code + cipher_code) % 256 # Perform XOR encryption
            encrypted.append(chr(encrypted_code))
        return ''.join(encrypted)
    else:
        decrypted = []
        for i, char in enumerate(message):
            char_code = ord(char)
            cipher_code = int(np.round((cipher[i % steps] - np.floor(cipher[i % steps]))*1000)) # Map the cipher stream to integers between 0 and 999
            decrypted_code = (char_code - cipher_code) % 256 # Reverse XOR encryption
            decrypted.append(chr(decrypted_code))
        return ''.join(decrypted)


message_user = input("Please give me something to encrypt : ")
key_pwlcm = [16, 34, 65, 12, 10] # Example key
pwlcm = pwlcm_cipher(message_user, key_pwlcm)
# Set the key
key_lorenz = (10, 28, 8/3, 1, 1, 1)
lorenz = lorenz_cipher(message_user, key_lorenz)
print("Encrypts : ")
print("")
print("PWLCM : ", pwlcm)
print("LORENZ : ", lorenz)
print("")

#this decryption doesnt work so meow
decrypted_message_i_dont_work = pwlcm_cipher(pwlcm, key_pwlcm, encrypt=False)
decrypted_lorenz_i_dont_want_to_work_either = lorenz_cipher(lorenz_cipher, key_lorenz, encrypt=False)
print("DECRYPTS : ")
#print(decrypted_message_i_dont_work)
#print(decrypted_lorenz_i_dont_want_to_work_either)