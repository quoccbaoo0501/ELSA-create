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
        'finish_icon': {'path': 'images/finish_icon.png', 'timeout': 5},
        'share_icon': {'path': 'images/share_icon.png', 'timeout': 5},
        'chrome_icon': {'path': 'images/chrome_icon.png', 'timeout': 5},
        'forward_icon': {'path': 'images/forward_icon.png', 'timeout': 5},
        'copylink_icon': {'path': 'images/copylink_icon.png', 'timeout': 5}
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
    """Split paragraph into sentences, handling both regular text and lyrics format"""
    # First split by newlines to preserve line breaks in lyrics
    lines = paragraph.split('\n')
    sentences = []
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Check if line ends with common sentence endings
        if line.endswith(('.', '!', '?')):
            sentences.append(line)
        else:
            # For lyrics, treat each line as a sentence if it's long enough
            # and doesn't end with conjunction or preposition
            words = line.split()
            if len(words) >= 3 and not words[-1].lower() in {'and', 'or', 'but', 'in', 'on', 'at', 'to', 'the', 'a'}:
                sentences.append(line)
            else:
                # If it's a continuation, append to previous sentence if exists
                if sentences and len(words) > 0:
                    sentences[-1] = sentences[-1] + ' ' + line
                elif len(words) > 0:
                    sentences.append(line)
    
    # Clean up sentences
    cleaned_sentences = []
    for sentence in sentences:
        # Remove extra spaces
        cleaned = ' '.join(sentence.split())
        if cleaned:
            cleaned_sentences.append(cleaned)
    
    return cleaned_sentences

def process_paragraph(icons, paragraph):
    """Process each sentence in the paragraph"""
    # Handle both string and list input
    if isinstance(paragraph, str):
        sentences = split_into_sentences(paragraph)
    else:
        sentences = paragraph  # Already split by LLM
        
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
        time.sleep(3)  # Wait between sentences
    
    return True

def share_and_copy_link(icons):
    """Function to handle sharing and copying the study set link"""
    steps = [
        ('finish_icon', 3, "Clicking finish button..."),
        ('share_icon', 3, "Clicking share icon..."),
        ('chrome_icon', 3, "Clicking chrome icon..."),
        ('forward_icon', 3, "Clicking forward icon..."),
        ('copylink_icon', 3, "Clicking copy link icon...")
    ]

    for step in steps:
        icon_key, delay, message = step
        icon = icons[icon_key]
        
        print(message)
        if not wait_and_click_icon(icon['path'], icon['timeout']):
            print(f"Failed at step: {icon_key}")
            return False
                
        if delay > 0:
            time.sleep(delay)
    return True

def create_new_deck_on_Elsa_in_Noxplayer(study_set_name=None, paragraph=None, progress_callback=None):
    print("Starting automation sequence...")
    
    if progress_callback:
        progress_callback("Initializing...", 5)
    
    # Initialize and verify icons
    icons = initialize_icons()
    if not verify_images(icons):
        return False
        
    if progress_callback:
        progress_callback("Opening Bluestacks...", 15)
    
    # First click Bluestacks
    if not wait_and_click_icon(icons['bluestacks']['path'], icons['bluestacks']['timeout']):
        print("Failed to click Bluestacks")
        return False
    time.sleep(7)
    
    if progress_callback:
        progress_callback("Opening ELSA app...", 30)
    
    # Check if discover is already visible
    discover_visible = False
    for path in icons['discover']['paths']:
        if locate_icon(path, 0.8) is not None:
            discover_visible = True
            print("Discover icon already visible, skipping ELSA launch")
            break
    
    if not discover_visible:
        if not wait_and_click_icon(icons['elsa']['path'], icons['elsa']['timeout']):
            print("Failed to click ELSA")
            return False
        time.sleep(5)
    
    if progress_callback:
        progress_callback("Navigating to study sets...", 45)
    
    # Navigate to study sets
    if not navigate_to_studysets(icons):
        return False
    
    if progress_callback:
        progress_callback("Creating study set...", 60)
    
    # Handle study set name if provided
    if study_set_name:
        if not enter_study_set_name(icons, study_set_name):
            return False
    
    if progress_callback:
        progress_callback("Processing paragraph...", 75)
    
    # Process paragraph if provided
    if paragraph:
        print("Processing paragraph...")
        if not process_paragraph(icons, paragraph):
            print("Failed to process paragraph")
            return False
    
    if progress_callback:
        progress_callback("Finalizing and sharing deck...", 90)
    
    # Share and copy link
    if not share_and_copy_link(icons):
        print("Failed to share and copy link")
        return False
    
    print("Successfully completed all steps!")
    return True

def main():
    # When running directly, use default values
    create_new_deck_on_Elsa_in_Noxplayer()

if __name__ == "__main__":
    main()