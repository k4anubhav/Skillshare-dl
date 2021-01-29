from skillshare import Skillshare

cookie = open('cookie.txt').read().replace('\n', '')

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")

dl = Skillshare(cookie=cookie)

url = input("Enter class url:: ")

# bool for downloading subtitle
boolSubtitle = yes_or_no("Do you want to download subtitle")

# bool for downloading resources
boolResources = yes_or_no("Do you want to download resources")

dl.download_course_by_url(url, boolSubtitle, boolResources)