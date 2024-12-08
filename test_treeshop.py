import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

@pytest.fixture
def driver():
    # Khởi tạo WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()  # Tối đa hóa cửa sổ trình duyệt
    yield driver  # Trả về driver cho các test case
    driver.quit()  # Đóng trình duyệt sau khi hoàn tất

def test_search_valid_product(driver):
    driver.get("https://www.tree-shop.co.uk/")
    search_box = driver.find_element(By.NAME, "s")  # Thay thế 's' bằng tên thực tế của ô tìm kiếm
    search_box.send_keys("Oak Tree")
    search_box.send_keys(Keys.RETURN)
    time.sleep(10)  # Đợi 10 giây để trang tải
    assert "Oak Tree" in driver.page_source, "Sản phẩm 'Oak Tree' không được tìm thấy."

def test_search_non_existing_product(driver):
    driver.get("https://www.tree-shop.co.uk/")
    search_box = driver.find_element(By.NAME, "s")
    search_box.send_keys("Unicorn Tree")
    search_box.send_keys(Keys.RETURN)
    time.sleep(10)  # Đợi 10 giây để trang tải
    assert "No products were found matching your selection" in driver.page_source, "Thông báo không được hiển thị cho sản phẩm không tồn tại."

def test_search_empty_query(driver):
    driver.get("https://www.tree-shop.co.uk/")
    search_box = driver.find_element(By.NAME, "s")
    search_box.send_keys("")  # Để ô tìm kiếm trống
    search_box.send_keys(Keys.RETURN)
    time.sleep(10)  # Đợi 10 giây để trang tải

    # Kiểm tra xem số lượng sản phẩm hiển thị
    result_count_text = driver.find_element(By.CLASS_NAME, "woocommerce-result-count").text
    assert "Showing 1–10 of 204 results" in result_count_text, f"Kết quả tìm kiếm không chính xác: {result_count_text}"

def test_check_search_results_layout(driver):
    driver.get("https://www.tree-shop.co.uk/")
    search_box = driver.find_element(By.NAME, "s")
    search_box.send_keys("Pine Tree")
    search_box.send_keys(Keys.RETURN)

    time.sleep(10)  # Đợi 10 giây để trang tải

    # Kiểm tra tiêu đề sản phẩm
    product_title = driver.find_element(By.CSS_SELECTOR, ".woocommerce-loop-product__title")
    assert product_title.is_displayed(), "Tiêu đề sản phẩm không hiển thị."

    # Kiểm tra giá sản phẩm
    product_price = driver.find_element(By.CSS_SELECTOR, ".woocommerce-Price-amount")
    assert product_price.is_displayed(), "Giá sản phẩm không hiển thị."

def test_add_to_cart(driver):
    driver.get("https://www.tree-shop.co.uk/")
    driver.find_element(By.ID, "menu-item-113").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/ul/li[1]/a").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "button").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[6]/div/button").click()
    time.sleep(10)
    alert_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[1]/div").text
    assert '"ASPEN Populus Tremula- Buy Online" has been added to your basket.' in alert_message

