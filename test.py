from ClientUpdate import DVUpload

DV = DVUpload("jose176","Yuca23*12","https://revmnt.sld.cu/index.php/rmnt/")
DV.login()
repo = DV.make_repo()
print(repo)