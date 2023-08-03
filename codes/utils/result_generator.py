import os
import sys
import subprocess
import shutil
from shutil import copyfile
from subprocess import Popen, PIPE
import csv
import pandas as pd
from time import time
from codes.parameters import ASTRAL, COMPLETE, OUTPUT_FOLDER, WQFM

from codes.utils.file import join_dir

# base_dir = "/home/shashata/Documents/11_Taxon_Sim/15_genes"
# true_st_directory     = base_dir+"/"+"True_STs"
base_dir = ""
doing = ""
complete_astral_dir   = ""
complete_wqmc_dir     = ""
#incomplete_astral_dir = base_dir+"/"+"ASTRAL_sp_tree_Incomplete"
#incomplete_wqmc_dir   = base_dir+"/"+"WQMC_sp_tree_Incomplete"
# doing = "4-5"
incomplete_pnm_wqmc_dir = ""
incomplete_pnm_astral_dir = ""
imputed_st_pnm_dir= ""

# whole_gene_quartet
#imputed_st_pruner_dir="/home/arpita/Documents/Thesis/Final_utils_along_with_gene_trees/26-taxon-4_sets_of_species_trees/Imputed_ST_pruner"
#fp_removed_pnm_dir="/home/arpita/Documents/Thesis/Final_utils_along_with_gene_trees/26-taxon-4_sets_of_species_trees/SP_tree_Imputed_FP_Removed/Species_tree_Imputed_Prune-nam-modified-py"
#fp_removed_pruner_dir="/home/arpita/Documents/Thesis/Final_utils_along_with_gene_trees/26-taxon-4_sets_of_species_trees/SP_tree_Imputed_FP_Removed/Species_tree_Imputed_Prunener-py"

'''

Matrix
Col ->  Replicate Number	Complete (Astral)	Complete (WQMC)	Incomplete (Astral)	Incomplete (WQMC)	Imputed

'''
def checkEqual2(iterator):

	# return True
	# print(set(iterator))
	if(len(set(iterator)) > 1):
		print(set(iterator))
	# return True
	return len(set(iterator)) <= 1


