import pyautogui
import time
import os



def click_on_icon(image_path, confidence=0.8):
    try:
        if not os.path.exists(image_path):
            print(f"Warning: Image not found - {image_path}")
            return False
            
        res = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if res:
            print(f'Clicking on {image_path}')
            pyautogui.moveTo(res)
            pyautogui.click()
            return True
        return False
    except Exception as e:
        print(f"Error clicking on {image_path}: {str(e)}")
        return False



def locate_icon(image_path, confidence=0.8):
    try:
        if not os.path.exists(image_path):
            print(f"Warning: Image not found - {image_path}")
            return None
            
        res = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if res:
            print(f'Located {image_path}')
        return res
    except Exception as e:
        print(f"Error locating {image_path}: {str(e)}")
        return None


# Đảm bảo có khoảng thời gian an toàn để di chuyển chuột
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def select_category(category_name):
    try:
        # 1. Locate categoryinside
        category_inside = locate_icon('images/categoryinside.png')
        if category_inside is None:
            print("Could not find categoryinside")
            return False
        
        # 2. Move to categoryinside position and click
        pyautogui.moveTo(category_inside[0], category_inside[1])
        pyautogui.click()
        time.sleep(0.5)
        
        max_attempts = 11
        found = False
        
        for attempt in range(max_attempts):
            print(f"Attempt {attempt + 1} of {max_attempts}")
            
            # 3. Check if Category_name exists
            category_pos = locate_icon(f'images/categoryimages/{category_name}.png', confidence=0.995    )
            
            if category_pos:
                # 4. If Category_name is available
                # Move to and click ok_icon
                ok_icon = locate_icon('images/categoryimages/ok_icon.png')
                if ok_icon:
                    pyautogui.moveTo(ok_icon[0], ok_icon[1])
                    pyautogui.click()
                    found = True
                    break
            
            # 5. If Category_name is not found, scroll up and try again
            if not found and attempt < max_attempts - 1:
                # Move back to categoryinside
                pyautogui.moveTo(category_inside[0], category_inside[1])
                time.sleep(0.2)
                
                # Scroll up
                pyautogui.mouseDown()
                pyautogui.moveRel(0, -40, duration=0.3)  # Changed from -30 to 30 for upward scroll
                pyautogui.mouseUp()
                time.sleep(0.5)  # Increased wait time for scroll
        
        if not found:
            print(f"Could not find category {category_name} after {max_attempts} attempts")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error in select_category: {str(e)}")
        try:
            pyautogui.mouseUp()
        except:
            pass
        return False

# Ví dụ sử dụng:
if __name__ == "__main__":
    # Đợi 3 giây trước khi bắt đầu để người dùng có thời gian chuẩn bị
    print("Chuẩn bị kéo thả trong 3 giây...")
    time.sleep(3)
    select_category('IELTS')
