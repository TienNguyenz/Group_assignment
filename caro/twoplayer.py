import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller

# Tự động cài đặt chrome driver
chromedriver_autoinstaller.install()

# Khởi tạo trình duyệt (Chrome)
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://playtictactoe.org/")
    driver.find_element(By.CLASS_NAME,"swap").click()
    yield driver
    driver.quit()


# Hàm để chờ đợi và nhấp vào một ô
def click_square(driver, xpath):
    try:
        # Chờ phần tử xuất hiện và có thể nhấp vào
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath))  # Kiểm tra phần tử có thể nhấp vào
        )
        element.click()
    except Exception as e:
        print(f"Lỗi khi nhấp vào phần tử: {e}")

# Test case 1: Hòa
def test_draw(driver):
    # Di chuyển các quân cờ theo cách hòa
    click_square(driver, '/html/body/div[3]/div[1]/div[1]')  
    click_square(driver, '/html/body/div[3]/div[1]/div[2]') 
    click_square(driver, '/html/body/div[3]/div[1]/div[3]')  
    
    click_square(driver, '/html/body/div[3]/div[1]/div[5]')  
    click_square(driver, '/html/body/div[3]/div[1]/div[4]')  
    click_square(driver, '/html/body/div[3]/div[1]/div[6]')  

    click_square(driver, '/html/body/div[3]/div[1]/div[8]')  
    click_square(driver, '/html/body/div[3]/div[1]/div[7]')  
    click_square(driver, '/html/body/div[3]/div[1]/div[9]')  
    time.sleep(2)
    # Chờ thêm một chút để chắc chắn trạng thái đã được cập nhật
    result = driver.find_element(By.XPATH,"/html/body/div[4]/p[2]/span").text
    assert result == "1", f"Expected '1', but got {result}"

# Test case 2: X thắng
def test_win_x(driver):
    # Di chuyển các quân cờ theo cách X thắng
    click_square(driver, '/html/body/div[3]/div[1]/div[1]')  # X đi đầu (Hàng 1, Ô 1)
    click_square(driver, '/html/body/div[3]/div[1]/div[2]')  # O đi (Hàng 1, Ô 2)
    click_square(driver, '/html/body/div[3]/div[1]/div[4]')  # X đi (Hàng 2, Ô 1)
    click_square(driver, '/html/body/div[3]/div[1]/div[5]')  # O đi (Hàng 2, Ô 2)
    click_square(driver, '/html/body/div[3]/div[1]/div[7]')  # X đi (Hàng 3, Ô 1)
    time.sleep(2)
    result = driver.find_element(By.XPATH,"/html/body/div[4]/p[1]/span[4]").text
    assert result == "1", f"Expected '1', but got {result}"

def test_win_0(driver):
    # Di chuyển các quân cờ theo cách X thắng
    click_square(driver, '/html/body/div[3]/div[1]/div[1]')  # X đi đầu (Hàng 1, Ô 1)
    click_square(driver, '/html/body/div[3]/div[1]/div[2]')  # O đi (Hàng 1, Ô 2)
    click_square(driver, '/html/body/div[3]/div[1]/div[4]')  # X đi (Hàng 2, Ô 1)
    click_square(driver, '/html/body/div[3]/div[1]/div[5]')  # O đi (Hàng 2, Ô 2)
    click_square(driver, '/html/body/div[3]/div[1]/div[9]')  # X đi (Hàng 3, Ô 1)
    click_square(driver, '/html/body/div[3]/div[1]/div[8]') # O đi (Hàng 3, Ô 3)
    time.sleep(2)
    result = driver.find_element(By.XPATH,"/html/body/div[4]/p[3]/span[4]").text
    assert result == "1", f"Expected '1', but got {result}"