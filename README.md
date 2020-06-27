# gradox-scraper

The **Computer Engineering Degree in the University of Santiago de Compostela** has an unofficial **repository that covers each one of the subjects** that are taught: [gradox](https://www.gradox.es).

Its contents have been primarily provided by the students, and they cover:
* Notes.
* Assignments (both exercises and projects).
* Tests.

This Python script takes care of **browsing all the available content in the repository and retrieving it to the local storage**.

## Why was gradox-scraper created?

The repository faces a **huge challenge: if the server that hosts it does not answer, there is no other way to access its files**. It may seem like an uncommon event, and indeed it its, but it tends to have bad timing, as in the weeks that lead up to the final terms.

Furthermore, **the repository's website is not designed in such a way that a single user is able to quickly download all present files**. It is also not possible to perform any kind of search, sorting files using their upload dates, for instance.

Obviously, **no one desires to perform a tiresome task such as manually downloading tens of files** from a website.

## Getting started

### Prerequisites

You will need:

* Any of the following **browsers**: Firefox, Chromium.

* A working installation of **Python 3**.

* The **```selenium``` module**, which is needed to control the browser, and which is not included by default in Python 3.
    * You can add it to your Python installation using: ```pip3 install selenium```.

### Running the script

1. Download the file ```backup.py```

2. Grant it execution permissions; one way would be running: ```chmod u+x ./backup.py```

3. Execute the script: ```./backup.py```

    * The default browser that it will try to use is Chromium. You can also tell it to open Firefox, via an argument: ```./backup.py -d firefox```
    * If you do not need the files from all grades, you can restrict the search so that just the files in a certain grade (4 in total) are downloaded, also via an argument; for instance, you can download files from the third grade using: ```./backup.py -g 3```

4. A window of the selected browser will automatically be opened. Do not close it, as the script requires it to explore the repository!

5. When the script has finished downloading the files, the browser will automatically be closed, therefore finishing the execution of the script.

## Built With

* [Python 3](https://www.python.org/)
* [Selenium Webdriver](https://www.selenium.dev/projects/)

## Authors

* **Álvaro Goldar Dieste** - [alvrogd](https://github.com/alvrogd)
* **D. Coladas** - [DColadas](https://github.com/DColadas)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
