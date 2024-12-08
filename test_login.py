import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# User Authentication
# TC1: Valid Login
# TC2: Invalid Login
# TC3: Empty Username/Password
# TC4: Logout Functionality

def test_valid_login(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    assert "inventory.html" in driver.current_url

def test_invalid_login(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
    assert "Username and password do not match" in error_message

@pytest.mark.parametrize("username, password, expected", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("problem_user", "secret_sauce", True),
    ("performance_glitch_user", "secret_sauce", True)
])
def test_login_multiple_users(driver, username, password, expected):
    driver.get("https://www.saucedemo.com/")
    
    # Nhập tên đăng nhập
    driver.find_element(By.ID, "user-name").send_keys(username)
    time.sleep(2)
    # Nhập mật khẩu
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(2)
    # Nhấn nút đăng nhập
    driver.find_element(By.ID, "login-button").click()

    time.sleep(2)
    
    if expected:
        # Xác minh đăng nhập thành công
        assert "inventory.html" in driver.current_url, f"Đăng nhập thất bại với tài khoản {username}"
    else:
        # Xác minh đăng nhập thất bại
        error_message = driver.find_element("css selector", ".error-message-container").text
        assert "Epic sadface" in error_message, f"Đăng nhập không thất bại với tài khoản {username}"

def test_empty_username(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
    assert "Username is required" in error_message

def test_empty_password(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
    assert "Password is required" in error_message

def test_logout_functionality(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)  # Optional wait

    driver.find_element(By.ID, "react-burger-menu-btn").click()  # Open the menu
    time.sleep(2)
    driver.find_element(By.ID, "logout_sidebar_link").click()  # Click on logout
    time.sleep(3)  # Optional wait
    assert "https://www.saucedemo.com/" in driver.current_url

def test_add_item_to_cart(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)  # Optional wait
    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    add_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    random_index = random.randint(0, len(products) - 1)
    product_name = products[random_index].text
    add_buttons[random_index].click()  # Thêm sản phẩm ngẫu nhiên vào giỏ
    time.sleep(2)
    
    return product_name

def test_remove_item_from_cart(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)  # Optional wait

    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    add_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    random_index = random.randint(0, len(products) - 1)
    product_name = products[random_index].text
    add_buttons[random_index].click()  # Thêm sản phẩm ngẫu nhiên vào giỏ
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)

    cart_items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    assert any(product_name in item.text for item in cart_items), "Sản phẩm không có trong giỏ hàng."

    driver.find_element(By.XPATH, "//button[text()='Remove']").click()
    time.sleep(2)
    cart_items_after_removal = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    assert not any(product_name in item.text for item in cart_items_after_removal), "Sản phẩm vẫn còn trong giỏ hàng."
    print(f"Sản phẩm {product_name} đã được xóa khỏi giỏ hàng.")

def test_view_cart_functionality(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)  # Optional wait

    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    add_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    random_index = random.randint(0, len(products) - 1)
    product_name = products[random_index].text
    add_buttons[random_index].click()  # Thêm sản phẩm ngẫu nhiên vào giỏ
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)

    cart_items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    cart_item_names = [item.text for item in cart_items]
    
    print("Các sản phẩm trong giỏ hàng:", cart_item_names)
    return cart_item_names

def test_checkout_process(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)  # Optional wait
    driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
    time.sleep(2) 
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2) 
    driver.find_element(By.XPATH, "//button[text()='Checkout']").click()
    time.sleep(2)  # Optional wait
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    time.sleep(2)
    assert "Checkout: Overview" in driver.page_source
    driver.find_element(By.ID, "finish").click()
    time.sleep(2)
    assert "Thank you for your order!" in driver.page_source, "Không tìm thấy thông báo xác nhận đơn hàng"
    print("Checkout thành công.")

def test_checkout_without_info(driver):
    driver.get("https://www.saucedemo.com/")
    
    # Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Thêm sản phẩm vào giỏ hàng và mở giỏ hàng
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(2)
    driver.find_element(By.ID, "shopping_cart_container").click()
    time.sleep(2)
    # Nhấn nút thanh toán và thử tiếp tục mà không nhập thông tin
    driver.find_element(By.ID, "checkout").click()
    time.sleep(2)
    driver.find_element(By.ID, "continue").click()
    time.sleep(2)
    # Kiểm tra thông báo lỗi
    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
    assert "Error" in error_message, "Không hiển thị thông báo lỗi khi không nhập thông tin"

