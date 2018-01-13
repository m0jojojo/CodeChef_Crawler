import requests 
from bs4 import BeautifulSoup
countv=0





base_url="https://www.codechef.com/"
def crawl_user(username):
    url = "https://www.codechef.com/users/" + str(username) 
    source_code = requests.get(url)
    plain_text = source_code.content
    soup =BeautifulSoup(plain_text,'html.parser')
    section = soup.find(class_='rating-data-section problems-solved')
    links = section.find_all('a')
    for link in links:
        problem_status_url=base_url+ link['href']
        name = link.string
        writeSubmission(problem_status_url,name)
        







def writeSubmission(url,name):
    url = url + "?sort_by=All&sorting_order=asc&language=All&status=15&Submit=GO" #show only Correct Submissions!
    source_code = requests.get(url)
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text,'html.parser')
    id_list = soup.find('td',width='60')
    try:
        submission_id=id_list.string  #taking the latest correct submission's ID
    except:
        print("Skipping:-",name)
        return    
    lang_list = soup.find_all('td', width='70')
    try:
        lang = lang_list[0].string       #taking the language of latest correct submission
    except:
        lang = lang_list.string     
    submission_url = base_url + "viewplaintext/" + str(submission_id) 
    code = fetchSubmission(submission_url)
    print("Downloading->",name)
    ext=".txt"
    if lang.startswith("C++"):
        ext=".cpp"
    if lang.startswith("PYTH"):
        ext=".py"
    if lang=="C":
        ext=".c"
    if lang=="JAVA":
        ext=".java"            
    name = name + ext
    f = open(name,'w')  
    f.write(code)
    f.close()
        



def fetchSubmission(url):
    source_code = requests.get(url)
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text,'html.parser')
    problem_code = soup.get_text()
    global countv
    countv+=1
    return (problem_code) 
    
    



username = input("Enter the username: ")    
crawl_user(str(username))
print("Total:-",countv," solutions downloaded")