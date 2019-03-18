import platform
import subprocess
import sys
import os

def install():
	if(sys.version_info[0] < 3 and sys.version_info[1] != 6):
		print("Must be using Python 3.6! Exiting installer...")
		sys.exit(1)
	
	print("\nInstalling virtualenv...\n")
	subprocess.call([sys.executable, "-m", "pip", "install", "virtualenv"])
	
	system = str(platform.system())
	release = str(platform.release())
	print("OS info:", system, release)
	
	venv_directory = ""
	token_dir_path = ""
	token_file_path = ""
	
	
	##Set up directories for each OS
	if(system == "Windows"):
		venv_directory = "C:\\Users\\" + str(os.getlogin()) + "\\AppData\\Local\\Programs\\Python\\Python" + str(sys.version_info[0]) + str(sys.version_info[1]) + "\\Lib\\venv\\scripts\\nt\\activate.bat"
		token_dir_path = "bot\\secret"
		token_file_path = token_dir_path + "\\token.txt"
		
	elif(system == "Linux"):
		venv_directory = "/usr/lib/python3" + str(sys.version_info[0]) + str(sys.version_info[1]) + "venv/scripts/common/activate"
		token_dir_path = "bot/secret"
		token_file_path = token_dir_path + "/token.txt"
		
	else:
		##TODO: add Mac support
		print("MacOS not yet supported! Please run install.sh instead.")
		sys.exit(2)
	
	print("Activating venv...")
	os.startfile(venv_directory)
	
	print("Installing dependencies...")
	install_deps()
	
	print("Making directory for Discord token...")
	if(os.path.isdir(token_dir_path)):
		print("Token path already exists! Continuing...")
	else:
		os.mkdir(token_dir_path)
		
	if(os.path.isfile(token_file_path)):
		overwrite_token = input("Token file already exists! Would you like to overwrite it? (y/N): ")
		
		if(overwrite_token.lower() == "y"):
			token = input("Enter your bot's Discord token: ")
			token_file = open(token_file_path, "w+")
			token_file.write(token)
			token_file.close()
			print("Token saved!")
		else:
			print("Using existing token")
	else:
		token = input("Enter your bot's Discord token: ")
		token_file = open(token_file_path, "w+")
		token_file.write(token)
		token_file.close()
		print("Token saved!")
	
	print("Success! The bot has been installed.")
	
	
def install_deps():
	with open("requirements.txt", "r") as reqs:
		deps = reqs.readlines()
	for dep in deps:
		subprocess.call([sys.executable, "-m", "pip", "install", dep])
	reqs.close()
	
install()
