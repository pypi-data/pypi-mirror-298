#Define loop of unencryptable numbers and pi
loop_o_death = [0, 33, 25, 90, 248, 480, 105, 50, 32, 16, 41, 3, 7, 2, 14, 1, 4, 5, 10, 15]

def define_pi(path="pi.txt"):
    """Define the Pi you want to access for encryption and decryption

    Args:
        path (str, optional): Specify externally downloaded pi txt files. Defaults to "pi.txt".

    Returns:
        str: pi digits
    """
    with open(path, mode="r") as f:
        pi = f.read()
    return pi

def encrypt(pi,message):
    """Encrypts an integer using Kryptograpi

    Args:
        pi (str) : str of pi digits
        message (int): Message to be encrypted

    Returns:
        kryptograpi_cipher: The encrypted cipher
    """
    
    #Raise exception if mesage cant be encrypted
    if message in loop_o_death:
        raise Exception
    
    #Define vars
    starting_index_of_integer_sequence = str(message)
    c = 0
    suffix_list = {}
    ending_index_of_integer_sequence = 0
    
    #Run infinite loop
    while True:
        
        #Find the initial messages index within pi
        starting_index_of_integer_sequence = str(pi.find(starting_index_of_integer_sequence))
        
        #
        if str(pi.find(starting_index_of_integer_sequence[:-1])) == str(pi.find(starting_index_of_integer_sequence)) and pi.find(starting_index_of_integer_sequence) != -1:
            starting_index_of_integer_sequence = starting_index_of_integer_sequence
            suffix_list[c] = starting_index_of_integer_sequence[-1]
          
        #If the final number cant be found within the defined pi or keeps repeating itself  
        if starting_index_of_integer_sequence == "-1" or starting_index_of_integer_sequence == ending_index_of_integer_sequence:
            
            #Break the loop making the last sequence the LINUM
            break
        
        #This rounds ending index will be next rounds starting index
        ending_index_of_integer_sequence = starting_index_of_integer_sequence
        c += 1
    
    #Define the final linum and return the kryptograpi_cipher
    LINUM=ending_index_of_integer_sequence
    return [int(LINUM), c, suffix_list]

def decrypt(pi,kryptograpi_cipher):
    """Decrypts Encrypted Data

    Args:
        pi (str) : str of pi digits
        kryptograpi_cipher (list): List consisting of LINUM,C and Suffix list

    Returns:
        str: original encrypted string
    """
    
    #Setting vars
    count = 0
    start_index_of_integer_sequence, c, suffix_list = kryptograpi_cipher[0], kryptograpi_cipher[1], kryptograpi_cipher[2]

    #While reduction count has not reached c (final count) 
    while count != c:
        
        #As the ending index must be bigger than starting index we add 1 to it
        ending_index_of_integer_sequence = start_index_of_integer_sequence + 1
        
        #As long as the calculated index doesnt correspond to the number we want we extend it by one digit
        while pi.find(str(pi[start_index_of_integer_sequence:ending_index_of_integer_sequence])) != start_index_of_integer_sequence:
            ending_index_of_integer_sequence += 1


        try:
            
            #If there is a suffix available it gets retrieved
            suffix = suffix_list[c - count - 2]
            
            #Get the integer sequence for the next round and append the suffix
            start_index_of_integer_sequence = pi[start_index_of_integer_sequence:ending_index_of_integer_sequence]
            start_index_of_integer_sequence += suffix
            
        except KeyError:
            
            #If there is no suffix available define the start index for next round without any additions
            start_index_of_integer_sequence = pi[start_index_of_integer_sequence:ending_index_of_integer_sequence]
        
        #Convert str fomrat to int and increase count by 1
        start_index_of_integer_sequence = int(start_index_of_integer_sequence)
        count += 1

    #Return the original message
    return start_index_of_integer_sequence