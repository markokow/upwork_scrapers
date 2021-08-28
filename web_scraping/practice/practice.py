from bs4 import BeautifulSoup

with open('home.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    courses = soup.find_all('div', class_ = 'card')
    for course in courses:
        course_temp = course.h5.text
        price_temp = course.a.text.split()[-1]
        print(course_temp, 'costs', price_temp)