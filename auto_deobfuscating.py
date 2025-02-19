import re
import subprocess, sys
import argparse

parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('-f', type=str,
                    help='Enter obfuscated file path')
args = parser.parse_args()

#read a file
with open(args.f,"r") as file:
    text = file.read()

result=''
#find the text with the format "( -f )" or "( -F )"
x = re.findall(r'\([^\)]\{[0-9]+\}[^\)]+[\-f|\-F][^\)]+\)' , text)
y = re.findall(r"\('[^']+'\+[^)]+\)|\(\"[^\"]+\"\+[^)]+\)", text)

#create a process to run powershell command line
def runPowershellScript(encoded_command):
    decoded_string = subprocess.run(["powershell.exe",encoded_command],capture_output=True, text=True)
    return decoded_string.stdout.strip() # strip for no new line at the end 

for match in x:
    clean_script = runPowershellScript(match)
    text = text.replace(match,clean_script)

for match in y:
    clean_script = runPowershellScript(match)
    text = text.replace(match,clean_script)

#replace ` with ""
text = text.replace('`', '')
print(text)