def test_add_multiple_products_to_cart(driver):
    driver.get("https://www.tree-shop.co.uk/")
    

    products_to_add = [
        {"menu_item": "menu-item-113", 
         "product_xpath": "/html/body/div[1]/div/div/main/div[2]/ul/li[1]/a", 
         "button":"/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[6]/div/button",
         "alert_message": '"ASPEN" has been added to your basket.',
         "name":"ASPEN"},
        {"menu_item": "menu-item-113", 
         "product_xpath": "/html/body/div[1]/div/div/main/div[2]/ul/li[2]/a", 
         "button":"/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[4]/div/button",
         "alert_message": '"Amelanchier" has been added to your basket.',
         "name":"Amelanchier"},
        {"menu_item": "menu-item-113", 
         "product_xpath": "/html/body/div[1]/div/div/main/div[2]/ul/li[3]/a", 
         "button":"/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[7]/div/button",
         "alert_message": '"Fig Tree ‘Brown Turkey’" has been added to your basket.',
         "name":"Fig Tree ‘Brown Turkey’"},
    ]
    
    for product in products_to_add:

        driver.find_element(By.ID, product["menu_item"]).click()
        
        driver.find_element(By.XPATH, product["product_xpath"]).click()
        time.sleep(1)
        
        driver.find_element(By.CLASS_NAME, "button").click()
        time.sleep(1)
        
        driver.find_element(By.XPATH, product["button"]).click()
        time.sleep(1)

        alert_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[1]/div").text
        assert product["alert_message"] in alert_message, f"Thông báo không chính xác cho sản phẩm {product['alert_message']}."
        
        driver.back()
        time.sleep(2) 
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu-item-113")))  

    view_cart_button = driver.find_element(By.CLASS_NAME, "basket-icon") 
    view_cart_button.click()  
    time.sleep(10)  

#thêm nhiều sản phẩm có thể tăng giảm số lượng
def test_add_multiple_products_to_cart_with_fixed_quantity(driver):

    driver.get("https://www.tree-shop.co.uk/")
    
    products_to_add = [
        {"menu_item": "menu-item-113", 
         "product_xpath": "/html/body/div[1]/div/div/main/div[2]/ul/li[1]/a", 
         "quantity": "/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[6]/div/div/input", 
         "button":"/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[6]/div/button",
         "alert_message": '"ASPEN" has been added to your basket.',
         "name":"ASPEN"},
        {"menu_item": "menu-item-113", 
         "product_xpath": "/html/body/div[1]/div/div/main/div[2]/ul/li[2]/a", 
         "quantity": "/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[4]/div/div/input", 
         "button":"/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[4]/div/button",
         "alert_message": '"Amelanchier" has been added to your basket.',
         "name":"Amelanchier"},
        {"menu_item": "menu-item-113", 
         "product_xpath": "/html/body/div[1]/div/div/main/div[2]/ul/li[3]/a", 
         "quantity": "/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[7]/div/div/input", 
         "button":"/html/body/div[1]/div/div/main/div[2]/div[2]/div/form/div/table/tbody/tr[1]/td[7]/div/button",
         "alert_message": '"Fig Tree ‘Brown Turkey’" has been added to your basket.',
         "name":"Fig Tree ‘Brown Turkey’"},
    ]
    
    added_products = []

    for product in products_to_add:
        driver.find_element(By.ID, product["menu_item"]).click()
        
        driver.find_element(By.XPATH, product["product_xpath"]).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button"))).click()
        
        random_quantity = random.randint(1, 1000)
        quantity_input = driver.find_element(By.XPATH, product["quantity"])
        quantity_input.clear()
        quantity_input.send_keys(str(random_quantity))


        driver.find_element(By.XPATH, product["button"]).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/main/div[1]/div")))
        
        alert_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[1]/div").text
        assert product["alert_message"] in alert_message, f"Thông báo không chính xác cho sản phẩm {product['alert_message']}."
        
        added_products.append({"name": product["name"], "quantity": random_quantity})
        
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu-item-113")))

    view_cart_button = driver.find_element(By.CLASS_NAME, "basket-icon")
    view_cart_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/main/article/section/div/form/table/tbody/tr[1]/td[5]/div/input")))
    time.sleep(10)

    for index, product in enumerate(added_products, start=1):
        print(f"Checking product {product['name']} in cart...")
        assert product["name"].split(' ')[0] in driver.page_source, f"Sản phẩm {product['name']} không có trong giỏ hàng."

        quantity_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/main/article/section/div/form/table/tbody/tr[{index}]/td[5]/div/input")
        quantity_value = quantity_element.get_attribute("value")
        assert int(quantity_value) == product["quantity"], f"Số lượng cho sản phẩm {product['name']} không chính xác."

