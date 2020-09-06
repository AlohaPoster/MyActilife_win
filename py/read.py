# This is 8g + 16g
import argparse
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import re
#from pandas.plotting import register_matplotlib_converters

xtick = []
xtick_label = []
basename = ""
delta_time = datetime.timedelta(seconds=0.0)
def main():
    global basename
    global delta_time
    parser = argparse.ArgumentParser(description='Read SD Card and save into CSV file')
    parser.add_argument('-p', metavar='PATH', type=str, help='Path to SD Card')
    parser.add_argument('-d', metavar='UID', type=str, help='Device ID')
    parser.add_argument('-u', metavar='UID', type=str, help='User ID')
    parser.add_argument('-n', metavar='filename', type=str)
    parser.add_argument('-c', metavar='csvpath', type=str)

    args = parser.parse_args()
    if args.p == None:
        print("Error, no device path!")
        return
    if args.d == None:
        print("Error, no device id!")
    if args.u == None:
        print("Error, no user id!")
        return
    path = args.p       # Get path from command line
    n_blocks, id1, id2, id3, id4 = get_block_count(path)
    if n_blocks == 1:       # No samples to read from SD
        raise DataError 

    byte_array = np.fromfile(path, dtype=np.uint8, count=512 * n_blocks, sep="")

    try:
        time_data = byte_array[512+1020:512+1024]
        #time_data = byte_array[512+4092:512+4096] # Initial timestamp from first data block
        start_time = get_time(time_data)        # Convert to readable time
        end_time = get_time(byte_array[-4:])

        deltaT = (end_time - start_time).total_seconds() / (85.0 * (n_blocks-1))

        delta_time = datetime.timedelta(seconds=deltaT)

        startDate = start_time.strftime('%x').split('/')
        startDate = startDate[0] + '_' + startDate[1] + '_' + startDate[2]

        startTime = start_time.strftime('%X').split(':')
        startTime = startTime[0] + '_' + startTime[1] + '_' + startTime[2]

        absT, relT, x_acc, y_acc, z_acc = get_sample_adxl362(byte_array, start_time) # Parse all samples

    except:
        time_data = byte_array[512+4092:512+4096]       # Initial timestamp from first data block
        start_time = get_time(time_data)        # Convert to readable time
        end_time = get_time(byte_array[-4:])

        #deltaT = (end_time - start_time).total_seconds() / (85.25 * (n_blocks-1))
        deltaT = (end_time - start_time).total_seconds() / (85.0 * (n_blocks-1))
        delta_time = datetime.timedelta(seconds=deltaT)

        startDate = start_time.strftime('%x').split('/')
        startDate = startDate[0] + '_' + startDate[1] + '_' + startDate[2]

        startTime = start_time.strftime('%X').split(':')
        startTime = startTime[0] + '_' + startTime[1] + '_' + startTime[2]

        absT, relT, x_acc, y_acc, z_acc = get_sample_icm20948(byte_array, start_time) # Parse all samples

    samples = {'abs_time': [],
               'rel_time': [],
               'x_acc': [],
               'y_acc': [],
               'z_acc': [],
               }
    samples['abs_time'] = absT
    samples['rel_time'] = relT
    samples['x_acc'] = x_acc
    samples['y_acc'] = y_acc
    samples['z_acc'] = z_acc

    data = pd.DataFrame(data=samples)
    SDID = str(id4) + str(id1)
    mm, ss = divmod(data.iloc[-1]['rel_time'], 60)
    hh, mm = divmod(mm, 60)
    hms_time = str(int(hh)) + ' hours, ' + str(int(mm)) + ' minuts, ' + str(int(ss)) + ' seconds'
    realname = args.c +"/"+args.n + '.csv'
    infoname = args.c +"/"+args.n + '.txt'

    info = {'starttime':start_time,
            'endtime':end_time,
            'samplefrequency':"50Hz",
            'deviceid':args.d,
            'userid':args.u,
            'startdate':startDate,
            'SDid':SDID,
            'durationtime':hms_time,
            'localtion':realname
            }
    print("START TIME:", start_time)
    print("END TIME:", end_time)
    print("START DATA:", startDate)
    print("DELTAT TIME:", delta_time)
    print("Saving into file %s" %(realname))
    with open(infoname, 'w') as f:       # Write file information
        f.write("设备号: %s\n" % args.d)
        f.write("使用者号: %s\n" % args.u)
        f.write("SD卡编号: %s\n" % info['SDid'])
        f.write("测试开始日期: %s\n" % info['startdate'])
        f.write("测试开始时间: %s\n" % info['starttime'])
        f.write("测试持续时间: %s\n" % info['durationtime'])
        f.write("测试结束时间: %s\n" % info['endtime'])
        f.write("测试频率: %s\n" % info['samplefrequency'])

    data.to_csv(realname, mode='a', index=False)       # Write samples to csv

    get_xtick(data[1:]['abs_time'], data[1:]['rel_time'], 12)
    plot_axis(data[1:]['x_acc'], data[1:]['rel_time'], 'X-axis', args.c, args.n)  # Plot and save each axis separately
    plot_axis(data[1:]['y_acc'], data[1:]['rel_time'], 'Y-axis', args.c, args.n)
    plot_axis(data[1:]['z_acc'], data[1:]['rel_time'], 'Z-axis', args.c, args.n)
    combo_plot(data[1:]['x_acc'], data[1:]['y_acc'], data[1:]['z_acc'], data[1:]['rel_time'], args.c, args.n)  # Create plot with all axes

