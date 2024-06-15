from playwright.sync_api import sync_playwright
import time
import requests
import base64
from PIL import Image
import os
from auto_create_acc import Tk_Locator

coordinates = None
# Function to wait for page title change
def wait_for_title_change(page, current_title):
    while True:
        new_title = page.title()
        if new_title != current_title:
            return new_title
        time.sleep(1)  # Wait for 1 second before checking again
def check_login_container(page):
    try:
        page.wait_for_selector('xpath=//*[@id="loginContainer"]', timeout=5000)
        login_container = page.locator('xpath=//*[@id="loginContainer"]')
        if login_container.is_visible():
            return True
        else:
            return False
    except:
        return False
def check_form_login_container(page):
    try:
        page.wait_for_selector('xpath=//*[@id="loginContainer"]/div/div/div[1]/div[5]', timeout=5000)
        login_container = page.locator('xpath=//*[@id="loginContainer"]/div/div/div[1]/div[5]"]')
        if login_container.is_visible():
            return True
        else:
            return False
    except:
        return False
def dowload_image(url):
        #dowload img
    url = url
    file_path = 'C:\\Users\\PC\\project\\alphabot\\auto_create_acc\\auto_create_tiktok\\test.jpg'
    
    output_directory = 'C:\\Users\\PC\\project\\alphabot\\auto_create_acc\\auto_create_tiktok'
    output_path = os.path.join(output_directory, 'resized_image.jpg')
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Ảnh đã được tải về và lưu tại {file_path}")
        image = Image.open(file_path)
        resized_image = image.resize((340, 212))
        resized_image.save(output_path)
    else:
        print("Không thể tải ảnh. Kiểm tra lại URL.")