#tạo list có 20 sản phẩm và chọn ngẫu nhiên 5 sản phẩm trong 20 và số lượng quanity hay vì nhập thì click random
def  test_add_random_products_to_cart(driver):
    driver.get("https://www.tree-shop.co.uk/")
    
    products_to_add = [
        {"menu_item": "menu-item-113",
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "product": "ASPEN",  
         "button":"increase",
         "alert_message": '"ASPEN" has been added to your basket.',
         "name":"ASPEN"},
        {"menu_item": "menu-item-113", 
         "product": "Amelanchier", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Amelanchier" has been added to your basket.',
         "name":"Amelanchier"},
        {"menu_item": "menu-item-113", 
         "product": "Fig Tree ‘Brown Turkey’", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(3) > a",
         "button":"increase",
         "alert_message": '"Fig Tree ‘Brown Turkey’" has been added to your basket.',
         "name":"Fig Tree ‘Brown Turkey’"},
         {"menu_item": "menu-item-113", 
         "product": "Bird Cherry trees", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"Bird Cherry trees" has been added to your basket.',
         "name":"Bird Cherry trees"},
         {"menu_item": "menu-item-113", 
         "product": "Black Walnut trees",
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a", 
         "button":"increase",
         "alert_message": '"Black Walnut trees" has been added to your basket.',
         "name":"Black Walnut trees"},
         {"menu_item": "menu-item-113", 
         "product": "COAST REDWOOD", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"COAST REDWOOD" has been added to your basket.',
         "name":"COAST REDWOOD"},
         {"menu_item": "menu-item-113", 
         "product": "Common Alder trees", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"Common Alder trees" has been added to your basket.',
         "name":"Common Alder trees"},
         {"menu_item": "menu-item-113", 
         "product": "Common Dogwood", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"Common Dogwood" has been added to your basket.',
         "name":"Common Dogwood"},
         {"menu_item": "menu-item-113", 
         "product": "COMMON OAK", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"COMMON OAK" has been added to your basket.',
         "name":"COMMON OAK"},
         {"menu_item": "menu-item-113", 
         "product": "Common Walnut trees", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"Common Walnut trees" has been added to your basket.',
         "name":"Common Walnut trees"},
         {"menu_item": "menu-item-113", 
         "product": "Cranberry Vaccinium Macrocarpon", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"Cranberry Vaccinium Macrocarpon" has been added to your basket.',
         "name":"Cranberry Vaccinium Macrocarpon"},
         {"menu_item": "menu-item-113", 
         "product": "Downy Birch", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(1) > a",
         "button":"increase",
         "alert_message": '"Downy Birch" has been added to your basket.',
         "name":"Downy Birch"},
         {"menu_item": "menu-item-113", 
         "product": "Amelanchier Canadensis Rainbow Pillar-Snowy Mespilus Tree", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Amelanchier Canadensis Rainbow Pillar-Snowy Mespilus Tree" has been added to your basket.',
         "name":"Amelanchier Canadensis Rainbow Pillar-Snowy Mespilus Tree"},
         {"menu_item": "menu-item-113", 
         "product": "Black Cherry Plum Tree", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Black Cherry Plum Tree" has been added to your basket.',
         "name":"Black Cherry Plum Tree"},
         {"menu_item": "menu-item-113", 
         "product": "Black Mulberry", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Black Mulberry" has been added to your basket.',
         "name":"Black Mulberry"},
         {"menu_item": "menu-item-113", 
         "product": "Blue Atlas Cedar trees",
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a", 
         "button":"increase",
         "alert_message": '"Blue Atlas Cedar trees" has been added to your basket.',
         "name":"Blue Atlas Cedar trees"},
         {"menu_item": "menu-item-113", 
         "product": "Blushing Bride", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Blushing Bride" has been added to your basket.',
         "name":"Blushing Bride"},
         {"menu_item": "menu-item-113", 
         "product": "Brewers weeping Spruce trees evergreen arboretum tree ‘a must have spruce’.", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Brewers weeping Spruce trees evergreen arboretum tree ‘a must have spruce’." has been added to your basket.',
         "name":"Brewers weeping Spruce trees evergreen arboretum tree ‘a must have spruce’."},
         {"menu_item": "menu-item-113", 
         "product": "Cappadocian Maple", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Cappadocian Maple" has been added to your basket.',
         "name":"Cappadocian Maple"},
         {"menu_item": "menu-item-113", 
         "product": "Cedar of Lebanon Tree", 
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a",
         "button":"increase",
         "alert_message": '"Cedar of Lebanon Tree" has been added to your basket.',
         "name":"Cedar of Lebanon Tree"},
         {"menu_item": "menu-item-113", 
         "product": "Cherry Double Blossom",
         "product_s": "#main > div.wrapper.cf > ul > li:nth-child(2) > a", 
         "button":"increase",
         "alert_message": '"Cherry Double Blossom" has been added to your basket.',
         "name":"Cherry Double Blossom"},

    ]
    
    added_products = []
    while len(added_products) < 5:
        random_product = random.choice(products_to_add)  # Chọn một sản phẩm ngẫu nhiên
        
            # Kiểm tra xem sản phẩm đã có trong added_products chưa
        if any(product["name"] == random_product["name"] for product in added_products):
        # Nếu sản phẩm đã có, chọn lại sản phẩm khác
            continue

        driver.find_element(By.ID, random_product["menu_item"]).click()

        driver.find_element(By.CSS_SELECTOR,random_product["product_s"]).click()
        
        driver.find_element(By.LINK_TEXT, random_product["product"]).click()

        # Nếu sản phẩm là "Brewers weeping Spruce trees", nhấn vào Full Description
        if random_product["name"] == "Brewers weeping Spruce trees evergreen arboretum tree ‘a must have spruce’.":
            full_description_button = driver.find_element(By.CLASS_NAME, "accordion-heading")  # Cần điều chỉnh để chọn đúng nút
            full_description_button.click()
            time.sleep(1)  # Đợi một chút cho mô tả tải
        
        target_quantity  = random.randint(1, 100)  
        # Nhấn nút tăng số lượng đến khi đạt số lượng mong muốn
        current_quantity = 1  # Bắt đầu từ 1 vì mặc định
        while current_quantity < target_quantity:
            driver.find_element(By.CLASS_NAME, random_product["button"]).click()
            # Kiểm tra lại số lượng
            quantity_input = driver.find_element(By.XPATH, "//*[contains(@name, 'quantity')]") 
            current_quantity = int(quantity_input.get_attribute("value"))
        driver.find_element(By.NAME, "variation_id").click()
    # Kiểm tra xem sản phẩm có còn hàng không
        try:
            
            alert_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[1]/div").text
            
            # Kiểm tra thông báo xác nhận
            assert random_product["alert_message"] in alert_message, f"Thông báo không chính xác cho sản phẩm {random_product['alert_message']}."
            
            # Thêm sản phẩm vào danh sách đã thêm với số lượng
            added_products.append({
                "name": random_product["name"], 
                "quantity": current_quantity
            })
        except NoSuchElementException:
            print(f"Sản phẩm {random_product['name']} không thể được thêm vào giỏ hàng (có thể đã hết hàng). Bỏ qua.")

            
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu-item-113")))
    for product in added_products:
        print(f"Sản phẩm: {product['name']}, Số lượng: {product['quantity']}")
    view_cart_button = driver.find_element(By.CLASS_NAME, "basket-icon")
    view_cart_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/main/article/section/div/form/table/tbody/tr[1]/td[5]/div/input")))
    time.sleep(10)

    # Kiểm tra từng sản phẩm trong giỏ hàng
    for index, product in enumerate(added_products):
        print(f"Checking product {product['name']} in cart...")
    
    # Kiểm tra sản phẩm có trong giỏ hàng
        assert product["name"].split(' ')[0] in driver.page_source, f"Sản phẩm {product['name']} không có trong giỏ hàng."

    # Xpath để lấy phần tử số lượng dựa trên thứ tự sản phẩm
        quantity_xpath = f"/html/body/div[1]/div/div/main/article/section/div/form/table/tbody/tr[{index + 1}]/td[5]/div/input"
    
    # Lấy giá trị số lượng từ giỏ hàng
        quantity_element = driver.find_element(By.XPATH, quantity_xpath)
        quantity_value = quantity_element.get_attribute("value")

    # So sánh số lượng trong giỏ hàng với số lượng đã thêm
        assert int(quantity_value) == product["quantity"], f"Số lượng cho sản phẩm {product['name']} không chính xác."


    #sau khi kt xong thì check giá có đúng với giá tổng ko và sau khi đổi số lượng và update thì giá có đúng với giá tổng ko

