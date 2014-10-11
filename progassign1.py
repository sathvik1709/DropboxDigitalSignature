#CSE 6331 Cloud Computing Summer 2014
#Programming assignment 1
#Sathvik Shivaprakash
#1000989203

import os, time
import dropbox
import gnupg

gpg = gnupg.GPG(gnupghome=r'C:\gnupg-home-dir-sathvik')
client = dropbox.client.DropboxClient("Jtjy6HbrtdkAAAAAAAAAhy7pQp7cNY1IBcUNUil9s19T2sDdnOxsLkdP6QLiAxmh")

#####################
#generating keys
student_params = {
		'Key-Type': 'DSA',
		'Key-Length': 1024,
		'Passphrase':'studentsecret',
		'Subkey-Type': 'ELG-E',
        'Subkey-Length': 2048,
        'Name-Real':'student',
        'Name-Email':'student@uta.edu',
        'Expire-Date': 0,
    }
stu_inp = gpg.gen_key_input(**student_params)
#Generating student key with above parameters
studentkey = gpg.gen_key(stu_inp)
#studentkey = studentkey.fingerprint
#print studentkey

professor_params = {
		'Key-Type': 'DSA',
		'Key-Length': 1024,
		'Passphrase':'professorsecret',
		'Subkey-Type': 'ELG-E',
        'Subkey-Length': 2048,
        'Name-Real':'professor',
        'Name-Email':'professor@uta.edu',
        'Expire-Date': 0,
	}
prof_inp = gpg.gen_key_input(**professor_params)
#Generating professor key with the specified parameters
professorkey = gpg.gen_key(prof_inp)
#professorkey = professorkey.fingerprint
#print professorkey
print "Keys generated."
print "Monitoring started.."
#####################

# This is the path of the directory to be monitored
folder_to_monitor = r'C:\Users\sathvikwin8\Desktop\Cloud1'
# getting the list of directories already present in the path specified
before = dict ([(f, None) for f in os.listdir (folder_to_monitor)])

while 1:
    time.sleep (10)
	#check for changes every 10 seconds
    after = dict ([(f, None) for f in os.listdir (folder_to_monitor)])
    file_added = [f for f in after if not f in before]
    file_removed = [f for f in before if not f in after]
    
    if file_added: #If a new file is added
        localboxpath = folder_to_monitor + "\\"+",".join(file_added)
		#open the file
        file = open(localboxpath)
		# encrypt the file and sign, encryption using professor key and sign using student key
        encrypted = gpg.encrypt_file(file, professorkey,sign=studentkey, passphrase='studentsecret',output=r'C:\Users\sathvikwin8\Desktop\Cloud\enc.txt')
		#open the encrypted file
        f = open(r"C:\Users\sathvikwin8\Desktop\Cloud\enc.txt", 'rb')
		#put the signed file onto dropbox
        response = client.put_file('/encrypted.txt', f)
        file.close()
        f.close()
        print "File added."
    if file_removed: #if removed
		#download the file from dropbox
		fd, metadata = client.get_file_and_metadata('/encrypted.txt')
		# open the file in write mode
		out = open(r"C:\Users\sathvikwin8\Desktop\Cloud\decrt.txt", 'wb')
		out.write(fd.read())
		out.close()
		# again open the file (at this point it contains only encrypted data)
		out1 = open(r'C:\Users\sathvikwin8\Desktop\Cloud\decrt.txt', 'r').read()
		# verify the file with passphrase and decrypt it
		decrypted = gpg.decrypt(out1, passphrase='professorsecret', output=r'C:\Users\sathvikwin8\Desktop\Cloud\decrt.txt')
		#out.write(fd.read())
		print "File verified and decrypted."
    before = after

"""
References:
https://www.dropbox.com/developers/core/start/python
https://pythonhosted.org/python-gnupg/
https://gist.github.com/vsajip/922267
http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
http://en.wikipedia.org/wiki/Digital_signature

"""

  
  
 
  
  
