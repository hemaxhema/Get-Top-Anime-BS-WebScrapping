import imp
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os
import urllib.request
from pyfiglet import figlet_format


def returnNameOfAnime(anime):
    name = str(anime.find(
        "td", {"class": "data title clearfix"}).a.text).strip()

    DisAllowedChars = "<>/\\|\"*?:-"
    for char in DisAllowedChars:
        name = name.replace(char, "=")
    # فيه حروف مينفعش تتحط في المسار

    return name


def returnURLOfAnime(anime):
    return "https://myanimelist.net/" + str(anime.find("td", {"class": "data image"}).a["href"]).strip()


def returnWebpOfAnime(anime):
    return str(anime.find("td", {"class": "data image"}).a.img["src"]).strip()


def returnScoreOfAnime(anime):
    # التقييم أحيانا بيكون "-" فهو بيحاول يخليه رقم لو جه فاليو إيرور هيخليه 0
    try:
        returnedValue = int(str(anime.find("td", {"class": "data score"}).find(
            "span", class_="score-label").string).strip())
    except ValueError:
        returnedValue = 0
    return returnedValue


def returnDescripOfAnime(animePage):
    animesoub = BeautifulSoup(animePage, "lxml")
    return str(animesoub.find("p", {"itemprop": "description"}).text).strip().replace("\n", "__")


def returnPhotoOfAnime(animePage):
    animesoub = BeautifulSoup(animePage, "lxml")
    return animesoub.find(id="content").find("div", {"class": "leftside"}).div.a.img["data-src"]


def FuncMkdirOfAllAnimes():
    try:
        os.mkdir(MyDir)
        print("mkdir is done")
    except:
        print("you didn't delete the file on the desktop")


def FuncMkdirOfAnimeandSaveFiles(AnimeName, AnimeURL, AnimeWebp, AnimePhoto, AnimeDescrip, AnimePage, AnimeScore):
    try:
        os.mkdir(MyDir+"\\"+AnimeName)
        SaveWebp(Webp=AnimeWebp, name=AnimeName)
        SavePhoto(Photo=AnimePhoto, name=AnimeName)
        WriteTxt(name=AnimeName, URL=AnimeURL, photo=AnimePhoto,
                 webp=AnimeWebp, score=AnimeScore, descrip=AnimeDescrip)

    except FileExistsError:
        FuncMkdirOfAnimeandSaveFiles(AnimeName=f"{AnimeName} e", AnimeURL=AnimeURL, AnimeScore=AnimeScore,
                                     AnimePhoto=AnimePhoto, AnimeWebp=AnimeWebp, AnimeDescrip=AnimeDescrip, AnimePage=AnimePage)


def SaveWebp(Webp, name):

    urllib.request.urlretrieve(Webp, f"{MyDir}\\{name}\\webp.webp")


def SavePhoto(Photo, name):
    urllib.request.urlretrieve(Photo, f"{MyDir}\\{name}\\photo.jpg")


def WriteTxt(name, score, photo, webp, URL, descrip):
    with open(f"{MyDir}\\{name}\\{name}.txt", "a", encoding="utf-8")as file:
        file.write(
            f"Name is: {name}\nScore is: {score}\nUrl is:{URL}\nPhoto is:{photo}\nWebp is:{webp}\nDesciption is:{descrip}\n")


############### The Beginning of App ###############
ScoreYouWantStopAfter = 8        # عاوز تجيب من تقييم 10 لحد آخر تقييم إيه
MyDir = "D:\\WSAnime"

browser = webdriver.Chrome(ChromeDriverManager().install())
# بيفتح المتصفح

browser.get(
    'https://myanimelist.net/animelist/hemaxhema?status=7&order=4&order2=0')
# بيفتح الموقع

soup = BeautifulSoup(browser.page_source, "lxml")
# بيعمل شوربة من سورس المتصفح اللي اتفتح


AllAnimes = soup.findAll("tbody", class_="list-item")


FuncMkdirOfAllAnimes()

for __anime in AllAnimes:

    print("____________")
    __anime = __anime.find("tr", class_="list-table-data")
    #  just a shortcut

    __animename = returnNameOfAnime(__anime)

    __animeURL = returnURLOfAnime(__anime)

    __animewebp = returnWebpOfAnime(__anime)

    __animeScore = returnScoreOfAnime(__anime)

    if __animeScore < ScoreYouWantStopAfter:
        browser.quit()
        break

    __animePage = requests.get(__animeURL).content

    __animeDescrip = returnDescripOfAnime(__animePage)

    __animePhoto = returnPhotoOfAnime(__animePage)

    FuncMkdirOfAnimeandSaveFiles(AnimeURL=__animeURL,
                                 AnimeName=__animename, AnimeScore=__animeScore, AnimePhoto=__animePhoto, AnimeWebp=__animewebp, AnimeDescrip=__animeDescrip, AnimePage=__animePage)
    print(__animename)
    print(__animeScore)
    print(__animeURL)
    # print(__animePhoto)
    print(__animewebp)

print(figlet_format("Finished"))
############### The End of App ###############
