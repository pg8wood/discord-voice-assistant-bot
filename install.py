import platform
import subprocess
import sys
import os

def install():
	if(sys.version_info[0] < 3 and sys.version_info[1] != 6):
		print("Must be using Python 3.6!")
		sys.exit()
	
	print("\nInstalling virtualenv...\n")
	subprocess.call([sys.executable, "-m", "pip", "install", "virtualenv"])
	
	system = str(platform.system())
	release = str(platform.release())
	print("OS info:", system, release)
	
	if(system == "Windows"):
		##install the Windows way
	
		venv_directory = "C:\\Users\\" + str(os.getlogin()) + "\\AppData\\Local\\Programs\\Python\\Python" + str(sys.version_info[0]) + str(sys.version_info[1]) + "\\Lib\\venv\\scripts\\nt\\activate.bat"
		
		print("Activating venv...")
		os.startfile(venv_directory)
		
		print("Installing dependencies...")
		installDeps()
		
		print("Making directory for Discord token...")
		token_path = "bot\\secret"
		if(os.path.isdir(token_path)):
			print("Token path already exists! Continuing...")
		else:
			os.mkdir(token_path)
			
		token_path = token_path + "\\token.txt"  ##why use two variables when one will do?
			
		if(os.path.isfile(token_path)):
			overwrite_token = input("Token file already exists! Would you like to overwrite it? (Y/N): ")
			
			if(overwrite_token.lower() == "y"):
				token = input("Enter your bot's Discord token: ")
				token_file = open(token_path, "w+")
				token_file.write(token)
				token_file.close()
				print("Token saved!")
			else:
				print("Using existing token")
		else:
			token = input("Enter your bot's Discord token: ")
			token_file = open(token_path, "w+")
			token_file.write(token)
			token_file.close()
			print("Token saved!")
		
		
	elif(system == "Linux"):
		##install the Linux way
		
		venv_directory = "/usr/lib/python3" + str(sys.version_info[0]) + str(sys.version_info[1]) + "venv/scripts/common/activate"
		
		print("venv_directory:", venv_directory)
		
		print("Activating venv...")
		os.system(venv_directory)
		
		print("Installing dependencies...")
		installDeps()
		
		print("Making directory for Discord token...")
		token_path = "bot/secret"
		if(os.path.isdir(token_path)):
			print("Token path already exists! Continuing...")
		else:
			os.mkdir(token_path)
			
		token_path = token_path + "/token.txt"  ##why use two variables when one will do?
			
		if(os.path.isfile(token_path)):
			overwrite_token = input("Token file already exists! Would you like to overwrite it? (Y/N): ")
			
			if(overwrite_token.lower() == "y"):
				token = input("Enter your bot's Discord token: ")
				token_file = open(token_path, "w+")
				token_file.write(token)
				token_file.close()
				print("Token saved!")
			else:
				print("Using existing token")
		else:
			token = input("Enter your bot's Discord token: ")
			token_file = open(token_path, "w+")
			token_file.write(token)
			token_file.close()
			print("Token saved!")
		
		
	else:  ##Not Windows or Linux, must be a Mac
		##TODO: install the Mac way
		print("MacOS not yet supported! Oops...")
	
	
	print("Success! The bot has been installed.")
	
	
def installDeps():
	with open("requirements.txt", "r") as reqs:
		deps = reqs.readlines()
	for dep in deps:
		subprocess.call([sys.executable, "-m", "pip", "install", dep])
	reqs.close()
	
install()
