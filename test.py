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

def wait_and_click_icon(image_path, timeout=20, confidence=0.8):
    start_time = time.time()
    while True:
        if locate_icon(image_path, confidence) is None:
            time.sleep(2)  # Reduced sleep time for faster response
            if (time.time() - start_time > timeout):
                print(f'Timeout: Could not find {image_path} within {timeout} seconds')
                return False
        else:
            return click_on_icon(image_path, confidence)

def initialize_icons():
    return {
        'nox': {'path': 'images/nox_icon_on_taskbar.png', 'timeout': 20},
        'elsa': {'path': 'images/elsa_icon.png', 'timeout': 50},
        'discover': {
            'paths': ['images/discover_icon.png', 'images/discover_icon2.png'],
            'timeout': 20
        },
        'studysets': {'path': 'images/studysets_icon.png', 'timeout': 20},
        'addbutton': {'path': 'images/addbutton_icon.png', 'timeout': 20},
        'studysetblank': {'path': 'images/studysetblank.png', 'timeout': 10}
    }

def verify_images(icons):
    for name, icon in icons.items():
        if 'paths' in icon:  # Handle multiple paths case
            for path in icon['paths']:
                if not os.path.exists(path):
                    print(f"Error: Required image missing - {path}")
                    return False
        else:  # Single path case
            if not os.path.exists(icon['path']):
                print(f"Error: Required image missing - {icon['path']}")
                return False
    return True

def try_multiple_icons(icon_paths, timeout, confidence):
    start_time = time.time()
    while True:
        for path in icon_paths:
            if locate_icon(path, confidence) is not None:
                return wait_and_click_icon(path, timeout, confidence)
        time.sleep(2)
        if (time.time() - start_time > timeout):
            print(f'Timeout: Could not find any of the icons within {timeout} seconds')
            return False

def open_elsa_app(icons):
    steps = [
        ('nox', 4),  # (icon_key, delay_after_click)
        ('elsa', 3)
    ]
    
    for step in steps:
        icon_key, delay = step
        icon = icons[icon_key]
        
        print(f"Executing step: {icon_key}")
        
        if not wait_and_click_icon(icon['path'], icon['timeout']):
            print(f"Failed at step: {icon_key}")
            return False
                
        if delay > 0:
            time.sleep(delay)
    return True

def navigate_to_studysets(icons):
    steps = [
        ('discover', 3),
        ('studysets', 3),
        ('addbutton', 3)
    ]

    for step in steps:
        icon_key, delay = step
        icon = icons[icon_key]
        
        print(f"Executing step: {icon_key}")
        
        if icon_key == 'discover':
            if not try_multiple_icons(icon['paths'], icon['timeout'], 0.8):
                print(f"Failed at step: {icon_key}")
                return False
        else:
            if not wait_and_click_icon(icon['path'], icon['timeout']):
                print(f"Failed at step: {icon_key}")
                return False
                
        if delay > 0:
            time.sleep(delay)
    return True

def enter_study_set_name(icons, study_set_name):
    if not wait_and_click_icon(icons['studysetblank']['path'], timeout=10):
        print("Failed to locate study set area")
        return False
        
    time.sleep(2)
    pyautogui.write(study_set_name)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    return True

def create_new_deck_on_Elsa_in_Noxplayer(study_set_name=None):
    print("Starting automation sequence...")
    
    # Initialize and verify icons
    icons = initialize_icons()
    if not verify_images(icons):
        return False
    
    # First click Nox
    if not wait_and_click_icon(icons['nox']['path'], icons['nox']['timeout']):
        print("Failed to click Nox")
        return False
    time.sleep(4)
    
    # Check if discover is already visible before clicking ELSA
    discover_visible = False
    for path in icons['discover']['paths']:
        if locate_icon(path, 0.8) is not None:
            discover_visible = True
            print("Discover icon already visible, skipping ELSA launch")
            break
    
    # Only click ELSA if discover is not visible
    if not discover_visible:
        if not wait_and_click_icon(icons['elsa']['path'], icons['elsa']['timeout']):
            print("Failed to click ELSA")
            return False
        time.sleep(3)
    
    # Navigate to study sets
    if not navigate_to_studysets(icons):
        return False
    
    # Handle study set name if provided
    if study_set_name:
        if not enter_study_set_name(icons, study_set_name):
            return False
    
    print("Successfully completed all steps!")
    return True

def main():
    # When running directly, use default values
    create_new_deck_on_Elsa_in_Noxplayer()

if __name__ == "__main__":
    main()

