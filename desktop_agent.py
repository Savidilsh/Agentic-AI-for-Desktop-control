import pyautogui
import pytesseract
import cv2
import numpy as np
import time

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure pyautogui safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

class SimpleAgent:
    def __init__(self):
        print("Desktop Agent Ready!")
        
    def take_screenshot(self):
        """Take a screenshot and return as numpy array"""
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)
    
    def find_text_on_screen(self, target_text):
        """Find text on screen and return its position"""
        screenshot = self.take_screenshot()
        
        # Get text data with positions
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        
        for i in range(len(data['text'])):
            text = data['text'][i].strip().lower()
            if target_text.lower() in text and len(text) > 0:
                x = data['left'][i] + data['width'][i] // 2
                y = data['top'][i] + data['height'][i] // 2
                return (x, y)
        return None
    
    def open_browser(self, browser_name="chrome"):
        """Open specific browser"""
        print(f"Opening {browser_name}")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite(browser_name)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)
        
    def search_web(self, search_term):
        """Search for something on the web"""
        print(f"Searching for: {search_term}")
        
        # Click on address bar (Ctrl+L works in most browsers)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1)
        
        # Type search term
        pyautogui.typewrite(f"{search_term}")
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)
    
    def open_app(self, app_name):
        """Open an application"""
        print(f"Opening {app_name}")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
    
    def click_text(self, text):
        """Find and click on text"""
        print(f"Looking for '{text}' to click")
        position = self.find_text_on_screen(text)
        if position:
            pyautogui.click(position[0], position[1])
            print(f"Clicked on '{text}'")
            return True
        else:
            print(f"Could not find '{text}' on screen")
            return False
    
    def type_text(self, text):
        """Type text"""
        print(f"Typing: {text}")
        pyautogui.typewrite(text)
    
    def run_goal(self, goal):
        """Execute a goal based on simple keywords"""
        print(f"Analyzing: {goal}")
        goal_lower = goal.lower()
        
        has_open = "open" in goal_lower
        has_search = "search" in goal_lower
        has_browser = any(browser in goal_lower for browser in ["chrome", "edge", "firefox", "browser"])
        
        if has_open and has_browser and has_search:
            browser_name = "chrome"
            if "edge" in goal_lower:
                browser_name = "edge"
            elif "firefox" in goal_lower:
                browser_name = "firefox"
            
            search_term = ""
            if "search for" in goal_lower:
                search_term = goal_lower.split("search for")[1].strip()
            elif "and search" in goal_lower:
                search_term = goal_lower.split("and search")[1].strip().replace("for", "").strip()
            
            print(f"Plan: Open {browser_name}, then search for '{search_term}'")
            self.open_browser(browser_name)
            if search_term:
                time.sleep(2)
                self.search_web(search_term)
            
        elif has_open and has_browser and not has_search:
            browser_name = "chrome"
            if "edge" in goal_lower:
                browser_name = "edge"
            elif "firefox" in goal_lower:
                browser_name = "firefox"
            self.open_browser(browser_name)
            
        elif has_search and not has_open:
            if "for" in goal_lower:
                search_term = goal_lower.split("for")[1].strip()
            else:
                search_term = goal_lower.replace("search", "").strip()
            self.search_web(search_term)
            
        elif has_open and not has_browser:
            app_name = goal_lower.replace("open", "").strip()
            self.open_app(app_name)
            
        elif "click" in goal_lower:
            text = goal_lower.replace("click", "").strip()
            self.click_text(text)
            
        else:
            print(f"Don't know how to: {goal}")

def main():
    """Main interactive loop"""
    agent = SimpleAgent()
    
    print("\nSIMPLE DESKTOP AGENT")
    print("Commands: open calculator, search for cars, click settings")
    print("Type 'quit' to exit\n")
    
    while True:
        goal = input("What should I do? ").strip()
        
        if goal.lower() in ['quit', 'exit', 'stop']:
            print("Goodbye!")
            break
            
        if not goal:
            continue
            
        print(f"Working on: {goal}")
        agent.run_goal(goal)
        print("Done!\n")

if __name__ == "__main__":
    main()