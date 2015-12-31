import time

class DS18B20:

    def __init__(self, device_file):
	#Sensor ID info so we know which file to look at
	self.device_file = device_file
	#A value we can modify and return at anytime, allows to calculate change in temp
	self.last_temp = 0.0

    def read_temp_raw(self):
	f = open(self.device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
 
    def read_temp(self):
	lines = self.read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
	self.last_temp = temp_c
        return temp_c

    def get_delta(self):
	start_temp = self.last_temp
	end_temp = self.read_temp()
	delta_temp = end_temp - start_temp
	return delta_temp
