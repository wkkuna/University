import csv
import numpy
with open('klimat.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=';', quotechar='|')
    data = numpy.matrix(list(data)[1:])
    # Wyodrębnienie temperatury, wysokości i szerokości
    temp = data[:,4]
    coord = data[:,1:3]
    
    # Dodatnie kolumny wypełnionej jedynkami i wypełnienie koordynatami
    # długości i szerokości
    X = numpy.matrix(numpy.ones((coord.shape[0], coord.shape[1] + 1)))
    X[:,1:] = coord

    temp = temp.astype(float)
    Beta = (X.T * X).I * X.T * temp
    print(Beta)