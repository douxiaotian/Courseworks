import requests
import bs4
import re
session_requests = requests.session()

def Getcode(url):
    result = session_requests.get(url)
    s = str(result.content, encoding="utf-8")
    return bs4.BeautifulSoup(s, "html.parser")

username = input("Username:")
password = input("Password:")
mylog = {
    "redirectUrl": "http://openjudge.cn/",
    "email": username,
    "password": password,
}
login_url = "http://openjudge.cn/api/auth/login/"

result = session_requests.post(
    login_url,
    data=mylog,
    headers=dict(referer=login_url),
)

homepage_r = re.compile(r"http://openjudge\.cn/user/\d+/")
link_code = Getcode("http://openjudge.cn/")

links = link_code.find("a", attrs={"href":homepage_r})
if links != None:
    homepage_link = links["href"]
ID = homepage_link.replace("http://openjudge.cn/user/","")
ID = ID.strip("/")

def processOnePage (pageUrl):
    pageUrl_code = Getcode(pageUrl)
    next = pageUrl_code.find("a", attrs= {"class": "nextprev", "rel": "next"})
    if next != None:
        nextpage_link = "http://openjudge.cn/user/"+ID+"/"+next["href"]
        return nextpage_link
    else:
        return None

def name_process (origin):
    processed = origin.lstrip("0123456789")
    processed = re.sub("[<>/\\\|:\"\?\*\(\)]", "" ,processed)
    return processed


done_names = []

i = -1
def save_onepage(Url):
    onepage_code = Getcode(Url)
    names_r = re.compile(r"http://wjjc\.openjudge\.cn/2019wjjchw\d/\d{3}/|http://wjjc\.openjudge\.cn/2019hw\d/\d+/")
    solutions_r = re.compile(r"http://wjjc\.openjudge\.cn/2019wjjchw\d/solution/\d{8}/"
                             r"|http://wjjc\.openjudge\.cn/2019hw\d/solution/\d{8}/")
    result_r = re.compile(r"result-\w+")
    question_names = onepage_code.find_all("a", attrs={"href": names_r})
    question_solutions = onepage_code.find_all("a", attrs={"href": solutions_r, "class": result_r})
    if (question_names != []) and (question_solutions != []):
        for x in question_names:
            global i
            i = i + 1 
            if x.text in done_names:  
                pass
            else:
                if question_solutions[i].text == "Accepted":
                    solution_link = question_solutions[i]["href"] 
                    question_name = x.text
                    done_names.append(question_name)  
                    question_name = name_process(question_name)
                    code_code = Getcode(solution_link)
                    code1 = code_code.find("pre", attrs={"class": ""})
                    if code1 != None:
                        code = code1.text 
                        f = open("/Users/rachel/Desktop/" + question_name + ".txt", "w")
                        f.write(code)
                        f.close()
                else:
                    pass


link = homepage_link  
while (True):
    i = -1  
    save_onepage(link)
    if processOnePage(link) == None: 
        break
    else:
        link = processOnePage(link)  