def get_xtick(time, rel_time, interval):
    global xtick
    global xtick_label

    interval = 60 * interval

    begin_time = time[1]
    year = begin_time[0:4]
    month = begin_time[5:7]
    day = begin_time[8:10]
    hour = begin_time[11:13]

    timedelta_hour = datetime.datetime.strptime(year + '-' + month + '-' + day + '_' + hour, '%Y-%m-%d_%H')
    timedelta_hour = timedelta_hour + datetime.timedelta(hours=1)

    flag = 0
    xtick = []
    xtick_label = []

    search_str = timedelta_hour.strftime("%Y-%m-%d") + '_' + timedelta_hour.strftime("%H:%M")
    i = 1
    while i < len(time):
        if flag:
            timedelta_hour = timedelta_hour + datetime.timedelta(minutes=interval)
            search_str = timedelta_hour.strftime("%Y-%m-%d") + '_' + timedelta_hour.strftime("%H:%M")
            flag = 0
        current_line_time = time[i]
        if re.match(search_str, current_line_time):
            flag = 1
            xtick.append(rel_time[i])
            xtick_label.append(current_line_time[8:10] + '_' + current_line_time[11:13])
            i = i + interval * 60 * 40
        i = i + 1

def get_sample_adxl362(byte_array, start_time):
    """
    Generator that takes byte array and yields x, y, and z axis sample data as well as
    the timestamp for each block.
    :param byte_array: byte data from SD
    :param start_time: initial timestamp for calculating elapsed time in seconds
    :return: acceleration sample data
    """
    data_blocks = byte_array[512:]      # First 512 bytes store info for block_count
    rel_time = datetime.timedelta(seconds=0.0)
    absT = []
    relT = []
    x_acc = []
    y_acc = []
    z_acc = []
    #last_time = start_time
    for i in range(1024, len(data_blocks), 1024): # we skip the first 2 blocks
        data = data_blocks[i:i+1020]       # Last 4 bytes of every block is time stamp data
        #time_stamp = data_blocks[i+1020:]		# Get time stamp data from end of block
        #curr_time = get_time(time_stamp)
        #deltaT = (curr_time - last_time).total_seconds() / 150.0
        #delta_time = datetime.timedelta(seconds=deltaT)
        #last_time = curr_time

        for j in range(0, len(data), 6):
            sample = data[j:j + 6]
            x_axis = sample[:2]
            y_axis = sample[2:4]
            z_axis = sample[4:]
            
            x_acc.append(convert_axis_adxl362(x_axis, 0b00)/np.float(235))
            y_acc.append(convert_axis_adxl362(y_axis, 0b01)/np.float(235))
            z_acc.append(convert_axis_adxl362(z_axis, 0b10)/np.float(235))
            relT.append(rel_time.total_seconds())
            absT.append(str(start_time + rel_time).replace(' ', '_', 1)) 
            rel_time += delta_time

    return absT, relT, x_acc, y_acc, z_acc   

