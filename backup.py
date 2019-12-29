#!/usr/bin/env python3

# Author: Álvaro Goldar Dieste
# Creation date: 25/12/2019


# Browser simulation
from selenium import webdriver
import selenium.common.exceptions as seleniumExceptions
# Downloads
import requests
# Filesystem handling
import os


def friendlifyString(string):

    # Accent removal
    import unicodedata
    # Simbol removal
    import re

    # Firstly, all accents are converted into non-accented characters
    # 'Mn' = Nonspacing_Mark
    newString = ''.join(c for c in unicodedata.normalize('NFD', string) if \
        unicodedata.category(c) != 'Mn')

    # Secondly, all other characters that are not accepted are converted
    # into an underscore 
    return(re.sub(r'[^A-Za-z0-9_./\-]', '_', newString))


def openGradox(browser):

    # Accessing to the login page
    browser.get('https://www.gradox.es')

    # Password field is filled
    browser.find_element_by_name('ac').send_keys('apuntes')

    # Login is performed
    browser.find_element_by_name('submit-login').click()


def retrieveSubjects(browser):

    # Result
    subjects = {}

    # Subjects are sorted by grade
    sortingKeys = ['primeiro', 'segundo', 'terceiro', 'cuarto']

    # For each group of subjects
    for key in sortingKeys:

        # The container of the subjects is retrieved
        container = browser.find_element_by_id(key)

        # All the contained subjects are retrieved from that container
        containedSubjects = container.find_elements_by_class_name(\
            'portfolio-link')

        # Each found subject is stored, associating its name with its URL
        foundSubjects = {}

        for subject in containedSubjects:

            # Name can be found inside a H4 tag
            # URL can be found as an attribute of the previously retrieved
            # item
            foundSubjects[subject.find_element_by_css_selector('h4').text] = \
                subject.get_attribute('href')

        # The retrieved subjects are stored in the result, related to their
        # corresponding grade
        subjects[key] = foundSubjects

    return(subjects)


def createDirectory(grade):

    # It will be created if it does not already exist
    if not os.path.exists(grade):
        os.makedirs(grade)


def retrieveSubjectContents(browser, destination, subjectURL):

    # Accessing to the subject's page
    browser.get(subjectURL)

    try:
        # The container of the subject's files is retrieved
        container = browser.find_element_by_class_name('container-fluid')

        # All the contained files are retrieved from that container
        files = container.find_elements_by_css_selector('a')

        containedFiles = []
        
        for fileElement in files:
            
            # Name can be found inside the element
            # URL can be found as an attribute
            containedFiles.append({\
                'fileName':fileElement.get_attribute('textContent'), \
                'fileURL':fileElement.get_attribute('href'), \
                'filePath':friendlifyString(os.path.join(destination, \
                    fileElement.get_attribute('textContent')))})
            
        # And each found file is downloaded to the specified destination, if it
        # does not already exist
        for counter, fileElement in enumerate(containedFiles):

            print('\t\t[!] Descargando el fichero: ', \
                fileElement['fileName'], ' (', counter + 1, ' de ', \
                len(containedFiles), ')', sep='', end='\r', flush=True)

            if not os.path.exists(fileElement['filePath']):
                
                # Starts the download. The server just checks if the following
                # cookie exists to determine if an user is logged in.
                # Therefore, it is included along with the request to be able
                # to perform the download from the 'requests' module
                #
                # It is also important to set 'stream=True' so that the whole
                # file is not directly downloaded into memory, which could
                # cause much trouble when dealing with big files
                data = requests.get(fileElement['fileURL'], cookies={\
                    'usuario':'quieroapuntes2017'}, stream=True)

                # Saves the requested data as the destination file step by
                # step
                with open(fileElement['filePath'], 'wb') as f:
                    # Each chunk will approximately be about 10MB (size goes
                    # in bytes)
                    #
                    # WARNING: switching to a small size may be prone to
                    # cause the following error because of still unknown
                    # reasons:
                    #   ssl.SSLError: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_
                    #   MAC] decryption failed or bad record mac (_ssl.c:2508)
                    for chunk in data.iter_content(chunk_size=1024*1024*10):
                        # Filtering out keep-alive chunks (they have no data)
                        if chunk:
                            f.write(chunk)
               
                # NOTE: the repository lists some files that actually are not
                # avaiable. However, when one of these files is requested, the
                # server replies with the main page and the '200 OK' code, so
                # there is no way to tell those files apart from the ones that
                # actually are available

            # Current output's line is cleared before moving on
            print('\x1b[2K', end='\r', flush=True)

    # The subject may also contain no files
    except seleniumExceptions.NoSuchElementException:
        pass


if __name__ == "__main__":

    # Chrome will be used to access the website
    browser = webdriver.Chrome()

    # Getting access to the repository
    openGradox(browser)

    # All the available subjects are retrieved, classified by grade
    availableSubjects = retrieveSubjects(browser)

    # For each grade's subjects
    for grade, subjects in availableSubjects.items():

        print("[!] Descargando ficheros del curso:", grade)

        # The grade's directory is created
        createDirectory(grade)
        
        for subjectName, subjectURL in subjects.items():

            print('\t[!] Descargando ficheros de la asignatura:', subjectName)

            # A directory is also created for each subject (inside its grade's
            # folder)
            subjectDirectory = friendlifyString(os.path.join(grade, subjectName))
            createDirectory(subjectDirectory)

            # And its contents are downloaded inside that directory
            retrieveSubjectContents(browser, subjectDirectory, subjectURL)

        print('[!] Finalizada la descarga de los ficheros del curso:', \
            grade, end='\n\n')

    # Before existing, the browser must be closed
    browser.quit()
