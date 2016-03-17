
import requests, re, datetime
from copy import deepcopy

class Panel:

     def __init__(self):
	self.panel_data = []
	self.panels =['16322224','16322207','16322217','16322204','16322219','16322205','16322211','16322229','16322209','16322206',\
          '16322216','16322234','16322222','16322232','16322208','16322221','16322218','16322212','16322223','16322231',\
          '16322236','16322230','16322226','16322225','16322214','16322220','16322227','16322235','16322233','16322228',\
          '16322203','16322215','16322210','16322213']

	self.field_list = {'Voltage _V_':'voltage','Power _W_':'power','Optimizer Voltage _V_':'opt_volt','Current _A_':'current','Last Measured':'last','Serial Number':'serial','Model':'model','Manufacturer':'manufacturer','Name':'name','energy':'energy'}
	self.headers = {'Host':'monitoring.solaredge.com',\
'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',\
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
'Accept-Language': 'en-US,en;q=0.5',\
'Accept-Encoding': 'gzip, deflate',\
'DNT': '1',\
'X-Requested-With': 'XMLHttpRequest',\
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',\
'Referer': 'https://monitoring.solaredge.com/solaredge-web/p/main',\
'Content-Length': '432',\
'Cookie': 'JSESSIONID=SANITIZED',\
'Connection': 'keep-alive',\
'Pragma': 'no-cache',\
'Cache-Control': 'no-cache'}

	self.payload = {'fieldId':'SANITIZED',\
'panelId':'se-schematics-container',\
'public':'false','r':self.panels}

	for each in self.panels:
   	  self.panel_data.append({'id':each})
	
     def get_panel_data(self):
     		
       try:
	r = requests.post("https://monitoring.solaredge.com/solaredge-web/p/systemDataTable", headers=self.headers, data=self.payload)

	for each in self.panel_data:
	    match = re.finditer("Ext.apply\(dataEl"+each['id']+",\{'(.*)':'(.*)'\}",r.text)
    	    for val in match:
		key = self.field_list[val.group(1)]
	        value = val.group(2)
		if key == 'name':
		   value = value[22:24]
		if key == 'last':
		#Mon Nov 16 16:36:52 GMT 2015
	           convert = datetime.datetime.strptime(value[4:],"%b %d %H:%M:%S %Z %Y")
		   value = datetime.datetime.strftime(convert,'%Y-%m-%d %H:%M')
		each[key] = value
		
	#return self.panel_data
	#Just pull out the desired stuff. Not sure why  I did it this way?
	final_data = deepcopy(self.panel_data)
	for each in final_data:
		each.pop("serial",None)
		each.pop("manufacturer",None)
		each.pop("model",None)
		each.pop("energy",None)
		each.pop("id",None)
	return final_data
	
       except:
	print "Error getting data from SolarEdge Web"
	return 
