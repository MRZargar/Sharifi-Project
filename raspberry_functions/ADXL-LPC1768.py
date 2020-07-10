#!/usr/bin/python3

import time
import serial
import os
import os.path

def send_id(id):
    from send_request.GeoLabAPI import GeoLabAPI
    API = GeoLabAPI()
    while True:
        try:
            return API.send_raspberry_id(id)
        except Exception as ex:
            time.sleep(0.5)
            continue

send_id(12345678)

ser = serial.Serial(
        port='/dev/ttyAMA1',    #ttyAMA1 for uart4
        baudrate = 203125,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)

tmp_var=[0]
RX_tmp=[0]
LEA=[0]*18
MPU=[0]*19
ADXL=[0]*16

GPS_Week=0
GPS_Second=0

cnt_write=0
cnt_tmp =0

inx_zero = 0;
elapsed=0
cnt_file=0

ADXL_time=0
acc_x = 0
acc_y = 0
acc_z = 0
scale_factor = 0.00000390625*9.80665
ADXL_Temp = 0

path_obs='/home/pi/Obs/'

while 1:
    cnt_tmp
    RX_tmp=ser.read(1)
    if len(RX_tmp):
        tmp_var[0] = RX_tmp[0]
        if (tmp_var[0]==165):
            t=time.time()
            while 1:
                RX_tmp=ser.read(1)
                if len(RX_tmp):
                    tmp_var[0] = RX_tmp[0] 
                    if (tmp_var[0]==98):
                        while 1:
                            RX_tmp=ser.read(1)
                            if len(RX_tmp):
                                tmp_var[0] = RX_tmp[0]
                                if (tmp_var[0]==6):
                                    while 1:
                                        RX_tmp=ser.read(1)
                                        if len(RX_tmp):
                                            tmp_var[0] = RX_tmp[0]
                                            if (tmp_var[0]==49):
                                                cnt_lea = 0
                                                while 1:
                                                    if (cnt_lea==18):
                                                        inx_zero=1
                                                        t=time.time()
                                                        GPS_Week=LEA[9]*256+LEA[8]
                                                        GPS_Second=((LEA[3]*16777216+LEA[2]*65536+LEA[1]*256+LEA[0])+(LEA[7]*16777216+LEA[6]*65536+LEA[5]*256+LEA[4])*0.00000000023283064)/1000+(LEA[17]*16777216+LEA[16]*65536+LEA[15]*256+LEA[14]-1)
                                                        dir_week=str("{0:04d}".format(GPS_Week))
                                                        if ((GPS_Second%3600)==0)|(cnt_write==0):
                                                            cnt_file = cnt_file + 1
                                                            cnt_write=0
                                                            if (cnt_write):
                                                                f.close()
                                                            if (os.path.isdir(path_obs)==False):
                                                                os.mkdir(path_obs)
                                                            file_name=path_obs+str("{0:04d}".format(GPS_Week))+str("{0:06d}".format(int(GPS_Second)))+'.txt'
                                                            f=open(file_name,'w')
                                                            print('*** New file was generated.')
                                                        
                                                        print('#file:',str(cnt_file),' #Epoch per file (sec):',str(cnt_write),'    GPS Week:',str(GPS_Week),'    GPS Second:',str(GPS_Second))
                                                        cnt_write = cnt_write + 1
                                                        
                                                        break
                                                    RX_tmp=ser.read(1)
                                                    if len(RX_tmp):
                                                        tmp_var[0] = RX_tmp[0]
                                                        LEA[cnt_lea] = tmp_var[0]
                                                        cnt_lea = cnt_lea + 1
                                            elif (tmp_var[0]==0):
                                                cnt_mpu = 0
                                                while 1:
                                                    if (cnt_mpu==19):
                                                        break
                                                    RX_tmp=ser.read(1)
                                                    if len(RX_tmp):
                                                        tmp_var[0] = RX_tmp[0]
                                                        MPU[cnt_mpu] = tmp_var[0]
                                                        cnt_mpu = cnt_mpu + 1
                                            elif (tmp_var[0]==1):
                                                cnt_adxl = 0
                                                while 1:
                                                    if (cnt_adxl==16):
                                                        if (inx_zero):
                                                            ADXL_time = GPS_Second + ((ADXL[15]*16777216+ADXL[14]*65536+ADXL[13]*256+ADXL[12])/(LEA[13]*16777216+LEA[12]*65536+LEA[11]*256+LEA[10]))
                                                            f.write('%.3f ' % ADXL_time)
                                                            acc_z = ADXL[0]*4096+ADXL[1]*16+ADXL[2]/16
                                                            if (acc_z>524288):
                                                                acc_z = -(1048576-acc_z)
                                                            acc_z = acc_z*scale_factor
                                                            acc_x = ADXL[5]*4096+ADXL[6]*16+ADXL[7]/16
                                                            if (acc_x>524288):
                                                                acc_x = -(1048576-acc_x)
                                                            acc_x = acc_x*scale_factor
                                                            acc_y = ADXL[8]*4096+ADXL[9]*16+ADXL[10]/16
                                                            if (acc_y>524288):
                                                                acc_y = -(1048576-acc_y)
                                                            acc_y = acc_y*scale_factor
                                                            ADXL_Temp = (((ADXL[3]*256+ADXL[4]) - 1852)/(-9.05)) + 25;
                                                            f.write('%.4f ' % acc_x)
                                                            f.write('%.4f ' % acc_y)
                                                            f.write('%.4f ' % acc_z)
                                                            f.write('%.2f\n' % ADXL_Temp)
                                                            elapsed=(time.time()-t)*1000
                                                        break
                                                    RX_tmp=ser.read(1)
                                                    if len(RX_tmp):
                                                        tmp_var[0] = RX_tmp[0]
                                                        ADXL[cnt_adxl] = tmp_var[0]
                                                        cnt_adxl = cnt_adxl + 1
                                            else:
                                                print('Wrong data',str(tmp_var[0]))
                                                break
                                            break
                                else:
                                    break
                                    break
                                break
                    else:   
                        break
                    break
    cnt_tmp=cnt_tmp+1
f.close()



