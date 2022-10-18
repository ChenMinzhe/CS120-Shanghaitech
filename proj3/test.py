import client

n2 = client.FTPClient()
n2.connect("ftp.sjtu.edu.cn",21)

n2.login("anonymous","cc")
n2.nlst()