def getFnFpRate_WQFM(base_dir,doing,gt_tail="_taxa/"):
	cols = 9
	
	complete_astral_dir   = base_dir+"/"+"Complete_ST"
	complete_wqfm_dir     = base_dir+"/Complete_ST_WQFM"
	complete_wqfm_sv_dir     = base_dir+"/Complete_ST_WQFM_SV"

	#incomplete_astral_dir = base_dir+"/"+"ASTRAL_sp_tree_Incomplete"
	#incomplete_wqmc_dir   = base_dir+"/"+"WQMC_sp_tree_Incomplete"
	# doing = "4-5"
	incomplete_pnm_wqfm_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/"+"Incomplete_GT/Species_tree_Missing_WQFM"
	incomplete_pnm_wqfm_sv_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/"+"Incomplete_GT/Species_tree_Missing_WQFM_SV"
	
	incomplete_pnm_astral_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/Incomplete_ST"
	
	imputed_st_pnm_wqfm_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_Missing_WQFM"
	imputed_st_pnm_wqfm_sv_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_Missing_WQFM_SV"


	csv_file = open("FnFpCalc_final_"+doing+"_TR_wqfm.csv", mode='w')
	fieldnames = ["Replicate_Number", 'Complete(Astral)', "Complete(WQFM)", "Complete(WQFM_SV)", "Incomplete(Astral)",
	"Incomplete(WQFM)","Incomplete(WQFM_SV)", "Imputed","Imputed_SV"]
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()
	# fl = open("FnFpCalc_final_"+doing+"_TR.res",'w+')
	true_sp_tree = base_dir + "/true-species.out.tree"
	for complete_astral_file in os.listdir(complete_astral_dir):
		row = ["--"]*cols
		file_sep_1 = complete_astral_file.split('_')[0]
		row[0] = file_sep_1
		# fl.write("For the replicate: " + file_sep_1+"\n")
		model_tree = complete_astral_dir + "/" + complete_astral_file
		res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',model_tree], encoding='UTF-8')
		
		res = res.replace("(","")
		res = res.replace(")","")
		res = res.replace("\n","")
		res = res.replace(" ","")
		backup = res
		res = res.split(",")
		if(checkEqual2(res) == True):
			row[1] = res[0]
		else:
			print("Different values of res - CA")
			print(res)
			row[1] = backup
			# row.append(res)
		# print(res)
		# fl.write("01) Result for comparing with complete astral " "\n")
		# fl.write(res + "\n")
		
		for complete_wqfm_file in os.listdir(complete_wqfm_dir):
			file_sep_4 = complete_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_4):
				complete_wqfm_tree=complete_wqfm_dir+"/"+complete_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',complete_wqfm_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[2] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[2] = backup
				# print(res)
				# fl.write("03) Result for comparing with complete wqmc " + "\n")
				# fl.write(res + "\n")
		
		for complete_wqfm_sv_file in os.listdir(complete_wqfm_sv_dir):
			file_sep_4 = complete_wqfm_sv_file.split('_')[-1]
			if(file_sep_1 == file_sep_4):
				complete_wqfm_tree=complete_wqfm_sv_dir+"/"+complete_wqfm_sv_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',complete_wqfm_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[3] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[3] = backup

		for incomplete_pnm_astral_file in os.listdir(incomplete_pnm_astral_dir):
			file_sep_7 = incomplete_pnm_astral_file.split('_')[0]
			if(file_sep_1 == file_sep_7):
				incomplete_pnm_astral_tree=incomplete_pnm_astral_dir+"/"+incomplete_pnm_astral_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_astral_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[4] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[4] = backup
				# #print(res)
				# fl.write("06) Result for comparing with Prune-nam-astral " +  "\n")
				# fl.write(res + "\n")

		for incomplete_pnm_wqfm_file in os.listdir(incomplete_pnm_wqfm_dir):
			file_sep_6 = incomplete_pnm_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_6):
				incomplete_pnm_wqfm_tree=incomplete_pnm_wqfm_dir+"/"+incomplete_pnm_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_wqfm_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[5] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[5] = backup
				#print(res)
				# fl.write("05) Result for comparing with Prune-nam-wqmc " + "\n")
				# fl.write(res + "\n")
		
		for incomplete_pnm_wqfm_sv_file in os.listdir(incomplete_pnm_wqfm_sv_dir):
			file_sep_6 = incomplete_pnm_wqfm_sv_file.split('_')[-1]
			if(file_sep_1 == file_sep_6):
				incomplete_pnm_wqfm_sv_tree=incomplete_pnm_wqfm_sv_dir+"/"+incomplete_pnm_wqfm_sv_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_wqfm_sv_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[6] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[6] = backup

		
		for imputed_st_pnm_wqfm_file in os.listdir(imputed_st_pnm_wqfm_dir):
			file_sep_9 = imputed_st_pnm_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_9):
				print("Imputed_st_pnm",file_sep_9)
				imputed_st_pnm_wqfm_tree=imputed_st_pnm_wqfm_dir+"/"+imputed_st_pnm_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',imputed_st_pnm_wqfm_tree], encoding='UTF-8')
				

				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[7] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[7] = backup

		for imputed_st_pnm_wqfm_file in os.listdir(imputed_st_pnm_wqfm_sv_dir):
			file_sep_9 = imputed_st_pnm_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_9):
				print("Imputed_st_pnm",file_sep_9)
				imputed_st_pnm_wqfm_tree=imputed_st_pnm_wqfm_sv_dir+"/"+imputed_st_pnm_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',imputed_st_pnm_wqfm_tree], encoding='UTF-8')
				

				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[8] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[8] = backup


		print(row,len(row))

		writer.writerow({"Replicate_Number": int(row[0]), "Complete(Astral)": row[1], "Complete(WQFM)": row[2], 
			"Complete(WQFM_SV)": row[3], "Incomplete(Astral)": row[4], "Incomplete(WQFM)": row[5],"Incomplete(WQFM_SV)": row[6], 
			"Imputed": row[7], "Imputed_SV": row[8]})
		# fl.write("-------------------------------------------------------------"+"\n\n")

	csv_file.close()

# def getRes():





