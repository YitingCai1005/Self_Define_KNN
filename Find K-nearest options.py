import pandas as pd
import math
import scipy.spatial
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


###################################################
###########Read data and clean data################
###################################################
NBO = pd.read_csv('Option.csv')
NBO_1=NBO.iloc[:,1:]

###################################################
###########Basic distance methods##################
###################################################
def Manhattan_dist_xx(x,t,columns,Scaling):  # calculate two x distance
    d=0.0
    for i in columns:  # Selected Columns
        d+=abs(t.loc[i]-x.loc[i])/Scaling[i]
    return d

def euclidean_distance(row,distance_columns,selected_option):
    inner_value = 0
    for k in distance_columns:
        inner_value += (row[k] - selected_option[k]) ** 2
    return math.sqrt(inner_value)

def correlation_distance(row,selected_option,distance_columns):
    correlation=scipy.spatial.distance.correlation(row[distance_columns],selected_option)
    return correlation

#######################################################
###########Calculate distance methods##################
#######################################################

#return 25 rows with entire information
def distance_K(selected_option,algorithm_input):
    print ".........Proceeding........"
    distance_columns=selected_option.keys().values.tolist()
    algorithm_input=algorithm_input.lower()
    if algorithm_input=='euclidean':
        distance_k = NBO_1.apply(euclidean_distance, args=(distance_columns, selected_option),axis=1).sort_values()[s:k].rename('Euclidean_distance')
    elif algorithm_input=='correlation':
        distance_k = NBO_1.apply(correlation_distance, args=(selected_option, distance_columns),axis=1).sort_values()[s:k].rename('Correlation_distance')
    elif algorithm_input=='manhattan':
        Scaling_s = NBO_1.apply(lambda x: x.max() - x.min())  # scaling min-max
        distance_k = NBO_1.apply(Manhattan_dist_xx, axis=1,args=(selected_option, distance_columns, Scaling_s)).sort_values()[s:k].rename('Manhattan_distance')
    else:
        return "No this distance method defined."

    NBO_withdistance = pd.concat([NBO.loc[distance_k.keys(), :], distance_k], axis=1)
    return NBO_withdistance

#obtain option information from user
def obtain_option():
    TT=dict()
    TT['Ask']=raw_input("Please enter Ask price(If not available please type 'N'):")
    TT['Bid']=raw_input("Please enter Bid price(If not available please type 'N'):")
    TT['LastPrice']=raw_input("Please enter LastPrice price(If not available please type 'N'):")
    TT['StockPrice'] = raw_input("Please enter StockPrice price(If not available please type 'N'):")
    TT['Strike'] = raw_input("Please enter Strike price(If not available please type 'N'):")
    TT['Volume'] = raw_input("Please enter Volume price(If not available please type 'N'):")
    TT['time_to_maturity'] = raw_input("Please enter time to maturity price(If not available please type 'N'):")

    Selected_dic=dict()
    for k, v in TT.iteritems():
        if v!='N':
           Selected_dic[k]=float(v)
    return pd.Series(Selected_dic)

