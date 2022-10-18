import client

n2 = client.FTPClient()
n2.connect("ftp.sjtu.edu.cn", 21)
n2.login("anonymous","**")
n2.pwd()
n2.cwd("/sites/www.pclinuxos.com/www.pclinuxos.com/wallpapers/")
n2.pwd()
n2.pasv()
n2.nlst()
n2.retr("1920x1080.jpg")