def  test_calculate_cart_total(driver):
    test_update_basket(driver)
    
    product_subtotal_elements = driver.find_elements(By.XPATH, "//td[contains(@class, 'product-subtotal')]")
    
    # Tổng số tiền subtotal sản phẩm
    total_product_subtotal = 0.0    
    for subtotal in product_subtotal_elements:
        
        subtotal_text = subtotal.text  # Điều này sẽ trả về '£X.XX'
        
        
        if subtotal_text.startswith('£'):
            price_value = float(subtotal_text.replace("£", "").replace(",", "").strip())
            total_product_subtotal += price_value
        
    rounded_total_product_subtotal = round(total_product_subtotal, 2) 
    # Lấy giá trị Subtotal tổng cộng từ giỏ hàng
    subtotal_element = driver.find_element(By.CSS_SELECTOR, "#section-1 > div > div.cart-collaterals > div > table > tbody > tr.cart-subtotal > td > span > bdi")
    subtotal_price = float(subtotal_element.text.replace("£", "").replace(",", ""))

    # So sánh tổng product subtotal với Subtotal tổng
    assert rounded_total_product_subtotal == subtotal_price, f"Tổng giá sản phẩm ({rounded_total_product_subtotal}) khác với Subtotal tổng ({subtotal_price})."
    