def get_sample_icm20948(byte_array, start_time):
    """
    Generator that takes byte array and yields x, y, and z axis sample data as well as
    the timestamp for each block.
    :param byte_array: byte data from SD
    :param start_time: initial timestamp for calculating elapsed time in seconds
    :return: acceleration sample data
    """
    data_blocks = byte_array[512:]      # First 512 bytes store info for block_count
    rel_time = datetime.timedelta(seconds=0.0)
    absT = []
    relT = []
    x_acc = []
    y_acc = []
    z_acc = []
    #last_time = start_time
    for i in range(4096, len(data_blocks), 4096): # we skip the first 8 blocks
        data = data_blocks[i:i+4092]       # Last 4 bytes of every block is time stamp data
        #time_stamp = data_blocks[i+1020:]      # Get time stamp data from end of block
        #curr_time = get_time(time_stamp)
        #deltaT = (curr_time - last_time).total_seconds() / 150.0
        #delta_time = datetime.timedelta(seconds=deltaT)
        #last_time = curr_time

        for j in range(0, len(data), 6):
            sample = data[j:j + 6]
            x_axis = sample[:2]
            y_axis = sample[2:4]
            z_axis = sample[4:]
            
            x_acc.append(convert_axis_icm20948(x_axis)*16.0/32768.0)
            y_acc.append(convert_axis_icm20948(y_axis)*16.0/32768.0)
            z_acc.append(convert_axis_icm20948(z_axis)*16.0/32768.0)
            relT.append(rel_time.total_seconds())
            absT.append(str(start_time + rel_time).replace(' ', '_', 1)) 
            rel_time += delta_time

    return absT, relT, x_acc, y_acc, z_acc

def get_block_count(path):
    """
    Read in first block of data and get total number of blocks written on SD card
    :param path: path to SD card
    :return: number of blocks written on SD
    """

    data = np.fromfile(path, dtype=np.uint8, count=512, sep="")		# Read first block from SD Card
    countFreq = {}
    for i in range(0, 64):
        block_count = bytes_to_int(data[(4*i):(4*i+4)])        # Convert 4 bytes to unsigned 32 bit integer
        if block_count not in countFreq:
            countFreq[block_count] = np.uint32(0)
        else:
            countFreq[block_count] += 1
    ret = np.uint32(0)
    freqMax = np.uint32(0)
    for count in countFreq.keys():
        if countFreq[count] > freqMax:
            freqMax = countFreq[count]
            ret = count
    id1 = bytes_to_int(data[256:260])
    id2 = bytes_to_int(data[260:264])
    id3 = bytes_to_int(data[264:268])
    id4 = bytes_to_int(data[268:272])
    return ret, id1, id2, id3, id4


def get_time(byte_array):
    """
    Given an array of bytes, convert to an integer timestamp and return formatted timestamp
    :param byte_array: 4 bytes corresponding to C time_t
    :return: formatted datetime timestamp
    """

    date_time = bytes_to_int(byte_array)        # Convert 4 bytes to unsigned 32 bit integer (equivalent to time_t) 
    return datetime.datetime.fromtimestamp(date_time)       # Return timestamp from datetime module


def bytes_to_int(byte_array):
    """
    Given a 4-byte array, convert into an unsigned 4-byte integer value
    :param byte_array: array of 4 bytes (LSB first, MSB last)
    :return: unsigned 4 byte-integer value
    """

    byte0 = np.uint32(byte_array[0])
    byte1 = np.uint32(byte_array[1])
    byte2 = np.uint32(byte_array[2])
    byte3 = np.uint32(byte_array[3])

    byte1 = np.left_shift(byte1, 8)
    byte2 = np.left_shift(byte2, 16)
    byte3 = np.left_shift(byte3, 24)

    tot = np.bitwise_xor(byte0, byte1)
    tot = np.bitwise_xor(tot, byte2)
    tot = np.bitwise_xor(tot, byte3)

    return tot


def convert_axis_adxl362(byte_array, axis):
    """
    Given a 2-byte array, convert to a 16-bit integer corresponding to acceleration data
    :param byte_array: 2-byte array representing a single axis' data
    :param axis: which axis the data is supposed to represent (x, y, or z based on order read from SD)
    :return: 16-bit integer corresponding to acceleration data
    """

    l_sig = np.uint16(byte_array[0])		# Get least significant byte
    m_sig = np.uint16(byte_array[1])		# Get most significant byte

    m_sig = np.left_shift(m_sig, 8)		# Shift and combine bytes
    tot = np.bitwise_xor(m_sig, l_sig)

    axis_bits = np.right_shift(tot, 14)		# Check axis bits against desired axis and raise error if don't match
    if axis_bits != axis:
        print('Trying ADXL362: Expected axis %d but got axis %d' % (axis, axis_bits))
        print('Now switch to ICM20948')
        raise AxisMismatchError

    sign_ext = 0        # Used for padding to 16 bits (since there is no 12 bit data type)
    if np.bitwise_and(tot, 0b0000100000000000):		# Sign extension is same as most significant bit (b11 or 12th bit)
        sign_ext = 1

    pos_data = np.bitwise_and(tot, 0b0000111111111111)		# Acceleration data is bottom 12 bits

    if sign_ext:
        pos_data = np.bitwise_or(pos_data, 0b1111000000000000)		# Pad with sign extension bit (to get to 16 bits)

    return np.int16(pos_data)		# Return signed integer value

