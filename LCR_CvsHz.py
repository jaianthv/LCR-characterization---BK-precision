from Gpib import *
import time
import sys 
import os

v=Gpib('LCR')


v.write('*CLS')
v.write('*CLS')

# sets function to parallel capacitance and parallel resistance
v.write('FUNC:IMP CPRP')

# sets the measuring voltage to 5mV, one can increase more for better s/n 
v.write('VOLTage 0.005')

# number of averages, there is a delay in the communication, therefore it is better to keep this as 1, and measure many cycle as I did below
v.write('APER FAST,1')

# list of frequencies you wish to measure
Freq = [20,50,100,300,500,700,1e3,3e3,5e3,7e3,10e3,30e3,50e3,70e3,100e3,300e3,500e3,700e3,800e3,900e3,1e6];

#define sample name
Sample = "electrolitic_12032019";

#create folder with sample name
os.makedirs(Sample)

# move to the folder
os.chdir('/home/mokeuser/Downloads/linux-gpib-4.0.4rc2/language/python/'+Sample)


#starts measurements from here and we make two measurement cycles with C vs Freq
for j in range(0,2): # please change the number of cycles accordingly

    #Files will be saved with the sample name and number C vs Freq sweep defined as "i"
    filename=open("CP_RP_"+Sample+"_%i.txt"%j,"a");

    for i in range(0,len(Freq)):
        v.write('FREQ %e'%Freq[i]);
        # it is important to give this 15 s time for the instrument to set the frequency
        time.sleep(15);
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
v.write('FUNC:IMP CSRS')

# sample is repeated for series capacitance and resistance

for k in range(0,2): # please change the number of cycles accordingly

    filename=open("CS_RS_"+Sample+"_%i.txt"%k,"a");

    for i in range(0,len(Freq)):
        v.write('FREQ %e'%Freq[i]);
        time.sleep(15);
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