#update basket
def test_update_basket(driver):
    test_add_random_products_to_cart(driver)
    quantity_inputs = driver.find_elements(By.CLASS_NAME, "input-text.qty.text")
    if quantity_inputs:
        random_index = random.randint(0, len(quantity_inputs) - 1)
        quantity_input = quantity_inputs[random_index]
        quantity_input.click()

        random_quantity = random.randint(1, 1000)

        quantity_input.clear()  
        time.sleep(3)
        quantity_input.send_keys(str(random_quantity)) 
        time.sleep(3)

        update_button = driver.find_element(By.NAME, "update_cart") 
        update_button.click()
        try:
            # Đợi cho thông báo xuất hiện trong vòng 10 giây
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-message"))
            )
            time.sleep(5)
            # Lấy văn bản từ success_message
            success_text = success_message.text.lower()
            assert "basket updated" in success_text, "Cập nhật giỏ hàng không thành công!"
        except Exception as e:
            print(f"Không tìm thấy thông báo thành công. Lỗi: {str(e)}")
    else:
        print("Không tìm thấy ô nhập số lượng sản phẩm.")

#checkout
def test_checkout(driver):
    test_calculate_cart_total(driver)
    time.sleep(5)
    checkout_button = driver.find_element(By.XPATH, "//a[contains(text(),'Proceed to checkout')]")
    checkout_button.click()
    time.sleep(3)
    first_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_first_name")))
    first_name_input.send_keys("John")
    time.sleep(3)
    last_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_last_name")))
    last_name_input.send_keys("Doe")
    time.sleep(3)
    company_input = driver.find_element(By.ID, "billing_company")
    company_input.send_keys("Doe Inc.")
    time.sleep(3)
    country_dropdown = driver.find_element(By.ID, "billing_country")
    country_options = country_dropdown.find_elements(By.TAG_NAME, "option")
    random_country = random.choice(country_options)
    random_country.click()
    time.sleep(3)
    street_address_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_address_1")))
    street_address_input.send_keys("123 Elm Street")
    time.sleep(3)
    town_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_city")))
    town_input.send_keys("Springfield")
    time.sleep(3)
    county_dropdown = driver.find_element(By.ID, "billing_state") 
    county_options = county_dropdown.find_elements(By.TAG_NAME, "option")
    if county_options:
        random_county = random.choice(county_options)
        random_county.click()
    else:
        print("Không có tùy chọn hạt nào.")
    time.sleep(3)

    postcode_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_postcode")))
    postcode_input.send_keys("62701")
    time.sleep(3)

    phone_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_phone")))
    phone_input.send_keys("1234367890")
    time.sleep(3)

    email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "billing_email")))
    email_input.send_keys("john.doe@example.com")
    time.sleep(3)
    delivery_first_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "shipping_first_name")))
    delivery_first_name_input.send_keys("Jane")
    time.sleep(3)
    delivery_last_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "shipping_last_name")))
    delivery_last_name_input.send_keys("Doe")
    time.sleep(3)
    delivery_street_address_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "shipping_address_1")))
    delivery_street_address_input.send_keys("436 Oak Avenue")
    time.sleep(3)
    delivery_town_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "shipping_city")))
    delivery_town_input.send_keys("Lincoln")
    time.sleep(3)
    delivery_county_input = driver.find_element(By.ID, "shipping_state")
    delivery_county_input.send_keys("NE")
    time.sleep(3)
    delivery_postcode_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "shipping_postcode")))
    delivery_postcode_input.send_keys("SW1A 1AA")  
    time.sleep(3)
    order_notes_input = driver.find_element(By.ID, "order_comments")
    order_notes_input.send_keys("Please leave the package at the front door.")
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, "blockUI")))
    time.sleep(3)
    terms_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "terms")))
    driver.execute_script("arguments[0].click();", terms_checkbox)  
    newsletter_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/article/section/div/form[2]/div[2]/div/div/p/label/input")))
    driver.execute_script("arguments[0].click();", newsletter_checkbox)  
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, "blockUI")))
    time.sleep(3)
    place_order_button = driver.find_element(By.ID, "place_order")
    driver.execute_script("arguments[0].scrollIntoView();", place_order_button)
    time.sleep(3)
    driver.execute_script("arguments[0].click();", place_order_button)

    time.sleep(30)

