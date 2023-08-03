import sys
import os

if(len(sys.argv) < 2):
		print("Format -> handle.py <input_file>")
		exit()

input_file_name = sys.argv[1]
with open(input_file_name, "r") as input_file:
	data = input_file.read()
lines=data.split("\n")
no_of_lines=len(lines)
wqmc_format=""
total_weight = 0.0

for i in range(0,no_of_lines):
	if lines[i].startswith('('):
		#print(lines[i])
		left_part=lines[i].split(';')
		weight=left_part[1]
		weight=weight.replace(' ','')
		total_weight += int(weight)
#print(total_weight)

for i in range(0,no_of_lines-1):
	if lines[i].startswith('('):
		#print(lines[i])
		left_part=lines[i].split(';')
		#parts=lines[i].split(',')
		parts=left_part[0].split(',')
		weight=left_part[1]
		#total_weight += int(weight)
		weight=weight.replace(' ','')
		#weight = float(weight)
		#weight = str(weight/total_weight)
		#print(parts)
		#q1=parts[0][2:]
		q1=parts[0].replace('(','')
		q2=parts[1].replace(')','')
		q3=parts[2].replace('(','')
		q4=parts[3].replace(')','')
		#q2=parts[1][0:len(parts[1])-1]
		#q3=parts[2][1:]
		#q4=parts[3][0:len(parts[3])-5]
		wqmc_format=wqmc_format+q1+","+q2+"|"+q3+","+q4+":"+weight+"\n"
		
	
#print(wqmc_format)
out_file = input_file_name.split('.')[0] + "_wqmc.quartets"
with open(out_file, "w+") as f:
	f.write(wqmc_format)
