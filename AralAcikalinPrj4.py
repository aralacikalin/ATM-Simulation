#Aral Açıkalın 20161701036
#written using python version 3.8.0 64-bit

import random
from timeit import default_timer as timer
import pandas

def randomExp(lambd):
    '''Creating a random inter-arival time in seconds'''  
    #creates a random inter-arrival variable 
    #dividing lambda by 60 gives the rate of customers arriving per second so inter-arrival time is in seconds
    nextArrival=random.expovariate(lambd/60) 
    return nextArrival

def simulation(lambd,mean,capacity):
    #initialize the simulation, statistics.
    snapshot=[]
    queTime=0
    servedCustomerCount=0 #!gerekebilir silinedebilir
    serviceTime=0


    #initializing the system state
    customersinQue=0
    isServing=False
    time=0

    #customer entity list
    customers=[]


    randArrival=randomExp(lambd)
    customerNo=0

    #stores events as time, event flag and customer no
    events=[[time,"Arrival",customerNo]]
    while(len(customers)<1000000): #TODO müşteri sayısı kadar loop yapmak için while ile değiştir
        
        #set the clock to the events clock
        time=events[0][0]
        

#TODO: capacity UNUTMA!!!
        #Arrival event
        if(events[0][1]=="Arrival"):
            if(not isServing):
                #setting ls(t) to 1
                isServing=True
                customerNo=events[0][2]


                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure",customerNo])
                #! eğer is serving değilse aynı customer için bi tane daha list entery oluşturuyo 
                #TODO ! çözülmüş olabilir ama daha çok kontrol et
                if(len(customers)-1==customerNo):
                    customers.pop(customerNo)
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
            servedCustomerCount+=1 #!gerekebilir silinedebilir
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
                #!test et burdayken customers arrayinde noluyo diye
                """
                customerNo=events[0][2]
                customers[customerNo][2]=time
                """


                #setting ls(t) to 0
                isServing=False
                events.pop(0)

        #sorting the events acording to their time
        events.sort()

        #saving current snapshot
        if(len(snapshot)<6):
            tempEvents=events.copy()
            snapshot.append([time,customersinQue,isServing,tempEvents])#!cumulatif istatistikler hakkında mail at


    collumns=["Clock","Customers in Que","isServing","Future Event List"]
    #table=pandas.DataFrame(snapshot,collumns)
    totalServiceTime=0
    customerCount=0
    for c in customers: #TODO cs sayısına göre düzenlenebilir
        if (not c[4] == None) and (not c[3] == None):
            queTime+=c[4]
            totalServiceTime+=c[3]
            customerCount+=1
    
    totalSystemTime=totalServiceTime+customerCount

    avarageSystemTime=totalSystemTime/customerCount
    avarageQue=queTime/customerCount
    avarageServiceTime=totalServiceTime/servedCustomerCount

    #print(table)
    

    print("q: " ,avarageQue , "s: ", avarageServiceTime, "cs :", customerCount, "c:",servedCustomerCount)



start=timer() #for outputing the run time of the code
simulation(10,12,5)

print("Time Elapsed: ",timer()-start," seconds.")