#lấy hết tên tất cả sản phẩm trong shop
def test_get_all_product(driver):
    driver.get("https://www.tree-shop.co.uk/shop/")
    
    # Đợi một thời gian để trang tải
    time.sleep(2)

    # Lấy tổng số danh mục sản phẩm
    category_count = len(driver.find_elements(By.CSS_SELECTOR, "#main > div.wrapper.cf > ul > li > a"))
    total_product_count = 0  
    all_product_names = []  # Danh sách lưu tất cả tên sản phẩm
    for i in range(1, category_count + 1):  # Lặp qua tất cả các danh mục
        try:
            # Tạo selector cho từng sản phẩm
            category_link = driver.find_element(By.CSS_SELECTOR, f"#main > div.wrapper.cf > ul > li:nth-child({i}) > a")
            category_link.click()
            
            # Đợi một thời gian để trang sản phẩm tải
            time.sleep(2)

            # Lặp qua các trang sản phẩm trong danh mục
            while True:
                # Lấy tất cả tên sản phẩm trên trang này
                product_elements = driver.find_elements(By.CLASS_NAME, "woocommerce-loop-product__title")
                product_names = [product.text for product in product_elements]
                all_product_names.extend(product_names)
                
                # Cập nhật tổng số sản phẩm
                total_product_count += len(product_names)

                # In ra tên sản phẩm
                print(f"Products in category {i}:")
                for name in product_names:
                    print(name)

                # Kiểm tra nếu có nút "Next" để tiếp tục
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")  # Selector cho nút "Next"
                    if next_button.is_enabled():  # Kiểm tra nếu nút có thể nhấp được
                        next_button.click()
                        # Đợi một thời gian để trang sản phẩm tải
                        time.sleep(2)
                    else:
                        print("No more pages. Returning to shop.")
                        break
                except Exception:
                    break
            
            # Quay lại trang shop
            driver.get("https://www.tree-shop.co.uk/shop/")
            time.sleep(2)  # Chờ trang tải lại
        except Exception as e:
            print(f"Error occurred for category {i}: {e}")
    # In ra tổng số sản phẩm đã liệt kê
    print(f"Total products listed: {total_product_count}")

    return all_product_names  # Trả về danh sách tên sản phẩm

