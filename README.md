# ICE_File_Downloader
ICE is a student system for students in XJTLU which is the college I was in. This scripts is mainly for those whose finals or midterms are closed and don't want to download studying materials one by one. 
This script will get all links under your account and download all. 

I didn't use any robust method here, since those who know how to use Python seldom struggle for exams.

## ICEAccess
This is a brief program that is able to pack the *ICE* of XJTLUer and download one or all documents on it.
What you need is to input your personal username and password after running the prohgram and follow the guidlines. 
And then tell your computer "Yes" or "No" to proceed the process. The same questions will be asked twice, if you provide "Yes"
twice, the program will download all documents, whereas, if you only give "Yes" after the first question, the program will just purely
output the documents and links. While no "Yes" is provided, the program only give the indirect link of documents without opening.

### Arguments
As for ICE system, there are always more than one system for each student. Each year one more system will be designed. 
If you want to acquire the documents in previous years, please set `archive=True` and give the specific year you want, for example, 
`Year=2016`. 
```{py}
ICE = ICE(archive=True, Year=2016)
```
When you set `archive=False`, then the argument `Year` will be ignored and only the current year's documents will be acquired.
When you only want the documents of a specific module like "MTH301", please tell the program by input `Course = "MTH301"`
```{py}
ICE = ICE(archive=True, Year=2016, Course="MTH301")
```

### Dependence
The program require a python 3 and a list of pre-installed packages. 
- `requests` for post and obtaining HTML, 
- `re` for regular expression,
- `bs4` for HTML parsing.

### Guidlines
To simplify the usage of users, some brief guidlines are embedded in the scripts.
1. `Your Username: `: Just input your ICE username.
2. `Your `Your Password: `: Input your ICE password.
3. `Success!!`: This means the program succeed in login and successfully get the dashboard.
4. `module's inner documents links list is obtained!!`: Since one document would have two links, inner link and direct link,
the direct link is hidden in the HTML script of inner link, this suggests that the inner link of one document have been acquired.
5. `Process for the File Link?: `: This asks you whether to proceed on parsing inner links to get direct links.
6. `Process to download File?:`: This asks you whether to proceed on parsing the direct links to download files.
