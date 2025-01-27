import pyautogui
import time
import os
import re

def click_on_icon(image_path, confidence=None):
    try:
        if not os.path.exists(image_path):
            print(f"Warning: Image not found - {image_path}")
            return False
            
        # Only use confidence if OpenCV is available
        try:
            if confidence:
                res = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            else:
                res = pyautogui.locateCenterOnScreen(image_path)
        except NotImplementedError:
            # Fallback to exact matching if OpenCV is not available
            res = pyautogui.locateCenterOnScreen(image_path)
            
        if res:
            print(f'Clicking on {image_path}')
            pyautogui.moveTo(res)
            pyautogui.click()
            return True
        return False
    except Exception as e:
        print(f"Error clicking on {image_path}: {str(e)}")
        return False

def locate_icon(image_path, confidence=None):
    try:
        if not os.path.exists(image_path):
            print(f"Warning: Image not found - {image_path}")
            return None
            
        # Only use confidence if OpenCV is available
        try:
            if confidence:
                res = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            else:
                res = pyautogui.locateCenterOnScreen(image_path)
        except NotImplementedError:
            # Fallback to exact matching if OpenCV is not available
            res = pyautogui.locateCenterOnScreen(image_path)
            
        if res:
            print(f'Located {image_path}')
        return res
    except Exception as e:
        print(f"Error locating {image_path}: {str(e)}")
        return None

def wait_and_click_icon(image_path, timeout=5, confidence=0.7):
    start_time = time.time()
    while True:
        if locate_icon(image_path, confidence) is None:
            time.sleep(1)
            if (time.time() - start_time > timeout):
                print(f'Timeout: Could not find {image_path} within {timeout} seconds')
                return False
        else:
            return click_on_icon(image_path, confidence)

def initialize_icons():
    return {
        'bluestacks': {'path': 'images/bluestacks_icon.png', 'timeout': 5},
        'elsa': {'path': 'images/elsa_icon.png', 'timeout': 5},
        'discover': {
            'paths': ['images/discover_icon.png', 'images/discover_icon2.png'],
            'timeout': 5
        },
        'studysets': {'path': 'images/studysets_icon.png', 'timeout': 5},
        'addbutton': {'path': 'images/addbutton_icon.png', 'timeout': 5},
        'studysetblank': {'path': 'images/studysetblank.png', 'timeout': 5},
        'categoryblank': {'path': 'images/categoryblank.png', 'timeout': 5},
        'ok_icon': {'path': 'images/ok_icon.png', 'timeout': 5},
        'addphrases_icon': {'path': 'images/addphrases_icon.png', 'timeout': 5},
        'search_icon': {'path': 'images/search_icon.png', 'timeout': 5},
        'check_icon': {'path': 'images/check_icon.png', 'timeout': 5},
        'add_icon': {'path': 'images/add_icon.png', 'timeout': 5},
        'finish_icon': {'path': 'images/finish_icon.png', 'timeout': 5}
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

def try_multiple_icons(icon_paths, timeout, confidence=0.7):
    start_time = time.time()
    while True:
        for path in icon_paths:
            if locate_icon(path, confidence) is not None:
                return wait_and_click_icon(path, timeout, confidence)
        time.sleep(1)
        if (time.time() - start_time > timeout):
            print(f'Timeout: Could not find any of the icons within {timeout} seconds')
            return False

def open_elsa_app(icons):
    steps = [
        ('bluestacks', 2),
        ('elsa', 2)
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
        ('discover', 2),
        ('studysets', 2),
        ('addbutton', 2)
    ]

    for step in steps:
        icon_key, delay = step
        icon = icons[icon_key]
        
        print(f"Executing step: {icon_key}")
        
        if icon_key == 'discover':
            if not try_multiple_icons(icon['paths'], icon['timeout']):
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
    if not wait_and_click_icon(icons['studysetblank']['path'], timeout=5):
        print("Failed to locate study set area")
        return False
        
    time.sleep(1)
    pyautogui.write(study_set_name)
    time.sleep(1)
    
    # Click on category blank area
    if not wait_and_click_icon(icons['categoryblank']['path'], timeout=5):
        print("Failed to click category blank")
        return False
    time.sleep(1)
    
    # Click OK button
    if not wait_and_click_icon(icons['ok_icon']['path'], timeout=5):
        print("Failed to click OK button")
        return False
    time.sleep(1)
    
    return True

def add_phrases(icons):
    steps = [
        ('addphrases_icon', 2),
        ('search_icon', 2)
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

def type_and_add_sentence(icons, sentence):
    """Function to type a sentence and add it to the study set"""
    # Type the sentence
    pyautogui.write(sentence)
    time.sleep(1)
    
    # Click check icon
    if not wait_and_click_icon(icons['check_icon']['path'], timeout=5):
        print("Failed to click check icon")
        return False
    
    # Calculate sleep time based on sentence length
    char_count = len(sentence)
    sleep_time = char_count / 7
    print(f"Waiting {sleep_time:.1f} seconds for sentence with {char_count} characters")
    time.sleep(sleep_time)
    
    # Click add icon
    if not wait_and_click_icon(icons['add_icon']['path'], timeout=5):
        print("Failed to click add icon")
        return False
    time.sleep(1)
    
    return True

def split_into_sentences(paragraph):
    """Split paragraph into sentences using regex"""
    # Split on period followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    # Remove empty sentences and strip whitespace
    return [s.strip() for s in sentences if s.strip()]

def process_paragraph(icons, paragraph):
    """Process each sentence in the paragraph"""
    # Split paragraph into sentences
    sentences = split_into_sentences(paragraph)
    print(f"Processing {len(sentences)} sentences...")
    
    # Process each sentence
    for i, sentence in enumerate(sentences, 1):
        if not add_phrases(icons):
            print("Failed to enter add phrases mode")
            return False
        print(f"Processing sentence {i}/{len(sentences)}: {sentence}")
        if not type_and_add_sentence(icons, sentence):
            print(f"Failed to add sentence: {sentence}")
            return False
        time.sleep(2)  # Wait between sentences
    
    return True

def create_new_deck_on_Elsa_in_Noxplayer(study_set_name=None, paragraph=None):
    print("Starting automation sequence...")
    
    # Initialize and verify icons
    icons = initialize_icons()
    if not verify_images(icons):
        return False
    
    # First click Bluestacks
    if not wait_and_click_icon(icons['bluestacks']['path'], icons['bluestacks']['timeout']):
        print("Failed to click Bluestacks")
        return False
    time.sleep(2)
    
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
        time.sleep(2)
    
    # Navigate to study sets
    if not navigate_to_studysets(icons):
        return False
    
    # Handle study set name if provided
    if study_set_name:
        if not enter_study_set_name(icons, study_set_name):
            return False
    
    # Process paragraph if provided
    if paragraph:
        print("Processing paragraph...")
        if not process_paragraph(icons, paragraph):
            print("Failed to process paragraph")
            return False
    
    # Click finish button
    print("Clicking finish button...")
    if not wait_and_click_icon(icons['finish_icon']['path'], icons['finish_icon']['timeout']):
        print("Failed to click finish button")
        return False
    time.sleep(2)  # Wait for completion
    
    print("Successfully completed all steps!")
    return True

def main():
    # When running directly, use default values
    create_new_deck_on_Elsa_in_Noxplayer()

if __name__ == "__main__":
    main()

