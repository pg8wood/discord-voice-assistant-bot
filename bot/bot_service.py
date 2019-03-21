import platform
import subprocess
import sys
import os
import time

def main():
	
	system = str(platform.system())
	release = str(platform.release())
	print("OS info:", system, release)
	
	if(system == "Windows"):
		venv_directory = "C:\\Users\\" + str(os.getlogin()) + "\\AppData\\Local\\Programs\\Python\\Python" + str(sys.version_info[0]) + str(sys.version_info[1]) + "\\Lib\\venv\\scripts\\nt\\activate.bat"
			
		print("Activating venv...")
		os.startfile(venv_directory)
		
	elif(system == "Linux"):
		venv_directory = "/usr/lib/python" + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "/venv/scripts/common/activate"
		
		print("Activating venv...")
		os.system(venv_directory)
	
	else:  ##Not Windows or Linux, must be a Mac
		##TODO: implement MacOS startup!
		print("MacOS not yet supported! Oops...")
	
	while(True):
		exit_code = subprocess.call([sys.executable, "index.py"])
		
		print("Exit code: ", exit_code)
		
		if(exit_code != 0 and exit_code != 1):
			print("The bot crashed with exit code %d. Restarting...\n" % exit_code)
			time.sleep(1)
		else:
			print("The bot exited gracefully. Bye!\n")
			exit(0)
	
main()