def compare_plot(o,t,distance_method,*find_option):
    distance_method=distance_method.title()
    U_avg_iv=o['ImpliedVolatility'].mean()
    d_avg_iv=np.average(o['ImpliedVolatility'], weights=1/o.iloc[:,-1])
    U_avg_v=o['Volatility'].mean()
    d_avg_v=np.average(o['Volatility'], weights=1/o.iloc[:,-1])
    print '\nuniform average Implied Volatility:{}\ndistance weighted Implied Volatility:{}\nuniform average Volatility:{}\ndistance weighted Volatility:{}'.format(U_avg_iv,d_avg_iv,U_avg_v,d_avg_v)

    fig,axes=plt.subplots(nrows=1,ncols=2)

    axes[0].plot(o['{}_distance'.format(distance_method)],o['ImpliedVolatility'],'o',c='black')

    if find_option:
        axes[0].axhline(t['ImpliedVolatility'], xmin=0, xmax=1,color='g')
        axes[0].text(o.iloc[0]['{}_distance'.format(distance_method)],t['ImpliedVolatility']+0.01,'Original Option',color='g')
    axes[0].axhline(U_avg_iv, xmin=0, xmax=1,color='r')
    axes[0].text(o.iloc[0]['{}_distance'.format(distance_method)],U_avg_iv+0.01,'Uniform average value',color='r')
    axes[0].axhline(d_avg_iv, xmin=0, xmax=1,color='b')
    axes[0].text(o.iloc[-10]['{}_distance'.format(distance_method)],d_avg_iv+0.01,'Distance weighted value',color='b')

    axes[0].set_xlabel('{}_distance'.format(distance_method))
    axes[0].set_ylabel('{}'.format('ImpliedVolatility'))
    axes[0].set_title('{} of 25 Nearest Neighbors'.format('ImpliedVolatility'))


    axes[1].plot(o['{}_distance'.format(distance_method)],o['Volatility'],'o',c='black')

    if find_option:
        axes[1].axhline(t['Volatility'], xmin=0, xmax=1,color='g')
        axes[1].text(o.iloc[0]['{}_distance'.format(distance_method)],t['Volatility']+0.01,'Original Option',color='g')
    axes[1].axhline(U_avg_v, xmin=0, xmax=1,color='r')
    axes[1].text(o.iloc[0]['{}_distance'.format(distance_method)],U_avg_v+0.01,'Uniform average value',color='r')
    axes[1].axhline(d_avg_v, xmin=0, xmax=1,color='b')
    axes[1].text(o.iloc[-10]['{}_distance'.format(distance_method)],d_avg_v+0.01,'Distance weighted value',color='b')

    axes[1].set_xlabel('{}_distance'.format(distance_method))
    axes[1].set_ylabel('{}'.format('Volatility'))
    axes[1].set_title('{} of 25 Nearest Neighbors'.format('Volatility'))

    fig.canvas.draw()
    #plt.show(block=False)
    plt.pause(0.1)
    #plt.waitforbuttonpress(timeout=-1)
    raw_input("Press [enter] to continue.")
    #return next_step


#get distance calculating method, calculate
def calculate(option,*find_option):
    algorithm_type = raw_input(
        "Please choose distance calculation methods from following methods:\nEuclidean\nCorrelation\nManhattan")
    if find_option:
        K_neighbors = distance_K(option.drop(['ImpliedVolatility','Volatility']), algorithm_type)
        print "K nearest neighbors based on {}\n".format(algorithm_type)
        print K_neighbors
        print '----------------------------'
        print 'Original option\n'+str(option)
        compare_plot(K_neighbors,option,algorithm_type,find_option)
    else:
        K_neighbors = distance_K(option, algorithm_type)
        print "K nearest neighbors based on {}\n".format(algorithm_type)
        print K_neighbors
        print '----------------------------'
        print 'Original option\n' + str(option)
        compare_plot(K_neighbors, option, algorithm_type)

#main interactive with user
def main():
    find_option=True
    global k
    global s
    while find_option:
        k = 25
        s=0

        find_option = raw_input(
            "\n\nFIND K NEAREST NEIGHBORS\n================\n<1>Use option in the repertory, please enter the option index, for instance [5]\n<2>or Type New Data, please enter [N] then follow instruction enter value\n<.>Press [q] to exit. ")

        if find_option.lower()=='q':
            print 'BYE~~~'
            break
        elif find_option.lower()=='n':
            option=obtain_option()
            calculate(option)
        else:
            try:
                index=int(find_option)
                if index<len(NBO_1):
                    option=NBO_1.iloc[index]
                    k=k+1
                    s=s+1
                    calculate(option,find_option)
                else:
                    print "\nThe number you enter is out of range. Please enter number between [0,{})".format(len(NBO_1))

            except ValueError:
                print '\nThe letter you enter is wrong. Please enter N if you want type new data'
                continue


if __name__ == "__main__":
    main()


