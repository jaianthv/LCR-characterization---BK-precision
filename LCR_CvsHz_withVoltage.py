#import gpib
from Gpib import *
import time
import sys 
import os

v=Gpib('LCR')
v.write('*CLS')
v.write('*CLS')
# sets the measuring voltage, one can increase more for better s/n 
v.write('VOLTage 0.150')
# number of averages, there is a delay in the communication, therefore it is better to keep this as 1, and measure many cycle as I did below
v.write('APER FAST,1')

# List of frequencies to measure

#Freq = [20,30,50,100,200,300,400,500,600,700,800,900,1e3,1.5e3,2e3,2.5e3,3e3,3.5e3,4e3,4.5e3,5e3,5.5e3,6e3,6.5e3,7e3,7.5e3,8e3,8.5e3,9e3,9.5e3,10e3,15e3,20e3,25e3,30e3,35e3,40e3,45e3,50e3,55e3,60e3,65e3,70e3,75e3,80e3,85e3,90e3,95e3,100e3,150e3,200e3,250e3,300e3,350e3,400e3,450e3,500e3,550e3,600e3,650e3,700e3,750e3,800e3,850e3,900e3,950e3,1e6]
Freq = [20,30,50,100,300,500,700,1e3,3e3,5e3,7e3,10e3,30e3,50e3,70e3,100e3,300e3,500e3,700e3,800e3,900e3,1e6];

#define sample name
Sample = "Al2O3";

#create folder with sample name
os.makedirs(Sample)
os.chdir('/home/mokeuser/Downloads/linux-gpib-4.0.4rc2/language/python/'+Sample)

# Sets DC voltage(s) measure capacitance as a function fo frequency 

# list of DC bias voltage

#volts=[0,1,2,3,4,5,4,3,2,1,0,-1,-2,-3,-4,-5,-4,-3,-2,-1,0];
volts=[0,0.1,0.2,0.3,0.4,0.5,0.4,0.3,0.2,0.1,0,-0.1,-0.2,-0.3,-0.4,-0.5,-0.4,-0.3,-0.2,-0.1,0];

# measurements start from here

for l in range(0,len(volts)):
    
# Turn on the DC bias, make sure you press the button before the measurement starts
    v.write('OUTP:DC:ISOL 1')
    v.write('BIAS:STATe 1');
    #set the DC bias
    v.write('BIAS:VOLT %sV'%volts[l]);
    # wait for 30s to stabilize
    time.sleep(30);
    v.write('*CLS')
    v.write('*CLS')
    # set to function parallel and series resistance
    v.write('FUNC:IMP CPRP')
    #wait 15 s
    time.sleep(15);


    #Measure the capacitance and resistance
    for j in range(0,3): # change average according to your needs

        filename=open("CP_RP_"+Sample+"_%i_%i_V_%i.txt"%(j,volts[l]*10,l),"a");

        for i in range(0,len(Freq)):
            v.write('FREQ %e'%Freq[i]);
            time.sleep(16);
            print Freq[i];
            v.write('FETC?')
            X = v.read();
            print X;
            split = X.split(',');
            C = split[0];
            R = split[1];
             #data will be saved with first column as freqeuncy, second column with capacitance and third column with resistance 
            filename.write("%e %s %s\n"%(Freq[i],C,R));
        filename.close()
    v.write('*CLS')
    v.write('*CLS')
    # set function to series and parallel capacitance and resistance repeat what was done in the previous loop
    v.write('FUNC:IMP CSRS')
    time.sleep(15);

    for k in range(0,3): # change average according to your needs
        filename=open("CS_RS_"+Sample+"_%i_%i_V_%i.txt"%(k,volts[l]*10,l),"a");

        for i in range(0,len(Freq)):
            v.write('FREQ %e'%Freq[i]);
            time.sleep(16);
            print Freq[i];
            v.write('FETC?')
            X = v.read();
            print X;
            split = X.split(',');
            C = split[0];
            R = split[1];
            filename.write("%e %s %s\n"%(Freq[i],C,R));
        filename.close()


os.chdir('/home/mokeuser/Downloads/linux-gpib-4.0.4rc2/language/python')




