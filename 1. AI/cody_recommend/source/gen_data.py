from random import *
import csv
import numpy as np

weather = ['sunny', 'rainy', 'cloudy']
sex = ['male', 'female']
style = ['sports', 'business', 'casual']


f = open('feature_data_valid.csv', 'w', newline="\n")
wr = csv.writer(f)
wr.writerow(['temp', 'weather', 'age', 'sex', 'height', 'weight', 'body_shape', 'style'])

for i in range(30):
    body_shape=''
    age = randint(20, 65)
    rand_w = randint(0, 2)
    rand_s = randint(0, 1)
    rand_st = randint(0, 2)
    temp = randint(20, 35)
    while True:
        if rand_s == 0:
            height = int(np.random.randn()*6+175)
            weight = int(np.random.randn()*11+71)
        else:
            height = int(np.random.randn()*5+161)
            weight = int(np.random.randn()*8+55)

        if (height-weight > 70) and ((height-weight) < 125):
            break
    if (weight / ((0.01*height)*(0.01*height)) < 18.5) :
        body_shape = 'thin'
    elif (weight / ((0.01*height)*(0.01*height)) > 25):
        body_shape = 'fat'
    else:
        body_shape = 'normal'
    wr.writerow([temp,weather[rand_w],age,sex[rand_s],height, weight,body_shape,style[rand_st]])