def getFnFpRate_V2(base_dir,doing):

	complete_astral_dir   = base_dir+"/"+"Complete_ST"
	complete_wqmc_dir     = base_dir+"/"+"Complete_ST_WQMC"
	
	#incomplete_astral_dir = base_dir+"/"+"ASTRAL_sp_tree_Incomplete"
	#incomplete_wqmc_dir   = base_dir+"/"+"WQMC_sp_tree_Incomplete"
	# doing = "4-5"
	incomplete_pnm_wqmc_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/"+"Incomplete_GT/Species_tree_decoded_Missing_WQMC"
	incomplete_pnm_astral_dir = base_dir+"/Incomplete_ST_"+doing+"_taxa_removed/"
	imputed_st_pnm_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+"_taxa/" +"Species_tree_decoded_Imputed"

	csv_file = open("FnFpCalc_final_"+doing+"_TR.csv", mode='w')
	fieldnames = ["Replicate_Number", 'Complete(Astral)', "Complete(WQMC)", "Incomplete(Astral)","Incomplete(WQMC)", "Imputed"]
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()
	# fl = open("FnFpCalc_final_"+doing+"_TR.res",'w+')
	true_sp_tree = base_dir + "/true-species.out.tree"
	for complete_astral_file in os.listdir(complete_astral_dir):
		row = ["--"]*6
		file_sep_1 = complete_astral_file.split('_')[0]
		row[0] = file_sep_1
		# fl.write("For the replicate: " + file_sep_1+"\n")
		model_tree = complete_astral_dir + "/" + complete_astral_file
		res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',model_tree], encoding='UTF-8')
		
		res = res.replace("(","")
		res = res.replace(")","")
		res = res.replace("\n","")
		res = res.replace(" ","")
		backup = res
		res = res.split(",")
		if(checkEqual2(res) == True):
			row[1] = res[0]
		else:
			print("Different values of res - CA")
			print(res)
			row[1] = backup
			# row.append(res)
		# print(res)
		# fl.write("01) Result for comparing with complete astral " "\n")
		# fl.write(res + "\n")
		
		for complete_wqmc_file in os.listdir(complete_wqmc_dir):
			file_sep_4 = complete_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_4):
				complete_wqmc_tree=complete_wqmc_dir+"/"+complete_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',complete_wqmc_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[2] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[2] = backup
				# print(res)
				# fl.write("03) Result for comparing with complete wqmc " + "\n")
				# fl.write(res + "\n")
		
		for incomplete_pnm_astral_file in os.listdir(incomplete_pnm_astral_dir):
			file_sep_7 = incomplete_pnm_astral_file.split('_')[0]
			if(file_sep_1 == file_sep_7):
				incomplete_pnm_astral_tree=incomplete_pnm_astral_dir+"/"+incomplete_pnm_astral_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_astral_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[3] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[3] = backup
				# #print(res)
				# fl.write("06) Result for comparing with Prune-nam-astral " +  "\n")
				# fl.write(res + "\n")

		for incomplete_pnm_wqmc_file in os.listdir(incomplete_pnm_wqmc_dir):
			file_sep_6 = incomplete_pnm_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_6):
				incomplete_pnm_wqmc_tree=incomplete_pnm_wqmc_dir+"/"+incomplete_pnm_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_wqmc_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[4] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[4] = backup
				#print(res)
				# fl.write("05) Result for comparing with Prune-nam-wqmc " + "\n")
				# fl.write(res + "\n")
		
		
		for imputed_st_pnm_file in os.listdir(imputed_st_pnm_dir):
			file_sep_9 = imputed_st_pnm_file.split('_')[0]
			if(file_sep_1 == file_sep_9):
				print("Imputed_st_pnm",file_sep_9)
				imputed_st_pnm_tree=imputed_st_pnm_dir+"/"+imputed_st_pnm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',imputed_st_pnm_tree], encoding='UTF-8')
				

				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[5] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[5] = backup

		print(row,len(row))

		writer.writerow({"Replicate_Number": int(row[0]), "Complete(Astral)": row[1], "Complete(WQMC)": row[2], "Incomplete(Astral)": row[3], "Incomplete(WQMC)": row[4], "Imputed": row[5]})
		# fl.write("-------------------------------------------------------------"+"\n\n")

	csv_file.close()
	

