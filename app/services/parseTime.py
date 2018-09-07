import datetime


def parseTime(input_str, n):
	if input_str == '0000-00-00 00:00:00' or input_str is None:
		input_str_add_3 = datetime.datetime.now() + datetime.timedelta(days=3)
		input_str = str(datetime.datetime.combine(input_str_add_3, datetime.time(23, 59, 59)))

	input_str=input_str.split()
	input_str=input_str[0].split('-')
	input_str=[int(a) for a in input_str]
	mydict={}
	if input_str[0]%4==0:
		mydict={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
	else:
		mydict={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
	
	date=input_str[2]
	mth=input_str[1]
	yr=input_str[0]
	output_day, output_mth, output_yr="","",""
	if (date+n)>mydict[mth]:	
		date=(date+n)%mydict[mth]
		if mth==12:
			mth=1
			yr=yr+1
		else:
			mth=mth+1
	else:
		date=date+n
	if mth<10:
		output_mth="0"+str(mth)
	else: 
		output_mth=str(mth)
	if date<10:
		output_date="0"+str(date)
	else:
		output_date=str(date)
	return (str(yr)+"-"+output_mth+"-"+output_date)