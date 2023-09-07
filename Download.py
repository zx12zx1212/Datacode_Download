def Download(start, account, password, end=None, hostname=None, port=None):
    if end == None:
        end = start
    import paramiko
    import os

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=account, password=password, port=port)
    sftp = ssh.open_sftp()

    for i in range(start, end + 1):
        print('\033[92m' + ("Download " + str(i)).center(100, '=') + '\033[0m')
        data_Path = "/home/datacode/Files/" + str(i)
        stdin, stdout, stderr = ssh.exec_command("cd " + data_Path + ";ls")
        studen_list = stdout.read().decode('utf-8').split('\n')

        local_path = "./" + str(i)
        if os.path.exists(local_path) == False:
            os.makedirs(local_path)

        for studen in studen_list:
            stdin, stdout, stderr = ssh.exec_command("cd " + data_Path + "/" + studen + "/Result" + ";ls")
            syuden_data = stdout.read().decode('utf-8').split('\n')
            if set(['Pass.txt']) < set(syuden_data):
                print(studen)
                sftp.get(data_Path + "/" + studen + "/" + studen + ".zip", local_path + "/" + studen + ".zip")

    sftp.close()
    ssh.close()

account = input("請輸入帳號密碼(用空格隔開):").split(" ")
start_number = input("請輸入題號(用空格隔開，如為連續題號請直接輸入開始及結束題號):").split(" ")
if len(start_number) == 2:
    Download(start=int(start_number[0]), end=int(start_number[1]), account=account[0], password=account[1])
else:
    Download(start=int(start_number[0]), account=account[0], password=account[1])