def read_and_display(file_ind,doing,out_dir,back_=""):
	if(file_ind == "F"):
		file_name = out_dir+"/"+"FnFpCalc_final_"+doing+"_TR"+back_+".csv"
		out_file_name = out_dir+"/"+"FnFpCalc_final_"+doing+"_sorted_TR"+back_+".csv"
		out_file = open(out_file_name,"w")
	elif(file_ind == "Q"):
		global base_dir

		folder = base_dir.split("/")[-1]
		file_name = "Quartet_score_"+folder+"/Quartet_score_"+doing+"_TR"+back_+".csv"
		out_file_name = "Quartet_score_"+folder+"/Quartet_score_sorted_"+doing+"_TR"+back_+".csv"
		out_file = open(out_file_name,"w")
	
	subprocess.call(['csvsort','-c 1',file_name],stdout=out_file)
	os.remove(file_name)
	df = pd.read_csv(out_file_name)
	print(df)



def getFnFpRate(base_dir,doing):
	complete_astral_dir   = base_dir+"/"+"Complete_ST"
	complete_wqmc_dir     = base_dir+"/"+"Complete_ST_WQMC"
	#incomplete_astral_dir = base_dir+"/"+"ASTRAL_sp_tree_Incomplete"
	#incomplete_wqmc_dir   = base_dir+"/"+"WQMC_sp_tree_Incomplete"
	# doing = "4-5"
	incomplete_pnm_wqmc_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/"+"Incomplete_GT/Species_tree_decoded_Missing_WQMC"
	incomplete_pnm_astral_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/"+"Incomplete_ST"
	imputed_st_pnm_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Numpy_"+doing+"_Taxa/" +"Species_tree_decoded_Imputed"

	fl = open("FnFpCalc_final_"+doing+"_TR.res",'w+')
	true_sp_tree = base_dir + "/true-species.out.tree"
	print("Running " + doing + " Taxa Removed")
	fl.write("================== Simulation for "+doing+" Taxa Removed ===================\n")
	for complete_astral_file in os.listdir(complete_astral_dir):
		file_sep_1 = complete_astral_file.split('_')[0]
		fl.write("For the replicate: " + file_sep_1+"\n")
		model_tree = complete_astral_dir + "/" + complete_astral_file
		res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',model_tree], encoding='UTF-8')
		#print(res)
		fl.write("01) Result for comparing with complete astral " "\n")
		fl.write(res + "\n")
		
		for complete_wqmc_file in os.listdir(complete_wqmc_dir):
			file_sep_4 = complete_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_4):
				complete_wqmc_tree=complete_wqmc_dir+"/"+complete_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',complete_wqmc_tree],  encoding='UTF-8')
				#print(res)
				fl.write("03) Result for comparing with complete wqmc " + "\n")
				fl.write(res + "\n")
		
		for incomplete_pnm_wqmc_file in os.listdir(incomplete_pnm_wqmc_dir):
			file_sep_6 = incomplete_pnm_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_6):
				incomplete_pnm_wqmc_tree=incomplete_pnm_wqmc_dir+"/"+incomplete_pnm_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_wqmc_tree],  encoding='UTF-8')
				#print(res)
				fl.write("05) Result for comparing with Prune-nam-wqmc " + "\n")
				fl.write(res + "\n")
		for incomplete_pnm_astral_file in os.listdir(incomplete_pnm_astral_dir):
			file_sep_7 = incomplete_pnm_astral_file.split('_')[0]
			if(file_sep_1 == file_sep_7):
				incomplete_pnm_astral_tree=incomplete_pnm_astral_dir+"/"+incomplete_pnm_astral_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_astral_tree], encoding='UTF-8')
				#print(res)
				fl.write("06) Result for comparing with Prune-nam-astral " +  "\n")
				fl.write(res + "\n")
		
		for imputed_st_pnm_file in os.listdir(imputed_st_pnm_dir):
			file_sep_9 = imputed_st_pnm_file.split('_')[0]
			if(file_sep_1 == file_sep_9):
				print("Imputed_st_pnm",file_sep_9)
				imputed_st_pnm_tree=imputed_st_pnm_dir+"/"+imputed_st_pnm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',imputed_st_pnm_tree], encoding='UTF-8')
				#print(res)
				fl.write("08) Result for comparing with imputed st -> pnm " + "\n")
				fl.write(res + "\n")
		'''for fp_removed_pnm_file in os.listdir(fp_removed_pnm_dir):
			file_sep_10 = fp_removed_pnm_file.split('_')[3]
			if(file_sep_1 == file_sep_10):
				#print("Imputed_st_pnm fp removed:",file_sep_10)
				fp_removed_pnm_tree=fp_removed_pnm_dir+"/"+fp_removed_pnm_file
				res = subprocess.check_output(['getFpFn.py','-t',model_tree,'-e',fp_removed_pnm_tree])
				#print(res)
				fl.write("09) Result for comparing with imputed st -> pnm, fp removed " + "\n")
				fl.write(res + "\n")'''
		fl.write("-------------------------------------------------------------"+"\n\n")

	fl.close()


