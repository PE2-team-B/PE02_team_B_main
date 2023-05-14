import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
import graph_individual as gi

def graph(x):
    insert = x
    data_elements = []
    output_elements = []

    for element in insert:
        if isinstance(element, list) or isinstance(element, tuple):
            data_elements.append(element)
        else:
            output_elements.append(element)



    if 'csv_file' in output_elements:
        graph_elements = output_elements.pop()
        k = len(graph_elements)
    else:
        graph_elements = output_elements
        k = len(graph_elements)

    def graph_saving(x):
        now = datetime.now()
       # 폴더 이름 만들기 (예: 2023-05-04)
        folder_name = now.strftime("%Y-%m-%d")
        # 폴더 생성하기
        if not os.path.exists("../res/" + folder_name):
            os.makedirs("../res/" + folder_name)
        plt.savefig('../res/' + folder_name + '/' + '{}_{}_{}'.format(*data_elements[x]) + ' '.join(str(x) for x in graph_elements) + '.png')
        # plt.show()
    def graph_select(x,y):
        if graph_elements[x] == 'IV':
            gi.IV_graph_plot(*data_elements[y])
        elif graph_elements[x] == 'TR':
            gi.transmission_spectra(*data_elements[y])
        elif graph_elements[x] == 'Ref_fit':
            gi.transmission_rsquare(*data_elements[y])

    for i in range(0,len(data_elements)):

        if k == 1:
            graph_select(0,i)
            graph_saving(i)
            plt.show()

        elif k == 2:
            plt.subplot(1,2,1)
            graph_select(0,i)
            plt.subplot(1,2,2)
            graph_select(1,i)
            graph_saving(i)
            plt.show()

        elif k == 4:
            plt.subplot(2,4,1)
            graph_select(0,i)
            plt.subplot(2,4,2)
            graph_select(1,i)
            plt.subplot(2,4,3)
            graph_select(2,i)
            plt.subplot(2,4,3)
            graph_select(3,i)
            graph_saving(i)
            plt.show()