#random add to cart
def test_add_random_product_to_cart(driver):
    """Hàm thêm sản phẩm ngẫu nhiên vào giỏ hàng."""
    all_product_names = test_get_all_product(driver)  # Gọi hàm để lấy tên sản phẩm
    if all_product_names:
        # Chọn một sản phẩm ngẫu nhiên
        random_product_name = random.choice(all_product_names)
        print(f"Selected random product: {random_product_name}")

        # Tìm sản phẩm ngẫu nhiên và thêm vào giỏ hàng
        search_box = driver.find_element(By.NAME, "s")  # Tìm ô tìm kiếm
        search_box.clear()
        search_box.send_keys(random_product_name)  # Nhập tên sản phẩm vào ô tìm kiếm
        search_box.submit()  # Gửi tìm kiếm

        time.sleep(2)  # Đợi kết quả tìm kiếm tải

        # Nhấp vào sản phẩm đầu tiên trong kết quả tìm kiếm
        product_link = driver.find_element(By.CSS_SELECTOR, ".woocommerce-loop-product__title")  # Selector cho sản phẩm
        product_link.click()  # Nhấp vào sản phẩm
        
        time.sleep(2)  # Đợi trang sản phẩm tải

        # Thêm vào giỏ hàng
        add_to_cart_button = driver.find_element(By.NAME, "variation_id")  # Selector cho nút thêm vào giỏ hàng
        add_to_cart_button.click()
        time.sleep(7)  # Đợi thông báo tải

        # Kiểm tra thông báo thành công
        success_message = driver.find_element(By.CLASS_NAME, "woocommerce-message")  # Selector cho thông báo thành công
        assert success_message.is_displayed()  # Kiểm tra nếu thông báo hiển thị
        print(f"Added {random_product_name} to cart.")
    else:
        print("No products found.")