def captcha_3D(url):
    #dowload img
    file = 'C:\\Users\\PC\\project\\alphabot\\auto_create_acc\\auto_create_tiktok\\resized_image.jpg'
    dowload_image(url)
    with open(file, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    url = "https://tiktok-captcha-solver2.p.rapidapi.com/tiktok/captcha"

    payload = {
        "cap_type": "3d",
        "image_base64": encoded_string
    }
    headers = {
        "x-rapidapi-key": "34aa46430amsh312cc6e3727740bp1a3e15jsn52273564d271",
        "x-rapidapi-host": "tiktok-captcha-solver2.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    s = response.json()['captcha_solution']
    
    return s
def captcha_whirl(url1,url2):
    url = "https://tiktok-captcha-solver2.p.rapidapi.com/tiktok/captcha"

    payload = {
        "cap_type": "whirl",
        "url1": url1,
        "url2": url2
    }
    headers = {
        "x-rapidapi-key": "34aa46430amsh312cc6e3727740bp1a3e15jsn52273564d271",
        "x-rapidapi-host": "tiktok-captcha-solver2.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    s = response.json()['captcha_solution']
    
    return s
def slove_whilr_and_3D_captcha(page):
    try:
        page.wait_for_selector('//*[@id="captcha_container"]//div//img',timeout=5000)

        # Lấy tất cả các thẻ img có thuộc tính data-test bên trong thẻ "captcha_container"
        img_elements = page.locator('//*[@id="captcha_container"]//div//img')

        # In ra giá trị của thuộc tính 'data-test' cho mỗi thẻ img
        data = []
        for i in range(img_elements.count()):
            img_element = img_elements.nth(i)
            data_test_value = img_element.get_attribute('data-testid')
            data_test_value1 = img_element.get_attribute('src')
            data.append(data_test_value1)
        print(data)
        if data_test_value == None:
            get_coordinates = captcha_3D(data[0])
            #//*[@id="captcha-verify-image"]
            coordinates_x1 = get_coordinates['x1']
            coordinates_y1 = get_coordinates['y1']
            coordinates_x2 = get_coordinates['x2']
            coordinates_y2 = get_coordinates['y2']
            coords = [(coordinates_x1, coordinates_y1), (coordinates_x2, coordinates_y2)]
            print(coords)
            captcha_element = page.query_selector('.captcha_verify_img--wrapper')
            if captcha_element:
                # Lấy vị trí của phần tử captcha
                bounding_box = captcha_element.bounding_box()

                # Tương tác với các tọa độ đã cung cấp
                for coord in coords:
                    x, y = coord
                    print(x,y)
                    page.mouse.move(bounding_box['x'] + x + 20, bounding_box['y'] + y + 20)
                    page.mouse.down()
                    page.mouse.up()

                # Chờ một lúc để xem kết quả
                page.wait_for_timeout(5000)  # Chờ 5 giây

            else:
                print("Không tìm thấy phần tử chứa captcha.")
        else:
            get_coordinates = captcha_whirl(data[0],data[1])
            coordinates = get_coordinates['x1']
            slider = page.locator(".secsdk-captcha-drag-icon")
            slider_box = slider.bounding_box()

            if slider_box:
                # Xác định vị trí bắt đầu và kết thúc của thanh trượt
                start_x = slider_box["x"]
                start_y = slider_box["y"] + slider_box["height"] / 2
                end_x = start_x + coordinates
                end_y = start_y

                # Di chuyển chuột đến vị trí bắt đầu của thanh trượt
                page.mouse.move(start_x, start_y)
                page.mouse.down()
                
                # Di chuyển chuột kéo thanh trượt từ trái sang phải
                page.mouse.move(end_x, end_y, steps=20)
                page.mouse.up()

                # Chờ để xem kết quả
                time.sleep(5)
            
        print(f"Image data-test attribute: {coordinates}")
        return coordinates
    except:
        return False
# Function to perform login
def perform_login(page, email, password):
    time.sleep(2)
    page.click('//*[@id="header-login-button"]')
    time.sleep(2)
    page.click('//*[@id="loginContainer"]/div/div/div[1]/div[2]/div[2]')

    current_title = page.title()
    print("Page title before login:", current_title)
    time.sleep(2)
    page.click('//*[@id="loginContainer"]/div/form/div[1]/a')
    time.sleep(2)
    page.fill('//*[@id="loginContainer"]/div[2]/form/div[1]/input', email)
    time.sleep(2)
    page.fill('//*[@id="loginContainer"]/div[2]/form/div[2]/div/input', password)
    print('Nhập user pwd thành công')
    time.sleep(2)
    page.click('//*[@id="loginContainer"]/div[2]/form/button')
    time.sleep(2)
    slove_whilr_and_3D_captcha(page)
    print('Giải capcha thành công')
    time.sleep(2)
    page.click(".e18d3d942")
    time.sleep(2)
    # Click button upload
    upload_button = page.frame_locator(Tk_Locator.tk_iframe).locator('button:has-text("Select video"):visible')
    with page.expect_file_chooser() as fc_info:
        upload_button.click()
    file_chooser = fc_info.value
    print('Bấm nút upload thành công')
    time.sleep(2)
    file_chooser.set_files("C:\\Users\\PC\\project\\alphabot\\auto_create_acc\\auto_create_tiktok\\2024-05-10 10-22-58.mkv")
    time.sleep(2)
    des = page.frame_locator(Tk_Locator.tk_iframe).locator('div.public-DraftEditor-content')
    des.click()
    time.sleep(2)
    page.keyboard.press("Control+KeyA")
    time.sleep(2)
    page.keyboard.press("Delete")
    page.keyboard.type("Xin chào Việt Nam")
    page.keyboard.press("Enter")
    time.sleep(2)
    page.keyboard.type("#DI DI Nhac Che")
    print('Viết hashtag thành công')
    status_bt = page.frame_locator(Tk_Locator.tk_iframe).locator('//*[@id="root"]/div/div/div/div[2]/div/div[1]/div/div[3]/div/button')
    status_bt.click()
    time.sleep(3)
    favorites_bt = page.frame_locator(Tk_Locator.tk_iframe).locator('button:has-text("Favorites"):visible')
    favorites_bt.click()
    print('Bấm nút favorit thành công')
    time.sleep(3)
    print("OK")

    time.sleep(3)

# Function to perform login
def perform_login_1(page, email, password):
    page.click('.css-6p3qh6-DivLoginOptionContainer > div:nth-child(2) > div:nth-child(2)')
    current_title = page.title()
    print("Page title before login:", current_title)
    time.sleep(2)
    page.click('//*[@id="loginContainer"]/div/form/div[1]/a')
    time.sleep(2)
    page.fill('//*[@id="loginContainer"]/div[2]/form/div[1]/input', email)
    time.sleep(2)
    page.fill('//*[@id="loginContainer"]/div[2]/form/div[2]/div/input', password)
    print('Nhập thành công user pwd')
    time.sleep(2)
    page.click('//*[@id="loginContainer"]/div[2]/form/button')
    time.sleep(2)
    slove_whilr_and_3D_captcha(page)
    print('Giải capcha thành công')
    time.sleep(2)
    page.click(".e18d3d942")
    print('đăng nhập thành công')
    time.sleep(2)
    # Click button upload
    upload_button = page.frame_locator(Tk_Locator.tk_iframe).locator('button:has-text("Select video"):visible')
    with page.expect_file_chooser() as fc_info:
        upload_button.click()
    print('Bấm thành công nút upload')
    file_chooser = fc_info.value
    
    time.sleep(2)
    file_chooser.set_files("C:\\Users\\PC\\project\\alphabot\\auto_create_acc\\auto_create_tiktok\\2024-05-10 10-22-58.mkv")
    time.sleep(2)
    des = page.frame_locator(Tk_Locator.tk_iframe).locator('div.public-DraftEditor-content')
    des.click()
    time.sleep(2)
    page.keyboard.press("Control+KeyA")
    time.sleep(2)
    page.keyboard.press("Delete")
    page.keyboard.type("Xin chào Việt Nam")
    page.keyboard.press("Enter")
    time.sleep(2)
    page.keyboard.type("#DI DI Nhac Che")
    print('Viết hashtag thành công')
    status_bt = page.frame_locator(Tk_Locator.tk_iframe).locator('button:has-text("Edit video"):visible')
    status_bt.click()
    time.sleep(3)
    favorites_bt = page.frame_locator(Tk_Locator.tk_iframe).locator('button:has-text("Favorites"):visible')
    favorites_bt.click()
    print('Bấm nút favorit thành công')
    time.sleep(3)
    
with sync_playwright() as p:
    # Init Page
    # browser = p.firefox.launch(headless=False)
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.clear_cookies()
    page = browser.new_page()
    page.set_viewport_size({'width': 1920, 'height': 1080})
    page.goto("https://www.tiktok.com/explore")
    flag = page.locator('//*[@id="loginContainer"]/div/div/div[1]/div[5]')
    result = check_login_container(page)
    print(result)
    if result == False:
        perform_login(page, "phung.qatest1@gmail.com", "@Conchimnon111")
    else:
        perform_login_1(page, "phung.qatest1@gmail.com", "@Conchimnon111")
    # /html/body/div[6]/div[3]/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]
    result_form = check_form_login_container(page)
    print(result_form)
    time.sleep(30)

    
# def run_tasks_for_account(email, password, page):
#     try:
#         page.goto("https://www.tiktok.com/explore")
#         flag = page.locator('//*[@id="loginContainer"]/div/div/div[1]/div[5]')
#         result = check_login_container(page)
#         print(result)
#         if result == False:
#             perform_login(page, email, password)
#         else:
#             perform_login_1(page, email, password)
        
#         result_form = check_form_login_container(page)
#         print(result_form)
#     except Exception as e:
#         print(f"An error occurred: {e}")
# def clear_cache_and_data(context):
#     # Clear cookies
#     context.clear_cookies()
    
# def main():
#     accounts = [
#         # {"email": "phung.qatest1@gmail.com", "password": "@Conchimnon1111"},
#         # Add more accounts here
#         {"email": "phung.thk12@gmail.com", "password": "@Conchimnon123"},
#         # Add more accounts as needed
#     ]
       
#     with sync_playwright() as p:
#         # Init browser
#         browser = p.chromium.launch(channel='msedge',headless=False, )
#         # browser = p.firefox.launch(headless=False)
#         context = browser.new_context()
#         context.clear_permissions()
#         context.clear_cookies(domain='https://www.tiktok.com/explore')
#         page = context.new_page()
#         for account in accounts:

#             page.set_viewport_size({'width': 1920, 'height': 1080})
            
#             email = account["email"]
#             password = account["password"]
#             run_tasks_for_account(email, password, page)
            
#             page.close()
#             context.close()

#         browser.close()

# if __name__ == "__main__":
#     main()
