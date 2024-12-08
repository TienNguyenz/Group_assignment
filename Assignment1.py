import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

@pytest.fixture(scope="module")
def setUp():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ tối đa

    service = Service('C:/xampp/htdocs/Phpcode/eCommerceSite-PHP/drivers/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('http://localhost/Phpcode/eCommerceSite-PHP')
    yield driver
    driver.quit()

# Test Case 1: User Registration with valid data
def test_user_registration(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Register").click()  # Nhấp vào liên kết Đăng ký
    time.sleep(2)
    driver.find_element(By.NAME, "cust_name").send_keys("testuser")
    driver.find_element(By.NAME,"cust_cname").send_keys("ABC Company")
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_phone").send_keys("0397387337")
    driver.find_element(By.NAME, "cust_address").send_keys("123 Main St")
    # Chọn quốc gia từ danh sách thả xuống
    country_select = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/form/div/div[2]/div[6]/span/span[1]/span/span[1]")
    country_select.click()  # Mở danh sách thả xuống
    time.sleep(1)
    # Chọn Vietnam
    country_option = country_select.find_element(By.XPATH, "//option[text()='Vietnam']")
    country_option.click()  # Nhấp vào "Vietnam"
    driver.find_element(By.NAME, "cust_city").send_keys("Ho Chi Minh")
    driver.find_element(By.NAME, "cust_state").send_keys("Mien Nam")
    driver.find_element(By.NAME, "cust_zip").send_keys("112233")
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "cust_re_password").send_keys("Password123")
    driver.find_element(By.NAME, "form1").click()  # Nhấp vào nút Đăng ký
    time.sleep(5)
    
    assert "Your registration is completed. Please check your email address to follow the process to confirm your registration." in driver.page_source ,"Email Address Already Exists." # Kiểm tra xem có chuyển đến trang Đăng nhập không
    

# Test Case 2: User Login with valid credentials
def test_user_login(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Login").click()  # Nhấp vào liên kết Đăng nhập
    time.sleep(2)
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "form1").click()  # Nhấp vào nút Đăng nhập
    time.sleep(2)
    assert "Welcome to the Dashboard" in driver.page_source  # Kiểm tra xem có chuyển đến trang Dashboard không

# Test Case 3: User Logout
def test_user_logout(setUp):
    driver = setUp
    test_user_login(driver)  
    driver.find_element(By.LINK_TEXT, "Logout").click()  
    time.sleep(2)

    assert "Customer Login" in driver.page_source 

# Test Case 4: Add Product to Cart
def test_add_product_to_cart(setUp):
    driver = setUp
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/ul/li[2]/a").click()  # Nhấp vào liên kết Sản phẩm
    time.sleep(2)

    driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div/div[1]/div/div[2]/p/a").click()  # Thay thế 'Tên sản phẩm mong muốn' bằng tên thực tế
    time.sleep(2)

    driver.find_element(By.NAME, "form_add_to_cart").click()  # Nhấp vào nút Thêm vào giỏ hàng
    time.sleep(2)

    driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/ul/li[3]/a").click()
    time.sleep(2)

    # Kiểm tra xem thông báo giỏ hàng có hiển thị không
    assert "Amazfit GTS 3 Smart Watch for Android iPhone" in driver.page_source  # Thay thế với thông báo thực tế

# Test Case 5: Search for a product
def test_search_product(setUp):
    driver = setUp
    test_user_login(driver)  # Đăng nhập trước
    search_box = driver.find_element(By.NAME, "search_text")
    search_box.send_keys("Men's Ultra Cotton T-Shirt, Multipack")
    search_box.send_keys(Keys.RETURN)  # Nhấn Enter
    time.sleep(2)
    assert "Men's Ultra Cotton T-Shirt, Multipack" in driver.page_source  # Kiểm tra xem sản phẩm có trong danh sách không

#--------------------------------------------------------------#

# Test Case 6: Check registration page layout
def test_registration_page_layout(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Register").click()  # Nhấp vào liên kết Đăng ký
    time.sleep(2)
    driver.find_element(By.NAME, "cust_name").is_displayed()
    driver.find_element(By.NAME,"cust_cname").is_displayed()
    driver.find_element(By.NAME, "cust_email").is_displayed()
    driver.find_element(By.NAME, "cust_phone").is_displayed()
    driver.find_element(By.NAME, "cust_address").is_displayed()
    # Chọn quốc gia từ danh sách thả xuống
    country_select = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/form/div/div[2]/div[6]/span/span[1]/span/span[1]")
    country_select.click()  # Mở danh sách thả xuống
    time.sleep(1)
    # Chọn Vietnam
    country_option = country_select.find_element(By.XPATH, "//option[text()='Vietnam']")
    country_option.click()  # Nhấp vào "Vietnam"
    driver.find_element(By.NAME, "cust_city").is_displayed()
    driver.find_element(By.NAME, "cust_state").is_displayed()
    driver.find_element(By.NAME, "cust_zip").is_displayed()
    driver.find_element(By.NAME, "cust_password").is_displayed()
    driver.find_element(By.NAME, "cust_re_password").is_displayed()
    time.sleep(5)
    

# Test Case 7: Check navigation menu
def test_navigation_menu(setUp):
    driver = setUp
    menu_items = ["Home", "Men", "Women", "Login","Contact Us","Electronics"]
    
    for item in menu_items:
        time.sleep(2)
        assert driver.find_element(By.LINK_TEXT, item).is_displayed()  # Kiểm tra từng mục trong menu có hiển thị không


def test_page_load_speed(setUp):
    driver = setUp

    # Đo tốc độ tải trang chủ
    start_time = time.time()
    driver.get("http://localhost/Phpcode/eCommerceSite-PHP")
    load_time = time.time() - start_time

    assert load_time < 5  # Trang tải trong dưới 5 giây

def test_product_search(setUp):
    driver = setUp

    # Tìm kiếm sản phẩm
    search_box = driver.find_element(By.NAME, "search_text")
    search_box.send_keys("Laptop")
    search_box.submit()
    time.sleep(2)

    # Kiểm tra kết quả tìm kiếm
    assert "Laptop" in driver.page_source

# Test Case 8: Verify error messages on invalid registration
def test_registration_error_messages(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Register").click()  # Nhấp vào liên kết Đăng ký
    time.sleep(2)

    driver.find_element(By.NAME, "cust_name").send_keys("testuser")
    driver.find_element(By.NAME,"cust_cname").send_keys("ABC Company")
    driver.find_element(By.NAME, "cust_phone").send_keys("0397387337")
    driver.find_element(By.NAME, "cust_address").send_keys("123 Main St")
    # Chọn quốc gia từ danh sách thả xuống
    country_select = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/form/div/div[2]/div[6]/span/span[1]/span/span[1]")
    country_select.click()  # Mở danh sách thả xuống
    time.sleep(1)
    # Chọn Vietnam
    country_option = country_select.find_element(By.XPATH, "//option[text()='Vietnam']")
    country_option.click()  # Nhấp vào "Vietnam"
    driver.find_element(By.NAME, "cust_city").send_keys("Ho Chi Minh")
    driver.find_element(By.NAME, "cust_state").send_keys("Mien Nam")
    driver.find_element(By.NAME, "cust_zip").send_keys("112233")
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "cust_re_password").send_keys("Password123")
    # Dùng JavaScript để bỏ qua kiểm tra email tự động của trình duyệt
    email_input = driver.find_element(By.NAME, "cust_email")
    driver.execute_script("arguments[0].removeAttribute('type')", email_input)
    driver.find_element(By.NAME, "cust_email").send_keys("invalid_email") # Nhập email không hợp lệ
    driver.find_element(By.NAME, "form1").click()  # Nhấp vào nút Đăng ký
    time.sleep(2)

    assert "Email address must be valid." in driver.page_source  # Kiểm tra thông báo lỗi email không hợp lệ

# Test Case 9: Check mobile responsiveness of the site
def test_mobile_responsiveness(setUp):
    driver = setUp
    driver.set_window_size(375, 812)  # Set kích thước cửa sổ để thử
    time.sleep(2)
    # Kiểm tra xem trang web có phản hồi tốt trên thiết bị di động hay không
    assert driver.find_element(By.LINK_TEXT, "Navigation").is_displayed()  # Kiểm tra xem trang chính có hiển thị không
    # Trả về kích thước bình thường
    driver.maximize_window()
    time.sleep(2)

# Test Case 10: Verify product details page layout
def test_product_details_layout(setUp):
    driver = setUp
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/div/ul/li[2]/a").click()  # Nhấp vào liên kết Sản phẩm
    time.sleep(2)

    driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div/div[1]/div/div[2]/p/a").click()  # Thay thế 'Tên sản phẩm mong muốn' bằng tên thực tế
    time.sleep(2)

    # Kiểm tra xem tên sản phẩm có hiển thị không
    assert driver.find_element(By.CLASS_NAME, "p-title").is_displayed()

    # Kiểm tra xem hình ảnh sản phẩm có hiển thị không
    assert driver.find_element(By.CLASS_NAME, "popup").is_displayed()

    # Kiểm tra xem giá sản phẩm có hiển thị không
    assert driver.find_element(By.CLASS_NAME, "p-price").is_displayed()

    # Kiểm tra xem mô tả sản phẩm có hiển thị không
    assert driver.find_element(By.ID, "productTitle").is_displayed()

    assert driver.find_element(By.NAME, "size_id").is_displayed()

    assert driver.find_element(By.NAME, "color_id").is_displayed()
    

    # Kiểm tra xem nút 'Add to Cart' có hiển thị không
    assert driver.find_element(By.NAME, "form_add_to_cart").is_displayed()



#---------------------------------------#

# Test Case 11: Registration with minimum password length
def test_registration_min_password(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Register").click()  # Nhấp vào liên kết Đăng ký
    time.sleep(2)
    driver.find_element(By.NAME, "cust_name").send_keys("testuser")
    driver.find_element(By.NAME,"cust_cname").send_keys("ABC Company")
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_phone").send_keys("0397387337")
    driver.find_element(By.NAME, "cust_address").send_keys("123 Main St")
    # Chọn quốc gia từ danh sách thả xuống
    country_select = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/form/div/div[2]/div[6]/span/span[1]/span/span[1]")
    country_select.click()  # Mở danh sách thả xuống
    time.sleep(1)
    # Chọn Vietnam
    country_option = country_select.find_element(By.XPATH, "//option[text()='Vietnam']")
    country_option.click()  # Nhấp vào "Vietnam"
    driver.find_element(By.NAME, "cust_city").send_keys("Ho Chi Minh")
    driver.find_element(By.NAME, "cust_state").send_keys("Mien Nam")
    driver.find_element(By.NAME, "cust_zip").send_keys("112233")
    driver.find_element(By.NAME, "cust_password").send_keys("123")
    driver.find_element(By.NAME, "cust_re_password").send_keys("123")
    driver.find_element(By.NAME, "form1").click()  # Nhấp vào nút Đăng ký
    time.sleep(5)
    assert "Password too short" in driver.page_source  # Kiểm tra thông báo lỗi
#lỗi

# Test Case 12: Search for a product with special characters
def test_search_special_characters(setUp):
    driver = setUp
    test_user_login(driver)
    search_box = driver.find_element(By.NAME, "search_text")
    search_box.send_keys("@#$%")  # Nhập ký tự đặc biệt
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    assert "No result found" in driver.page_source  # Kiểm tra thông báo không tìm thấy sản phẩm
    print("Test Search Special Characters Passed")

def test_search_empty_query(setUp):
    driver = setUp
    driver.find_element(By.NAME, "search_text").send_keys("")  # Empty search query
    driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/form/button")
    time.sleep(2)
    assert "Please enter a search term" in driver.page_source


def test_register_empty(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Register").click()  # Nhấp vào liên kết Đăng ký
    time.sleep(2)
    driver.find_element(By.NAME, "cust_name").send_keys("")
    driver.find_element(By.NAME,"cust_cname").send_keys("ABC Company")
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_phone").send_keys("0397387337")
    driver.find_element(By.NAME, "cust_address").send_keys("123 Main St")
    # Chọn quốc gia từ danh sách thả xuống
    country_select = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/form/div/div[2]/div[6]/span/span[1]/span/span[1]")
    country_select.click()  # Mở danh sách thả xuống
    time.sleep(1)
    # Chọn Vietnam
    country_option = country_select.find_element(By.XPATH, "//option[text()='Vietnam']")
    country_option.click()  # Nhấp vào "Vietnam"
    driver.find_element(By.NAME, "cust_city").send_keys("Ho Chi Minh")
    driver.find_element(By.NAME, "cust_state").send_keys("Mien Nam")
    driver.find_element(By.NAME, "cust_zip").send_keys("112233")
    driver.find_element(By.NAME, "cust_password").send_keys("")
    driver.find_element(By.NAME, "cust_re_password").send_keys("")
    driver.find_element(By.NAME, "form1").click()  # Nhấp vào nút Đăng ký
    time.sleep(5)
    assert "Customer Name can not be empty."
    assert"Password can not be empty." in driver.page_source  # Kiểm tra thông báo lỗi

# Test Case 14: Registration with maximum username length
def test_registration_max_username(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Register").click()  # Nhấp vào liên kết Đăng ký
    time.sleep(2)
    driver.find_element(By.NAME, "cust_name").send_keys("u" * 30)
    driver.find_element(By.NAME,"cust_cname").send_keys("ABC Company")
    driver.find_element(By.NAME, "cust_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "cust_phone").send_keys("0397387337")
    driver.find_element(By.NAME, "cust_address").send_keys("123 Main St")
    # Chọn quốc gia từ danh sách thả xuống
    country_select = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/form/div/div[2]/div[6]/span/span[1]/span/span[1]")
    country_select.click()  # Mở danh sách thả xuống
    time.sleep(1)
    # Chọn Vietnam
    country_option = country_select.find_element(By.XPATH, "//option[text()='Vietnam']")
    country_option.click()  # Nhấp vào "Vietnam"
    driver.find_element(By.NAME, "cust_city").send_keys("Ho Chi Minh")
    driver.find_element(By.NAME, "cust_state").send_keys("Mien Nam")
    driver.find_element(By.NAME, "cust_zip").send_keys("112233")
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "cust_re_password").send_keys("Password123")
    driver.find_element(By.NAME, "form1").click()  # Nhấp vào nút Đăng ký
    time.sleep(5)

    assert "Your registration is completed. Please check your email address to follow the process to confirm your registration." in driver.page_source  # Kiểm tra thông báo đăng ký thành công

# Test Case 15: Login with incorrect username
def test_login_incorrect_username(setUp):
    driver = setUp
    driver.find_element(By.LINK_TEXT, "Login").click()
    time.sleep(2)
    driver.find_element(By.NAME, "cust_email").send_keys("wronguser@gmail.com")  # Nhập tên người dùng không đúng
    driver.find_element(By.NAME, "cust_password").send_keys("Password123")
    driver.find_element(By.NAME, "form1").click()
    time.sleep(2)

    assert "Email Address does not match." in driver.page_source  # Kiểm tra thông báo lỗi