#contack us
def test_contact_us(driver):
    driver.get("https://www.tree-shop.co.uk/contact/")
    
    full_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "your-name")))
    full_name_input.clear()
    full_name_input.send_keys("John Doe")
    
    email_input = driver.find_element(By.NAME, "your-email")
    email_input.clear()
    email_input.send_keys("johndoe@example.com")
    
    message_input = driver.find_element(By.NAME, "your-comments")
    message_input.clear()
    message_input.send_keys("I would like to know more about the different types of Oak Trees you offer.")

    address_line_1 = driver.find_element(By.NAME, "your-address1")
    address_line_1.clear()
    address_line_1.send_keys("123 Forest Lane")
    
    address_line_2 = driver.find_element(By.NAME, "your-address2")
    address_line_2.clear()
    address_line_2.send_keys("Apt 101")
    
    town_input = driver.find_element(By.NAME, "your-town")
    town_input.clear()
    town_input.send_keys("Woodville")
    
    postcode_input = driver.find_element(By.NAME, "your-postcode")
    postcode_input.clear()
    postcode_input.send_keys("WV12 4TR")

    country_select = driver.find_element(By.NAME, "your-country")
    country_select.send_keys("United Kingdom")
    
    fax_number = driver.find_element(By.NAME, "your-fax")
    fax_number.clear()
    fax_number.send_keys("123456789")
    
    phone_number = driver.find_element(By.NAME, "your-tel")
    phone_number.clear()
    phone_number.send_keys("0123456789")
    

    rating_select = Select(driver.find_element(By.NAME, "your-rating"))
    rating_select.select_by_value("Excellent")  

    checkboxes = [
    {"label": "Land Owner", "xpath": "/html/body/div[1]/div/div/main/article/section[3]/div[2]/div/form/div[3]/div[2]/p/span/span/span[1]/input"},
    {"label": "Student", "xpath": "/html/body/div[1]/div/div/main/article/section[3]/div[2]/div/form/div[3]/div[2]/p/span/span/span[2]/input"},
    {"label": "Professional", "xpath": "/html/body/div[1]/div/div/main/article/section[3]/div[2]/div/form/div[3]/div[2]/p/span/span/span[3]/input"},
    {"label": "Planning New Woodland", "xpath": "/html/body/div[1]/div/div/main/article/section[3]/div[2]/div/form/div[3]/div[2]/p/span/span/span[4]/input"},
    {"label": "Managing Existing Woodland", "xpath": "/html/body/div[1]/div/div/main/article/section[3]/div[2]/div/form/div[3]/div[2]/p/span/span/span[5]/input"},
    ]


    random_checkbox = random.choice(checkboxes)


    checkbox_element = driver.find_element(By.XPATH, random_checkbox["xpath"])
    checkbox_element.click()

    
    brochure_checkbox = driver.find_element(By.NAME, "your-brochure")
    if not brochure_checkbox.is_selected():
        brochure_checkbox.click()

    seasonal_bulletins_checkbox = driver.find_element(By.NAME, "your-bulletins")
    if not seasonal_bulletins_checkbox.is_selected():
        seasonal_bulletins_checkbox.click()

    data_consent_checkbox = driver.find_element(By.NAME, "your-acceptance")
    if not data_consent_checkbox.is_selected():
        data_consent_checkbox.click()


    submit_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/article/section[3]/div[2]/div/form/div[6]/div[2]/p/a")
    submit_button.click()
    
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockOverlay")))

    try:
        success_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Thank you for your message')]"))
        )
        assert "Thank you for your message. It has been sent." in success_message.text, "Thông báo gửi không thành công."
    except TimeoutException:
        print("Lỗi: Không tìm thấy thông báo thành công.")
        driver.save_screenshot("screenshot.png")  # Lưu ảnh chụp màn hình để xem trạng thái

#check toàn bộ link liệu có chết ko
def test_check_all_links(driver):
    driver.get("https://www.tree-shop.co.uk/")
    

    links = driver.find_elements(By.TAG_NAME, "a")
    

    valid_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    for url in valid_links:
        try:
            driver.get(url)
            time.sleep(2) 
            assert "404" not in driver.title, f"Liên kết không hợp lệ: {url}"
            print(f"Liên kết hợp lệ: {url}")
        except Exception as e:
            print(f"Lỗi khi truy cập liên kết {url}: {e}")
        finally:
            driver.get("https://www.tree-shop.co.uk/")  # Quay lại trang chính

#check footer link liệu có chết ko
def test_check_footer_links(driver):
    driver.get("https://www.tree-shop.co.uk/")
    

    footer = driver.find_element(By.TAG_NAME, "footer")
    

    links = footer.find_elements(By.TAG_NAME, "a")

    valid_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    for url in valid_links:
        try:
            driver.get(url)
            time.sleep(2)  
            assert "404" not in driver.title, f"Liên kết không hợp lệ: {url}"
            print(f"Liên kết hợp lệ: {url}")
        except Exception as e:
            print(f"Lỗi khi truy cập liên kết {url}: {e}")
        finally:
            driver.get("https://www.tree-shop.co.uk/")  