def test_sort_items_by_nameaz(driver):
    driver.get("https://www.saucedemo.com/")
    
    # Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Sắp xếp sản phẩm theo giá từ thấp đến cao
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='az']").click()
    time.sleep(2)
    product_names_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    product_names = [element.text for element in product_names_elements]
    time.sleep(2)
    # Kiểm tra xem danh sách đã được sắp xếp đúng thứ tự A-Z
    sorted_names = sorted(product_names)
    assert product_names == sorted_names, "Sản phẩm không được sắp xếp theo thứ tự A-Z"

def test_sort_items_by_nameza(driver):
    driver.get("https://www.saucedemo.com/")
    
    # Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Sắp xếp sản phẩm theo giá từ thấp đến cao
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='za']").click()
    time.sleep(2)
    product_names_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    product_names = [element.text for element in product_names_elements]
    time.sleep(2)
    # Kiểm tra xem danh sách đã được sắp xếp đúng thứ tự A-Z
    sorted_names = sorted(product_names,reverse=True)
    assert product_names == sorted_names, "Sản phẩm không được sắp xếp theo thứ tự Z-A"

def test_sort_items_by_pricelh(driver):
    driver.get("https://www.saucedemo.com/")
    
    # Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Sắp xếp sản phẩm theo giá từ thấp đến cao
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='lohi']").click()
    time.sleep(2)
    # Xác minh sản phẩm đầu tiên có giá thấp nhất
    first_item_price = driver.find_element(By.CSS_SELECTOR, ".inventory_item_price").text
    assert first_item_price == "$7.99", "Sản phẩm không được sắp xếp đúng giá từ thấp đến cao"

def test_sort_items_by_pricehl(driver):
    driver.get("https://www.saucedemo.com/")
    
    # Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Sắp xếp sản phẩm theo giá từ thấp đến cao
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    sort_dropdown.find_element(By.CSS_SELECTOR, "option[value='hilo']").click()
    time.sleep(2)
    # Xác minh sản phẩm đầu tiên có giá thấp nhất
    first_item_price = driver.find_element(By.CSS_SELECTOR, ".inventory_item_price").text
    assert first_item_price == "$49.99", "Sản phẩm không được sắp xếp đúng giá từ cao đến thấp"

def test_session_timeout(driver):
    driver.get("https://www.saucedemo.com/")

    # Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    # Chờ thời gian timeout (giả sử 5 phút)
    time.sleep(300)  # 300 giây = 5 phút

    # Cố gắng thêm sản phẩm vào giỏ hàng sau khi phiên hết hạn
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    # Kiểm tra tiêu đề trang
    assert "Swag Labs" in driver.title, "Người dùng không bị chuyển hướng về trang đăng nhập sau khi phiên hết hạn"

def test_access_control_without_login(driver):
    # Truy cập trang giỏ hàng mà không đăng nhập
    driver.get("https://www.saucedemo.com/cart.html")

    error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-container")
    assert error_message.is_displayed(), "Thông báo lỗi không hiển thị, người dùng có thể đã đăng nhập thành công"

def test_https_encryption(driver):
    driver.get("https://www.saucedemo.com/")

    # Kiểm tra nếu trang sử dụng HTTPS
    assert "https" in driver.current_url, "Trang không sử dụng HTTPS để bảo mật truyền tải"

def test_sql_injection_attempt(driver):
    driver.get("https://www.saucedemo.com/")

    # Thử SQL injection trong trường Username và Password
    sql_injection_string = "' OR 1=1 --"
    
    driver.find_element(By.ID, "user-name").send_keys(sql_injection_string)
    driver.find_element(By.ID, "password").send_keys(sql_injection_string)
    time.sleep(2)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Kiểm tra xem trang có xử lý input không hợp lệ hay không
    error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-container")
    assert error_message.is_displayed(), "SQL Injection không bị phát hiện"

    # Kiểm tra nội dung thông báo lỗi đăng nhập
    assert "Username and password do not match" in error_message.text, "SQL Injection có thể đã thành công"
