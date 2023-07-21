import os
import datetime as dt
import csv
import glob

os.chdir(r'path')
cwd = os.getcwd()

#declare current period and store as value

timebegin = dt.datetime.now()
print("Start Time: "+str(timebegin))
currperiod = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")

#generate csv based on current period

row_count_sheet = ("CSV Row Count - {}").format(currperiod)

with open('{}.csv'.format(row_count_sheet), 'w') as creating_new_csv_file: 
   pass 
print("Successfully created file: {}".format(currperiod))

#iterate through each csv
#count the number of records (rows) in each csv
#write the csv name, number of rows, and whether the count is less than 2 million rows as a new line in the generated csv

result = [i for i in glob.glob('*.{}'.format("csv"))]

for i in result:
   with open(i, 'r', encoding="latin-1") as csvfile:
      csv_name = i
      count = str(len(csvfile.readlines()) - 1)
      count_len = len(csvfile.readlines())
      if count_len > 2000000:
         right_size = 'too large'
      else:
         right_size = 'good'
      print(csv_name,' : ',count, ' : ', right_size)
      columns = [csv_name,' has ',count,' rows : ',right_size]
      with open('{}.csv'.format(row_count_sheet),'a', newline= '\n') as csvfile:
         #appends data to new line
         my_writer = csv.writer(csvfile, delimiter= '\t',lineterminator='\n')
         for i in range (0,1):
            #looks at the next 1 record and writes the 'columns' variable to the line
            row = [i]
            my_writer.writerow(columns)
