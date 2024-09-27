
from model_calc import relative_humedity
from view import *


def control():
    num1,num2=read()
    result=relative_humedity(num1,num2)
    display(result)
    