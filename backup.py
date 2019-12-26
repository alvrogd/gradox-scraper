#!/usr/bin/env python3

# Author: Álvaro Goldar Dieste
# Creation date: 25/12/2019


# Browser simulation
from selenium import webdriver
import selenium.common.exceptions as seleniumExceptions
# Filesystem handling
import os
# Waiting
from time import sleep


def configureDownloads():

    # Default options
    options = webdriver.ChromeOptions()

    # Default download directory is changed to the current one
    prefs = {'download.default_directory' : os.getcwd()}
    options.add_experimental_option('prefs', prefs)
    
    return(options)


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

        # Each found subject is stores, associating its name with its URL
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
                'filePath':os.path.join(destination, \
                    fileElement.get_attribute('textContent'))})
            
        # And each found file is downloaded to the specified destination, if it
        # does not already exist
        for counter, fileElement in enumerate(containedFiles):

            print('\t\t[!] Descargando el fichero: ', \
                fileElement['fileName'], ' (', counter + 1, ' de ', \
                len(containedFiles), ')', sep='', end='\r', flush=True)

            if not os.path.exists(fileElement['filePath']):
                
                currentTry = 0

                # Starts the download
                browser.get(fileElement['fileURL'])

                # When the file is fully retrieved, it gets moved to its
                # corresponding directory
                # It will also skip the file after a 1 min wait
                while not os.path.exists(fileElement['fileName']) and \
                    currentTry < 60 * 5:
                    
                    currentTry += 1
                    
                    # The script waits 200 ms before checking again if the
                    # file is already downloaded
                    sleep(0.2)

                # If the file has been successfully retrieved
                if currentTry < 60 * 5:
                    os.rename(fileElement['fileName'], \
                        fileElement['filePath'])
                    
                else:
                    print('\t\t[!] No se ha podido descargar el fichero:', \
                        fileElement['fileName'])

            # Current output's line is cleared before moving on
            print('\x1b[2K', end='\r', flush=True)

    # The subject may also contain no files
    except seleniumExceptions.NoSuchElementException:
        pass


if __name__ == "__main__":

    # First of all, a profile needs to be created to configure Chrome to
    # download files to the working directory
    profile = configureDownloads()

    # Chrome will be used to access the website
    browser = webdriver.Chrome(options=profile)

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
            subjectDirectory = os.path.join(grade, subjectName)
            createDirectory(subjectDirectory)

            # And its contents are downloaded inside that directory
            retrieveSubjectContents(browser, subjectDirectory, subjectURL)

        print('[!] Finalizada la descarga de los ficheros del curso:', \
            grade, end='\n\n')

    # Before existing, the browser must be closed
    browser.quit()
