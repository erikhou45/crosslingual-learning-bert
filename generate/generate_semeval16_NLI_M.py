import os
from collections import defaultdict

from data_utils_semeval16 import *

data_dir='../data/semeval2016/'
dir_path = data_dir+'bert-pair/'

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

file_names = get_files(data_dir)

for file_name in file_names:
    with open(dir_path+file_name[:-4]+"_NLI_M_40.csv","w",encoding="utf-8") as g:
        with open(data_dir+file_name,"r",encoding="utf-8") as f:
            s=f.readline().strip()   
            while s:
                category=[]
                polarity = defaultdict(lambda: [])
                if "<sentence id" in s:
                    left=s.find("id")
                    right=s.find(">")
                    id=s[left+4:right-1]
                    while not "</sentence>" in s:
                        if "<text>" in s:
                            left=s.find("<text>")
                            right=s.find("</text>")
                            text=s[left+6:right]
                        if "<Opinion category" in s:
                            left=s.find("category=")
                            pound=s.find("#")
                            right=s.find("polarity=")
                            target=s[left+10:pound]
                            aspect=s[pound+1:right-2]
                            left=s.find("polarity=")
                            right=s.find("/>")
                            polarity[(target,aspect)].append(quantify_polarity(s[left+10:right-1]))
                        s=f.readline().strip()
                    targets = LAPTOP_TARGETS if "Laptop" in file_name else CELL_TARGETS
                    for target in targets:
                        for aspect in ASPECTS:
                            if (target,aspect) in polarity:
                                for i in range(40):
                                    g.write(id+"\t"+cal_polarity(polarity[(target,aspect)])+"\t"+target+"-"+aspect+"\t"+text+"\n")
                            else:
                                g.write(id+"\t"+"none"+"\t"+target+"-"+aspect+"\t"+text+"\n")
                else:
                    s = f.readline().strip()


