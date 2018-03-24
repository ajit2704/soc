

# NOTE: PLEASE PUT YOUR CREDENTIALS IN "login" FUNCTION

import unittest
import time
import urllib
import os
import urllib2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class SegAnnTest(unittest.TestCase):

    # The testprofile can be downloaded at
    # https://drive.google.com/open?id=0BxbS0oJuMJTHS1RGeGtvWmp3VzA

    def setUp(self):
        self.driver = webdriver.Firefox()
        # enter the test_profile_path here
        self.test_profile_path = "/home/ajit/SegAnnDB/test_profile.bedGraph.gz"

    def test010_isSegAnnUp(self):
        """
        Test#1
        This test is for checking whether the page is loading or not
        """
        print "Test#1 isSegAnnUp ?"
        driver = self.driver
        driver.get("http://localhost:8080")
        assert "SegAnnDB" in driver.title

    def test020_login(self):
        """
        Test#2
        This test is for testing whether the login functionality is working
        """
        print "Test#2 Persona login test"

        driver = self.driver
        driver.get("http://localhost:8080")
	self.login(driver)	
	"""driver.find_element_by_id('signin').click()
        wait = WebDriverWait(driver, 20)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys('kaleajit27@gmail.com')

        # enter the email of test user
        # click next
        driver.find_element_by_id('identifierNext').click()

	time.sleep(1)
	passwordElem = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
	passwordElem.send_keys('Ajit@1997')
	time.sleep(1)
	Sign_in =  driver.find_element_by_xpath('//*[@id="passwordNext"]/content/span')
        Sign_in.click()"""



        # Call the login method to login the user


        wait = WebDriverWait(driver, 10)
        assert wait.until(
            EC.element_to_be_clickable((By.ID, "signout"))).is_displayed()

    def test030_upload(self):
        """
        This test is for checking if we can successfully upload a profile
        """
        print "Test#3 Profile upload test"
        # login into the app
        driver = self.driver
        driver.get("http://localhost:8080/")
        self.login(driver)

        # make sure that we are logged in
        wait = WebDriverWait(driver, 60)
        assert wait.until(
            EC.element_to_be_clickable((By.ID, "signout"))).is_displayed()

        # go to the upload page
        driver.get("http://localhost:8080/upload")

        # in the upload file field, upload the file
        upload_field = driver.find_element_by_id("id_file")
        test_profile_path = self.test_profile_path
        upload_field.send_keys(test_profile_path)

        # we need to use the submit() button
        # because when we submit forms via click
        # the whole thing has been found to freeze.
        elem = driver.find_element_by_id("submit_button")
        elem.submit()

        assert wait.until(
            EC.presence_of_element_located((By.ID, "success")))

    def test040_annotate(self):
        """
        This test does two things -
        a. Annotate a region
        b. Delete that annotation

        This all happens on the test uploaded profile
        """

        print "Test #4 for testing annotation"

        # we need to give some time for profile processing before we can make
        # annotations
        time.sleep(60)

        driver = self.driver
        driver.get("http://localhost:8080/")
        self.login(driver)

        # make sure that we are logged in
        wait = WebDriverWait(driver, 60)
        assert wait.until(
            EC.element_to_be_clickable((By.ID, "signout"))).is_displayed()

        #
        url_for_annotation = (
            "http://localhost:8080/add_region/ES0004/3/breakpoints/1breakpoint/46469264/67723671/")

        delete_annotation = (
            "http://localhost:8080/delete_region/ES0004/3/breakpoints/0/")

        resp = urllib2.urlopen(url_for_annotation)

        if resp.getcode() != 200:
            print "Fail"
            assert False

        resp.close()

        del_resp = urllib2.urlopen(delete_annotation)
        if del_resp.getcode() != 200:
            assert False

        del_resp.close()

    def test050_delete(self):
        """
        This test is for checking if we are able to delete the uploaded profile
        """
        print "Test#5 Profile Deleting test."
        driver = self.driver
        driver.get("http://localhost:8080/")
        self.login(driver)

        # make sure that we are logged in
        wait = WebDriverWait(driver, 60)
        assert wait.until(
            EC.element_to_be_clickable((By.ID, "signout"))).is_displayed()

        # this is a hack, we need to change it to something more generic.
        # plausible for now
        driver.get("http://localhost:8080/delete_profile/ES0004/")

        # how to assert ?
        if ("deleted" in driver.page_source):
            assert True
        else:
            assert False

    def login(self,driver):
        """
        This method is internal to testing framework
        It is used to login the user.
        Each test requires the user to be logged in already

        Parameters:
            driver - reference to driver being used
        """
       	driver.find_element_by_id('signin').click()
        wait = WebDriverWait(driver, 20)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys('<your_email_id>')

        # enter the email of test user
        # click next
        driver.find_element_by_id('identifierNext').click()

	time.sleep(1)
	passwordElem = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
	passwordElem.send_keys('<your pass>')
	time.sleep(1)
	Sign_in =  driver.find_element_by_xpath('//*[@id="passwordNext"]/content/span')
        Sign_in.click()

	"""driver.find_element_by_id('signin').click()
        wait = WebDriverWait(driver, 60)
	email_field = wait.until(EC.element_to_be_clickable((By.ID, "Email")))

	emailElem = driver.find_element_by_id('Email')
	emailElem.send_keys('seganntest@gmail.com')
	nextButton = driver.find_element_by_id('next')
	nextButton.click()
	time.sleep(1)
	passwordElem = driver.find_element_by_id('Passwd')
	passwordElem.send_keys('segann@test')
	signinButton = driver.find_element_by_id('signIn')
	signinButton.click()"""

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    # now we check for existence of the test file
    # if it does not exist then we create it
    file_name = "test_profile.bedGraph.gz"
    file_path = "./" + file_name
    if os.path.isfile(file_path):
        print "Test file found!"
    else:
        print "Test file does not exists. Downloading."
        download_url = "https://raw.githubusercontent.com/abstatic/SegAnnDB-tests/master/test_profile.bedGraph.gz"
        urllib.urlretrieve(download_url, file_path)
        if os.path.isfile(file_path):
            print "Successfully downloaded the test profile."
        else:
            print "Failed to download the test profile."
    unittest.main()
