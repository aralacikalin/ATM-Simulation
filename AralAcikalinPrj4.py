#Aral Açıkalın 20161701036
#written using python version 3.8.0 64-bit

import random
from timeit import default_timer as timer
import tabulate

def randomExp(lambd):
    '''Creating a random inter-arival time in seconds'''  
    #creates a random inter-arrival variable 
    #dividing lambda by 60 gives the rate of customers arriving per second so inter-arrival time is in seconds
    nextArrival=random.expovariate(lambd/60) 
    return nextArrival

def simulation(lambd,mean,capacity):
    #initialize the simulation, statistics, cumulative statistics.
    snapshot=[]
    queTime=0
    servedCustomerCount=0
    customersinSystem=0
    allSnapshots=[]
    customerLeft=0

    serviceTime=0
    cumulCustomersinQue=0
    cumulCustomersinSystem=0


    #initializing the system state
    customersinQue=0
    isServing=False
    time=0

    #customer entity list
    customers=[]

    #as first event creating a arrival event
    randArrival=randomExp(lambd)
    customerNo=0

    #stores events as time, event flag and customer no
    events=[[time+randArrival,"Arrival",customerNo]]
    while(servedCustomerCount<1000000):
        
        #set the clock to the events clock
        time=events[0][0]

        #Arrival event
        if(events[0][1]=="Arrival"):
            
            #if no one is in service creates one depature event for the current 
            #and one arrival event for the next customer
            if(not isServing):
                #setting ls(t) to 1
                isServing=True
                customerNo=events[0][2]

                #creating a departure event
                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure",customerNo])


                if(len(customers)-1==customerNo):
                    customers.pop(customerNo)
                #customer entity stored as customer no , arrival time, departure time, service time and que time
                customers.append([customerNo,time,time+randDeparture,randDeparture,time+randDeparture-(randDeparture+time)]) #que time=departure time-service time-arrival time

                #creating a arrival event
                randArrival=randomExp(lambd)
                events.append([time+randArrival,"Arrival",customerNo+1])

                customers.append([customerNo+1,time+randArrival,None,None,None])

                #pop the event that currently handled
                events.pop(0)
                customersinSystem=customersinQue+1

            else:
                #if capacity argument is 0 then there is no capacity in the simulation
                if(capacity!=0):
                    #checks if arrival is over capacity
                    if(capacity>customersinQue+1):
                        customerNo=events[0][2]
                        customersinQue+=1
                        customersinSystem=customersinQue+1

                        #creating a arrival event
                        randArrival=randomExp(lambd)
                        events.append([time+randArrival,"Arrival",customerNo+1])

                        customers.append([customerNo+1,time+randArrival,None,None,None])

                        #pop the event that currently handled
                        events.pop(0)
                    else:
                        customerNo=events[0][2]
                        customersinSystem=customersinQue+1
                        customerLeft+=1

                        customers.pop(customerNo)

                        #creating a arrival event
                        randArrival=randomExp(lambd)
                        events.append([time+randArrival,"Arrival",customerNo])

                        customers.append([customerNo+1,time+randArrival,None,None,None])

                        #pop the event that currently handled
                        events.pop(0)
                else:
                    customerNo=events[0][2]
                    customersinQue+=1
                    customersinSystem=customersinQue+1

                    #creating a arrival event
                    randArrival=randomExp(lambd)
                    events.append([time+randArrival,"Arrival",customerNo+1])

                    customers.append([customerNo,time+randArrival,None,None,None])

                    #pop the event that currently handled
                    events.pop(0)



        #Departure event
        elif(events[0][1]=="Departure"):

            #collecting cumulative service time
            if(customers!=[]):
                if(customers[events[0][2]][3]!=None):
                    serviceTime+=customers[events[0][2]][3]

            servedCustomerCount+=1
            #if queue is not empty create departure event for the next customer
            if(customersinQue>0):
                customerNo=events[0][2]
                customersinQue-=1
                customersinSystem=customersinQue+1

                #creating a departure event
                randDeparture=randomExp(mean)
                events.append([time+randDeparture,"Departure",customerNo+1])

                #setting departure time of the customer
                customers[customerNo+1][2]=time+randDeparture
                #setting service time of the customer
                customers[customerNo+1][3]=randDeparture
                #que time = departure time- service time-arrival time
                customers[customerNo+1][4]=time+randDeparture-(randDeparture+customers[customerNo+1][1])
                
                #pop the event that currently handled
                events.pop(0)
            else:

                customersinSystem=0
                #setting ls(t) to 0
                isServing=False
                events.pop(0)

        #sorting the events acording to their time
        events.sort()

        #collecting cumulative statistics
        cumulCustomersinSystem+=customersinSystem
        cumulCustomersinQue+=customersinQue

        #saving current snapshot
        tempEvent=events.copy()
        allSnapshots.append([time,customersinQue,isServing,customersinSystem,tempEvent,serviceTime,cumulCustomersinQue,cumulCustomersinSystem])

        #for printing the first 6 snapshots
        if(len(snapshot)<6):
            tempEvents=events.copy()
            snapshot.append([time,customersinQue,isServing,customersinSystem,tempEvents,serviceTime,cumulCustomersinQue,cumulCustomersinSystem])


    


    totalServiceTime=0
    customerCount=0
    for i in range(servedCustomerCount):
        if (not customers[i][4] == None) and (not customers[i][3] == None):
            queTime+=customers[i][4]
            totalServiceTime+=customers[i][3]
            customerCount+=1
    
    totalSystemTime=totalServiceTime+queTime

    #avarage of customers in queue and in system
    avarageNumberCustomersinQue=allSnapshots[len(allSnapshots)-1][6]/len(allSnapshots)
    avarageNumberCustomersinSys=allSnapshots[len(allSnapshots)-1][7]/len(allSnapshots)


    avarageSystemTime=totalSystemTime/customerCount
    avarageQue=queTime/customerCount
    avarageServiceTime=totalServiceTime/servedCustomerCount
    percentageCustomersLeft=(customerLeft/(servedCustomerCount+customerLeft))*100

    #table headers clock is current time, q is customers in queue,inSys is customers in system 
    #and right side of the future event list is the cumulative statistics
    headers=["Clock","Q","isSrv","Sys","Future Event List","srvTime","cQ","cSys"]
    print(tabulate.tabulate(snapshot,headers=headers),"\n")

    print("Customers Served Number: ",servedCustomerCount)
    print("Avarage Queue Time: " ,avarageQue)
    print("Avarage Service Time: ", avarageServiceTime)
    print("Avarage System Time: ", avarageSystemTime)
    print("Avarage Number of Customers in Queue: ", avarageNumberCustomersinQue)
    print("Avarage Number of Customers in Sys: ", avarageNumberCustomersinSys)
    print("Percentage of customers who cannot enter the ATM: %", percentageCustomersLeft)



def main():

    l=int(input("Enter λ: "))
    m=int(input("Enter µ: "))
    n=int(input("Enter Capacity(Enter 0 for infinite capacity): "))

    start=timer() #for outputing the run time of the code
    simulation(l,m,n)

    print("\nTime Elapsed: ",timer()-start," seconds.")


main()
