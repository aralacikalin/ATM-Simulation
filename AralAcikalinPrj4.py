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


    #initializing the system state
    customersinQue=0
    isServing=False
    time=0

    #customer entity list
    customers=[]


    randArrival=randomExp(lambd)
    time+=randArrival
    customerNo=0

    #stores events as time, event flag and customer no
    events=[[time,"Arrival",customerNo]]

    for i in range(1000): #TODO müşteri sayısı kadar loop yapmak için while ile değiştir

        #set the clock to the events clock
        time=events[0][0]

        #Arrival event
        if(events[0][1]=="Arrival"):
            if(not isServing):
                #setting ls(t) to 1
                isServing=True
                customerNo=events[0][2]


                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure",customerNo])
                #! eğer is serving değilse aynı customer için bi tane daha list entery oluşturuyo
                #customer entity stored as customer no , arrival time, departure time, service time and que time
                customers.append([customerNo,time,time+randDeparture,randDeparture,time+randDeparture-(randDeparture+time)]) #que time=departure time-service time-arrival time

                randArrival=randomExp(lambd)
                events.append([time+randArrival,"Arrival",customerNo+1])

                customers.append([customerNo+1,time+randArrival,None,None,None])
                #TODO collect statistics
                events.pop(0)

            else:
                customerNo=events[0][2]
                customersinQue+=1
                randArrival=randomExp(lambd)
                events.append([time+randArrival,"Arrival",customerNo+1])

                customers.append([customerNo+1,time+randArrival,None,None,None])

                events.pop(0)
                #TODO collect statistics

        #Departure event
        elif(events[0][1]=="Departure"):
            if(customersinQue>0):
                customerNo=events[0][2]
                customersinQue-=1
                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure",customerNo+1])

                customers[customerNo+1][2]=time+randDeparture
                customers[customerNo+1][3]=randDeparture
                #que time = departure time- service time-arrival time
                customers[customerNo+1][4]=time+randDeparture-(randDeparture+customers[customerNo+1][1])

                #TODO collect statistics
                events.pop(0)
            else:

                """
                customerNo=events[0][2]
                customers[customerNo][2]=time
                """


                #setting ls(t) to 0
                isServing=False
                events.pop(0)

        #sorting the events acording to their time
        events.sort()

simulation(10,12,5)
