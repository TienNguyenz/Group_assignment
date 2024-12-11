from driver import *

def perform_login(driver, email, password):
    """Perform login with given email and password."""
    driver.find_element(By.NAME, "email").send_keys(email)
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(2)
    driver.find_element(By.NAME, "form1").click()
    time.sleep(2)
    
def navigate_to_edit_profile(driver):
    perform_login(driver, "admin@mail.com", "Password@123")
    driver.find_element(By.LINK_TEXT, "Administrator").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Edit Profile").click()
    time.sleep(2)

def test_update_information(driver):
    navigate_to_edit_profile(driver)
    name=driver.find_element(By.NAME, "full_name")
    name.clear()
    name.send_keys("Admin")
    time.sleep(1)
    email=driver.find_element(By.NAME, "email")
    email.clear()
    email.send_keys("admin@mail.com")
    time.sleep(1)
    phone= driver.find_element(By.NAME, "phone")
    phone.clear()
    phone.send_keys("0397387337")
    time.sleep(1)
    driver.find_element(By.NAME,"form1").click()
    assert "Profile updated successfully" in driver.page_source

def test_email(driver):
    navigate_to_edit_profile(driver)
    name=driver.find_element(By.NAME, "full_name")
    name.clear()
    name.send_keys("Admin")
    time.sleep(1)
    email=driver.find_element(By.NAME, "email")
    email.clear()
    email.send_keys("admin@mail")
    time.sleep(1)
    phone= driver.find_element(By.NAME, "phone")
    phone.clear()
    phone.send_keys("0397387337")
    time.sleep(1)
    driver.find_element(By.NAME,"form1").click()
    assert "Email address must be valid." in driver.page_source

def test_empty(driver):
    navigate_to_edit_profile(driver)
    name=driver.find_element(By.NAME, "full_name")
    name.clear()
    time.sleep(1)
    email=driver.find_element(By.NAME, "email")
    email.clear()
    time.sleep(1)
    phone= driver.find_element(By.NAME, "phone")
    phone.clear()
    time.sleep(1)
    driver.find_element(By.NAME,"form1").click()
    assert "Name can not be empty." in driver.page_source
    assert "Email Address can not be empty" in driver.page_source

