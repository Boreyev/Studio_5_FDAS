def save_encoding_Data(face_encoding):    #Outputs face detection data to text file
     lines = [str(face_encoding)]
     with open('src/data/encoding_data.txt', 'a') as f:
         for line in lines:
             f.write(line)
             f.write('\n')
def save_Data(nTime, name, confidence_out):    #Outputs face detection data to text file
    lines = [str(nTime) + '\n' + name + ': ' + str(confidence_out)]
    with open('src/data/test_data.txt', 'a') as f:
        for line in lines:
            f.write(line)
            f.write('\n')
            f.write('\n')

def save_distances(name, nTime, face_distances):    #Outputs face detection data to text file
        lines = [str(name) + ' Detected: ' + str(nTime) + '\n' + 'Distances: ' + str(face_distances)]
        with open('src/data/test_distances.txt', 'a') as f:
            for line in lines:
                f.write(line)
                f.write('\n')
                f.write('\n')