def split_token_and_send_Qscore(stderr):
	
	stderr = stderr.decode('UTF-8')

	if not "Final quartet" in stderr:
	
		print("Problem !!!!!!!")
		print(stderr)
		print("Problem !!!!!!!")

	for item in stderr.split("\n"):
		if "Final quartet" in item:
			score = item.strip().split(":")[1].strip()
			# print(score)
			return score

			# print(item.strip())



def calculate_Quartet_score(doing,output_dir,gt_tail):
	

	print("Now doing -> ", doing, "TR")

	start = time()
	global base_dir

	folder = base_dir.split("/")[-1]
	print(folder)
	# out_dir = "Quartet_score_" + folder
	# if not os.path.exists(out_dir):
	# 	os.mkdir(out_dir)
	

	complete_gene_direc = base_dir + "/Sampled_Complete_GTs/GT_Samp"
	complete_astral_dir   = base_dir+"/"+"Complete_ST"
	complete_wqfm_dir     = base_dir+"/Complete_ST_WQFM_SV"
	complete_wqmc_dir     = base_dir+"/"+"Complete_ST_WQMC"
	
	incomplete_pnm_wqmc_dir = base_dir+"/Incomplete_GT_"+doing+"_taxa_removed/"+"Species_tree_decoded_Missing_WQMC"
	incomplete_pnm_wqfm_dir =base_dir+"/Incomplete_GT_"+doing+"_taxa_removed/Species_tree_Missing_WQFM_Final"
	incomplete_pnm_astral_dir = base_dir+"/Incomplete_ST_"+doing+"_taxa_removed"
	
	imputed_st_pnm_wqfm_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_Missing_WQFM_Final"
	imputed_st_pnm_wqmc_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_decoded_Imputed"

	fieldnames = ["Replicate_Number", 'Complete(Astral)', "Complete(WQFM)", "Complete(WQMC)", "Incomplete(Astral)",
	"Incomplete(WQFM)","Incomplete(WQMC)", "Imputed(WQFM)","Imputed(WQMC)"]
	
	rows = []

	for filename in os.listdir(imputed_st_pnm_wqmc_dir):
		row = [None]*len(fieldnames)

		print(filename)
		# in_file = imputed_st_pnm_dir + "/" + filename
		file_sep= filename.split('_')
		idx = file_sep[0]
		row[0] = idx

		GT_file = complete_gene_direc + "/" + idx + "_true_genes_sampled.tree"

		complete_astral_tree = complete_astral_dir + "/" + idx + "_complete_spcs.out.tre"
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', complete_astral_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[1] = split_token_and_send_Qscore(stderr)
		
		complete_wqfm_tree=complete_wqfm_dir+"/Species_tree_missing_wqfm_sv_"+idx
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', complete_wqfm_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[2] = split_token_and_send_Qscore(stderr)

		complete_wqmc_tree = complete_wqmc_dir +"/"+idx+"_whole_sp_tree_wqmc"
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', complete_wqmc_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[3] = split_token_and_send_Qscore(stderr)

		incomplete_pnm_astral_tree = incomplete_pnm_astral_dir +"/"+idx+"_incomplete_spcs.out.tre"
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', incomplete_pnm_astral_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[4] = split_token_and_send_Qscore(stderr)

		incomplete_pnm_wqfm_tree = incomplete_pnm_wqfm_dir + "/Species_tree_missing_wqfm_"+idx
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', incomplete_pnm_wqfm_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[5] = split_token_and_send_Qscore(stderr)

		incomplete_pnm_wqmc_tree = incomplete_pnm_wqmc_dir + "/"+  idx + "_missing_sp_tree_wqmc"
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', incomplete_pnm_wqmc_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[6] = split_token_and_send_Qscore(stderr)
		
		imputed_st_pnm_wqfm_tree = imputed_st_pnm_wqfm_dir + "/Species_tree_missing_wqfm_"+idx
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', imputed_st_pnm_wqfm_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[7] = split_token_and_send_Qscore(stderr)
		

		imputed_st_pnm_wqmc_tree = imputed_st_pnm_wqmc_dir + "/" +  idx +"_imputed_sp_tree_wqmc"
		process = subprocess.Popen(['java','-jar','Codes/Astral/astral.5.6.3.jar','-q', imputed_st_pnm_wqmc_tree, '-i', GT_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=False)
		stdout, stderr = process.communicate()
		row[8] = split_token_and_send_Qscore(stderr)


		rows.append(row)
		
	df = pd.DataFrame(rows,columns = fieldnames)
	output_file = output_dir +"/" +"Quartet_Score_"+doing+"_TR.xlsx"
	df.to_excel(output_file,index=False)
	print("Quartet score generated in",time()-start)

def getFnFpRate_All(base_dir,doing,output_dir,gt_tail="_taxa/"):
	cols = 9
	
	complete_astral_dir   = join_dir(OUTPUT_FOLDER, COMPLETE, ASTRAL)
	complete_wqfm_dir     = join_dir(OUTPUT_FOLDER, COMPLETE, WQFM)
	# complete_wqmc_dir     = base_dir+"/"+"Complete_ST_WQMC"
	
	incomplete_pnm_wqmc_dir = base_dir+"/Smaller_Subset_"+doing+"_Taxa/Incomplete_GT/"+"Species_tree_decoded_Missing_WQMC"
	incomplete_pnm_wqfm_dir =base_dir+"/Smaller_Subset_"+doing+"_Taxa/Incomplete_GT/Species_tree_Missing_WQFM_SV"
	incomplete_pnm_astral_dir = base_dir+"/Incomplete_ST_"+doing+"_taxa_removed"
	

	# imputed_st_pnm_wqfm_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_Missing_WQFM"
	imputed_st_pnm_wqfm_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_Missing_WQFM_SV"
	imputed_st_pnm_wqmc_dir= base_dir + "/"+"GT_Numpy/"+"Imputed_Taxa_GT_Numpy_"+doing+gt_tail +"Species_tree_decoded_Imputed"

	output_file = output_dir +"/" +"FnFpCalc_final_"+doing+"_TR_wqfm.csv"
	csv_file = open(output_file, mode='w')
	fieldnames = ["Replicate_Number", 'Complete(Astral)', "Complete(WQFM)", "Complete(WQMC)", "Incomplete(Astral)",
	"Incomplete(WQFM)","Incomplete(WQMC)", "Imputed(WQFM)","Imputed(WQMC)"]
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()
	# fl = open("FnFpCalc_final_"+doing+"_TR.res",'w+')
	true_sp_tree = base_dir + "/true-species.out.tree"
	for complete_astral_file in os.listdir(complete_astral_dir):
		row = ["--"]*cols
		file_sep_1 = complete_astral_file.split('_')[0]
		row[0] = file_sep_1
		# fl.write("For the replicate: " + file_sep_1+"\n")
		model_tree = complete_astral_dir + "/" + complete_astral_file
		res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',model_tree], encoding='UTF-8')
		
		res = res.replace("(","")
		res = res.replace(")","")
		res = res.replace("\n","")
		res = res.replace(" ","")
		backup = res
		res = res.split(",")
		if(checkEqual2(res) == True):
			row[1] = res[0]
		else:
			print("Different values of res - CA")
			print(res)
			row[1] = backup
			# row.append(res)
		# print(res)
		# fl.write("01) Result for comparing with complete astral " "\n")
		# fl.write(res + "\n")
		
		for complete_wqfm_file in os.listdir(complete_wqfm_dir):
			file_sep_4 = complete_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_4):
				complete_wqfm_tree=complete_wqfm_dir+"/"+complete_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',complete_wqfm_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[2] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[2] = backup
				# print(res)
				# fl.write("03) Result for comparing with complete wqmc " + "\n")
				# fl.write(res + "\n")
		
		for complete_wqmc_file in os.listdir(complete_wqmc_dir):
			file_sep_4 = complete_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_4):
				complete_wqmc_tree=complete_wqmc_dir+"/"+complete_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',complete_wqmc_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[3] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[3] = backup

		for incomplete_pnm_astral_file in os.listdir(incomplete_pnm_astral_dir):
			file_sep_7 = incomplete_pnm_astral_file.split('_')[0]
			if(file_sep_1 == file_sep_7):
				incomplete_pnm_astral_tree=incomplete_pnm_astral_dir+"/"+incomplete_pnm_astral_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_astral_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[4] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[4] = backup
				# #print(res)
				# fl.write("06) Result for comparing with Prune-nam-astral " +  "\n")
				# fl.write(res + "\n")

		for incomplete_pnm_wqfm_file in os.listdir(incomplete_pnm_wqfm_dir):
			file_sep_6 = incomplete_pnm_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_6):
				incomplete_pnm_wqfm_tree=incomplete_pnm_wqfm_dir+"/"+incomplete_pnm_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_wqfm_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[5] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[5] = backup
				#print(res)
				# fl.write("05) Result for comparing with Prune-nam-wqmc " + "\n")
				# fl.write(res + "\n")
		
		for incomplete_pnm_wqmc_file in os.listdir(incomplete_pnm_wqmc_dir):
			file_sep_6 = incomplete_pnm_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_6):
				incomplete_pnm_wqmc_tree=incomplete_pnm_wqmc_dir+"/"+incomplete_pnm_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',incomplete_pnm_wqmc_tree], encoding='UTF-8')
				
				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[6] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[6] = backup

		
		for imputed_st_pnm_wqfm_file in os.listdir(imputed_st_pnm_wqfm_dir):
			file_sep_9 = imputed_st_pnm_wqfm_file.split('_')[-1]
			if(file_sep_1 == file_sep_9):
				print("Imputed_st_pnm",file_sep_9)
				imputed_st_pnm_wqfm_tree=imputed_st_pnm_wqfm_dir+"/"+imputed_st_pnm_wqfm_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',imputed_st_pnm_wqfm_tree], encoding='UTF-8')
				

				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[7] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[7] = backup

		for imputed_st_pnm_wqmc_file in os.listdir(imputed_st_pnm_wqmc_dir):
			file_sep_9 = imputed_st_pnm_wqmc_file.split('_')[0]
			if(file_sep_1 == file_sep_9):
				# print("Imputed_st_pnm",file_sep_9)
				imputed_st_pnm_wqmc_tree=imputed_st_pnm_wqmc_dir+"/"+imputed_st_pnm_wqmc_file
				res = subprocess.check_output(['getFpFn.py','-t',true_sp_tree,'-e',imputed_st_pnm_wqmc_tree], encoding='UTF-8')
				

				res = res.replace("(","")
				res = res.replace(")","")
				res = res.replace("\n","")
				res = res.replace(" ","")
				backup = res
				res = res.split(",")
				if(checkEqual2(res) == True):
					row[8] = res[0]
				else:
					print("Different values of res - CA")
					print(res)
					row[8] = backup


		print(row,len(row))

		writer.writerow({"Replicate_Number": int(row[0]), "Complete(Astral)": row[1], "Complete(WQFM)": row[2], 
			"Complete(WQMC)": row[3], "Incomplete(Astral)": row[4], "Incomplete(WQFM)": row[5],"Incomplete(WQMC)": row[6], 
			"Imputed(WQFM)": row[7], "Imputed(WQMC)": row[8]})
		# fl.write("-------------------------------------------------------------"+"\n\n")

	csv_file.close()




def main():
	if(len(sys.argv) < 3):
		print("Format -> handle.py base_dir <indicator> output_dir")
		exit()
	global base_dir
	base_dir = sys.argv[1]
	doing = sys.argv[2]
	output_dir = sys.argv[3]
	
	# getFnFpRate_V2(base_dir,doing)
	# getFnFpRate_WQFM(base_dir,doing,"_One_Third/")
	getFnFpRate_All(base_dir,doing,output_dir)
	# read_and_display("F",doing,output_dir,"_wqfm",)
	
	# calculate_Quartet_score(doing,output_dir,"_One_Third/")
	# read_and_display("Q",doing)


if __name__== "__main__":
	main()