def convert_axis_icm20948(byte_array):
    """
    Given a 2-byte array, convert to a 16-bit integer corresponding to acceleration data
    :param byte_array: 2-byte array representing a single axis' data
    :param axis: which axis the data is supposed to represent (x, y, or z based on order read from SD)
    :return: 16-bit integer corresponding to acceleration data
    """

    l_sig = np.uint16(byte_array[1])        # Get least significant byte
    m_sig = np.uint16(byte_array[0])        # Get most significant byte

    m_sig = np.left_shift(m_sig, 8)     # Shift and combine bytes
    tot = np.bitwise_xor(m_sig, l_sig)

    return np.int16(tot)        # Return signed integer value



class AxisMismatchError(Exception):
    """Wrong axis encountered in sample"""


class DataError(Exception):
    """No data to read from card"""

def plot_axis(axis, time, axis_name,rp,name):
    global basename
    global xtick
    global xtick_label
    """
    Plot a given axis against timestamps
    :param axis: axis data
    :param time: timestamp data (assumed linearly spaced)
    :param axis_name: name of axis (ex. x-axis).  Must have format _-axis
    :return: none; plot and save figure
    """

    fig = plt.figure(figsize=(25, 12))
    ax = fig.add_subplot(111)

    ax.plot(time, axis)
    ax.plot(time, np.zeros(len(axis)), 'k')

    ax.set_xticks(xtick)
    ax.set_xticklabels(xtick_label, rotation=30, fontsize='small')

    ax.set_title(axis_name)
    ax.set_ylabel(axis_name.split('-')[0])
    fig.savefig(rp+"/"+ name +"_" +axis_name)


def combo_plot(x, y, z, time, rp, name):
    global basename
    global xtick
    global xtick_label
    """
    Plot all axes in one figure (each plotted separately and then all on one shared plot)
    :param x: x data
    :param y: y data
    :param z: z data
    :param time: timestamp data
    :return: none; plot and save figure
    """

    fig = plt.figure(figsize=(25,12))
    ax = fig.add_subplot(111)
    # axes[1, 0].plot(time, z)
    # axes[1, 0].plot(time, np.zeros(len(z)), 'k')
    # axes[1, 0].set_title('Z-axis')

    # axes[1, 1].plot(time, x, 'r', alpha=0.5, label='X')
    # axes[1, 1].plot(time, y, 'g', alpha=0.5, label='Y')
    # axes[1, 1].plot(time, z, 'b', alpha=0.5, label='Z')
    # axes[1, 1].plot(time, np.zeros(len(x)), 'k')
    # axes[1, 1].set_title('X, Y, Z axes')
    # axes[1,1].legend()
    ax.plot(time, x, 'r', alpha=0.5, label='X')
    ax.plot(time, y, 'g', alpha=0.5, label='Y')
    ax.plot(time, z, 'b', alpha=0.5, label='Z')
    ax.plot(time, np.zeros(len(x)), 'k')
    ax.set_title('X, Y, Z axes')
    ax.legend()

    ax.set_xticks(xtick)
    ax.set_xticklabels(xtick_label, rotation=30, fontsize='small')


    # axes[0, 0].set_xticks(xtick)
    # axes[0, 0].set_xticklabels(xtick_label, rotation=30, fontsize='small')

    # axes[0, 1].set_xticks(xtick)
    # axes[0, 1].set_xticklabels(xtick_label, rotation=30, fontsize='small')

    # axes[1, 0].set_xticks(xtick)
    # axes[1, 0].set_xticklabels(xtick_label, rotation=30, fontsize='small')

    # axes[1, 1].set_xticks(xtick)
    # axes[1, 1].set_xticklabels(xtick_label, rotation=30, fontsize='small')

    fig.savefig(rp+"/"+ name +"_" +"combined")



if __name__ == '__main__':
    main()
