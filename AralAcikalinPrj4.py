#Aral Açıkalın
import random

def randomExp(lambd):
    '''Creating a random inter-arival time in seconds'''  
    #creates a random inter-arrival variable 
    #dividing lambda by 60 gives the rate of customers arriving per second so inter-arrival time is in seconds
    nextArrival=random.expovariate(lambd/60) 
    return nextArrival

def simulation(lambd,mean,capacity):
    #initialize the simulation, statistics.
    snapshot=[]
    waitTime=0
    customersinQue=0
    isServing=False
    time=0
    randArrival=randomExp(lambd)
    time+=randArrival
    randDeparture=randomExp(mean)
    customerNo=1

    #stores events as t,arrival event flag and customer no
    events=[[time,"Arrival",customerNo],[time+randDeparture,"Departure",customerNo]]

    for i in range(1000): #TODO müşteri sayısı kadar loop yapmak için while ile değiştir

        #sorting the events acording to their time
        events.sort()
        #set the clock to the events clock
        time=events[0][0]
        if(events[0][1]=="Arrival"):
            if(not isServing):
                #setting ls(t) to 1
                isServing=True
                customerNo=events[0][2]

                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure",customerNo])
                randArrival=randomExp(lambd)
                events.append([time+randArrival,"Arrival",customerNo+1])
                #TODO collect statistics
                events.pop(0)

            else:
                customersinQue+=1
                randArrival=randomExp(lambd)
                events.append([time+randArrival,"Arrival"])
                #TODO collect statistics


        elif(events[0][1]=="Departure"):
            if(customersinQue>0):
                customersinQue-=1
                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure"])
                #TODO collect statistics
                events.pop(0)
            else:
                isServing=False

