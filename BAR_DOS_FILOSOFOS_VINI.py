#  ██████╗  █████╗ ██████╗                     ██████╗  ██████╗ ███████╗ 
#  ██╔══██╗██╔══██╗██╔══██╗                    ██╔══██╗██╔═══██╗██╔════╝ 
#  ██████╔╝███████║██████╔╝                    ██║  ██║██║   ██║███████╗ 
#  ██╔══██╗██╔══██║██╔══██╗                    ██║  ██║██║   ██║╚════██║ 
#  ██████╔╝██║  ██║██║  ██║                    ██████╔╝╚██████╔╝███████║ 
#  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                    ╚═════╝  ╚═════╝ ╚══════╝ 
#                                                                        
#  ███████╗██╗██╗      ██████╗ ███████╗ ██████╗ ███████╗ ██████╗ ███████╗
#  ██╔════╝██║██║     ██╔═══██╗██╔════╝██╔═══██╗██╔════╝██╔═══██╗██╔════╝
#  █████╗  ██║██║     ██║   ██║███████╗██║   ██║█████╗  ██║   ██║███████╗
#  ██╔══╝  ██║██║     ██║   ██║╚════██║██║   ██║██╔══╝  ██║   ██║╚════██║
#  ██║     ██║███████╗╚██████╔╝███████║╚██████╔╝██║     ╚██████╔╝███████║
#  ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝

#ALUNO: VINICIUS AMARO SAMPAIO
#MATRICULA: 1368157


from threading import Thread, Lock
import time
from random import choice, randint, randrange
from datetime import datetime
from parsequotes import readfile
import pandas as pd

import logging
logging.basicConfig(filename='log.log',level=logging.DEBUG)
#logging.debug(',ID,SLEEP,WAIT,DRINK')

data_lock = Lock()
taken = []
quotes = readfile()


class filosofo(Thread):
    
    def count_drink(self):
        self.drinks = self.drinks + 1
    
    def change_estate(self):
        self.estate = self.estate + 1
        if self.estate > 2:
            self.estate = 0
    
    def free_drinks(self):
        for i in self.chosen_drinks:
            try:
                with data_lock:
                    taken.remove(i)
            except:
                try:
                    with data_lock:
                        taken.remove([i[1],i[0]])
                except:
                    pass


    def drink(self):
        time.sleep(1)
        self.count_drink()
        self.free_drinks()
        
        
    def number_drinks(self):
        return randint(2, self.n)
    
    def rest_time(self):
        return randrange(0,2000)/1000
    
    def rest(self,x):
        time.sleep(x)
        return
    
    def __init__(self,lista,token,q):
        Thread.__init__(self)
        self.conec = []
        self.iden = token
        self.chosen_drinks = []
        self.estate = 0
        self.drinks = 0
        self.n = 0
        self.k = q

        for i in range(0,len(lista)):
            if lista[i] == 1:
                self.n = self.n + 1
                self.conec.append([i,token])

    def run(self):
        while(self.drinks != self.k):
            t_calm = self.rest_time()
            self.rest(t_calm)

            t_start = datetime.now()
            n = self.number_drinks()

            d = 0
            flag = False
            while(d != n):

                dFlag = False
                while(not dFlag):
                    vertex = choice(self.conec)
                    if vertex not in self.chosen_drinks:
                        dFlag = True

                with data_lock:
                    if (vertex not in taken) or ([vertex[1],vertex[0]] not in taken):    
                        taken.append(vertex)
                        flag = True
                
                if flag:
                    self.chosen_drinks.append(vertex)
                    d = d + 1
            t_sede = datetime.now() - t_start
            self.drink()
            logging.info('Philosopher '+str(self.iden)+' rested for '+str(t_calm)+'s waited '+str(t_sede)[6:]+'s and drank '+str(self.chosen_drinks)+' and is now at '+str(self.drinks)+' drinks')
            #logging.debug(','+str(self.iden)+','+str(t_calm)+','+str(t_sede)[6:]+','+str(self.drinks))
            print('\033[94m'+'Philosopher ' +str(self.iden)+' shouts:'+'\033[0m'+'\n'+choice(quotes))
            self.chosen_drinks = []
                

def GetGraph(file):
    df = pd.read_csv(file,header=None)
    return df.values


def main():


    print('\n\t\033[1m'+'\033[5m'+'\033[92m'+'BAR DOS FILOSOFOS'+'\033[0m')

    print('\nSelect Case:\n')

    print('1\t5 vertices 6 drinks each')
    print('2\t6 vertices 6 drinks each')
    print('3\t12 vertices 3 drinks each')
    print('9\tLeave')

    f = False
    while(not f):
        try:
            case = int(input('\nSelect Option:\n'))
        except:
            case = 0

        if case == 1:
            file = 'grafo1.txt'
            r = 6
            break
        if case == 2:
            file = 'grafo2.txt'
            r = 6
            break
        if case == 3:
            file = 'grafo3.txt'
            r = 3
            break
        if case == 9:
            exit()
        print('\n'+'\033[91m'+'Invalid option!'+'\033[0m'+'\n')

    matrix = GetGraph(file)

    for i in range(0,len(matrix)):
        filo = filosofo(matrix[i],i,r)
        filo.start()

if __name__ == '__main__':
    main()