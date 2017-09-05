import requests, re, os
from bs4 import BeautifulSoup

class ICE:
    def __init__(self, archive=True, Year=2016, Course=None):
        if archive:
            self.PHP = "https://ice-archive.xjtlu.edu.cn/"+str(Year)+"/login/index.php"
        else:
            self.PHP = "https://ice.xjtlu.edu.cn/login/index.php"

        self.username = input("Your Username: ")
        print(self.username)
        self.Password = input("Your Password: ")
        print(self.Password)
        self.Course = Course
        self.Year = Year


        self.Sess = requests.session()
        self.Dict = self.getURL()
        with open("Modules of "+self.username+".txt", 'w') as f:
            for i, j in self.Dict.items():
                f.write(i + " | " + j +"\n")
        print("Success!!")

        # The HTMLFile of each module
        self.rawHTMLFile = self.getCourse_raw()
        print("Each module's parsed HTMLFile is obtained!!")

        # The list of documents' inner links and corresponding name
        self.DocLinks = self.getDocInnerUrl()
        print("module's inner documents links list is obtained!!")

        Command1 = input("Process for the File Link?: ")
        # The list of documents name and file links
        if Command1 == "Yes":
            self.DocFileLinks = self.getFile()
            with open("Documents Link"+" of "+ self.username+".txt",'w') as f2:
                for i, j in self.DocFileLinks.items():
                    for a, b in j.items():
                        f2.write(i[0:6] + " | " + a + " | " + b + "\n")
            print("Documents' direct link list is obtained!!")

            Command2 = input("Process to download File?:")
            if Command2 == "Yes":
                # Store the documents to corresponding directory/folder
                print('Now, start downloading files')
                self.docStorage()
        print("Everything is Done!!")

    def getURL(self):
        '''
        post the user data to server obtain the responses
        parse the responded HTML and evaluate the name of module and link

        :return: dictionary of module name and link
        '''

        params = {'username': self.username,
                  'password': self.Password}

        ## post to the server
        print('The userdata has been posted to the server...')
        file = self.Sess.post(self.PHP, data=params)

        print('Parse the HTML file obtained from server...')
        HTML = BeautifulSoup(file.content, 'html.parser')

        FileOfCourse = HTML.find_all(title=re.compile("^[A-X]{3}[0-9]{3}"))
        CourseName = [var.get('title') for var in FileOfCourse]
        CourseUrl = [var.get('href') for var in FileOfCourse]

        return dict(zip(CourseName, CourseUrl))

    def getCourse_raw(self):
        '''
        Firstly select the modules that are of interest from self.Dict
        Store the HTML files of each module into a new dictionary
        :return: A dictionary contain the module names and corresponding HTML files.
        '''
        if not self.Course is None:
            def isMatch(x,y):
                if not re.match(y, x) is None:
                    return True
                else:
                    return False

            tempre = re.compile(self.Course)
            CourseName = [var for var in self.Dict.keys() if isMatch(y=tempre, x=var)]
            CourseUrl = [self.Dict[var] for var in CourseName]
        else:
            CourseName = self.Dict.keys()
            CourseUrl = self.Dict.values()

        return dict(zip(CourseName, [self.getHTMLFile(var) for var in CourseUrl]))

    def getHTMLFile(self, url):
        '''
        Obtain the HTML file of each module w.r.t the url.
        parse the HTML file and return the result
        :param url: the url of any module
        :return: the parsed HTML file
        '''
        HTML1 = self.Sess.get(url)
        HTML2 = BeautifulSoup(HTML1.content, 'html.parser')
        return HTML2

    def getDocInnerUrl(self):
        '''
        find the links of documents from each modules' HTMLFile (self.rawHTMLFile)
        :return: the list of documents' links of each module
        '''

        # return document link list from an HTML file.
        def findLink(file):
            HTML1 = file.find_all('a', onclick=re.compile('.'), href=re.compile('.'))
            return [var.get('href') for var in HTML1]
        moduleName = list(self.rawHTMLFile.keys())
        docList = [findLink(var) for var in list(self.rawHTMLFile.values())]

        return dict(zip(moduleName, docList))

    def getFile(self):
        '''
        parse the documents links and obtain the documents beneath
        :return: The dictionary of file names and links
        '''

        def FileLink(url):
            print("Open",url,"now...")
            HTML1 = self.Sess.get(url)
            HTML2 = BeautifulSoup(HTML1.content, 'html.parser')
            temp = HTML2.find(class_='resourceworkaround').a
            name, link = temp.get_text(), temp.get('href')
            return name, link

        d = {}
        for i, j in self.DocLinks.items():
            print("Process on...", i)
            d[i] = dict([FileLink(var) for var in j])
        return d

    def docStorage(self):
        '''
        As we have obtained the documents links and names
        We then should download the documents to each folders
        :return: None
        '''
        for i, j in self.DocFileLinks.items():
            folder = i[0:6]
            if not os.path.exists(folder):
                os.mkdir(folder)
                os.chdir(folder)
            else:
                os.system('cd ' + folder)
            for a, b in j.items():
                temp = self.Sess.get(b)
                print("Downloading...", a, "in\n", i)
                if a in os.listdir():
                    with open(a, 'wb') as f:
                        f.write(temp.content)
                else:
                    continue
            os.system("cd ..")