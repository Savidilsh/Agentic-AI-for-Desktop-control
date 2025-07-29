import pyautogui
import pytesseract
import numpy as np
import time
import json
import re

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure pyautogui safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class KeyboardAgent:
    def __init__(self):
        print("Keyboard-Based Desktop Agent Ready!")
    
    def take_screenshot(self):
        """Take a screenshot and return as numpy array"""
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)
    
    def get_screen_text_simple(self):
        """Get simple screen text for context"""
        screenshot = self.take_screenshot()
        text = pytesseract.image_to_string(screenshot)
        # Return first 200 chars
        return text.strip()[:200]
    
    def open_calculator(self):
        """Open Windows calculator"""
        print("Opening calculator...")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite('calc')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)
        print("Calculator opened!")
    
    def calculator_operation_keyboard(self, expression):
        """Use keyboard to input calculator operations"""
        print(f"Typing calculation: {expression}")
        
        # Clear calculator first
        pyautogui.press('escape')
        time.sleep(0.5)
        
        # Type the expression directly
        for char in expression:
            pyautogui.press(char)
            time.sleep(0.3)
        
        # Press equals
        pyautogui.press('enter')
        time.sleep(0.5)
        print(f"Calculation '{expression}' completed!")
    
    def open_browser_and_search(self, search_term):
        """Open browser and search"""
        print(f"Opening browser and searching for: {search_term}")
        
        # Open browser
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite('chrome')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)
        
        # Focus address bar and search
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1)
        pyautogui.typewrite(search_term)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        print(f"Search for '{search_term}' completed!")
    
    def open_app(self, app_name):
        """Open any application"""
        print(f"Opening {app_name}...")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        print(f"{app_name} opened!")
    
    def call_ollama(self, prompt):
        """Call Ollama with simplified response parsing"""
        try:
            import ollama
            print("Using Ollama LLM...")
            
            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'user', 'content': prompt}
            ])
            content = response['message']['content']
            
            # Extract JSON more reliably
            if '[' in content and ']' in content:
                start = content.find('[')
                end = content.rfind(']') + 1
                json_str = content[start:end]
                try:
                    return json.loads(json_str)
                except:
                    pass
            
            return None
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return None
    
    def execute_action(self, action_type, parameters):
        """Execute actions using keyboard-based approach"""
        print(f"Executing: {action_type}")
        
        if action_type == "open_calculator":
            self.open_calculator()
            
        elif action_type == "calculator_operation":
            expression = parameters.get("expression", "")
            self.calculator_operation_keyboard(expression)
            
        elif action_type == "open_browser_search":
            search_term = parameters.get("search_term", "")
            self.open_browser_and_search(search_term)
            
        elif action_type == "open_app":
            app_name = parameters.get("app_name", "")
            self.open_app(app_name)
            
        elif action_type == "type_text":
            text = parameters.get("text", "")
            if text:
                pyautogui.typewrite(text)
            
        elif action_type == "press_key":
            key = parameters.get("key", "")
            if key:
                if "+" in key:
                    keys = key.split("+")
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(key)
        
        elif action_type == "scroll_down":
            print("Scrolling down...")
            pyautogui.scroll(-3)  # Scroll down
            
        elif action_type == "scroll_up":
            print("Scrolling up...")
            pyautogui.scroll(3)  # Scroll up
            
        elif action_type == "wait":
            seconds = parameters.get("seconds", 1)
            # Convert string to int/float if needed
            try:
                if isinstance(seconds, str):
                    seconds = float(seconds)
                time.sleep(seconds)
            except:
                time.sleep(1)
    
    def get_llm_decision(self, user_goal):
        """Get LLM decision with simplified actions"""
        
        screen_context = self.get_screen_text_simple()
        
        prompt = f"""You are a desktop automation agent. Based on the user goal, decide what actions to take.

User Goal: {user_goal}
Screen Context: {screen_context}

Available Actions:
- open_calculator: Open Windows calculator
- calculator_operation: Do math using keyboard (expression: "1+2")
- open_browser_search: Open browser and search (search_term: "cars")
- open_app: Open application (app_name: "notepad")
- type_text: Type text (text: "hello")
- press_key: Press key (key: "enter")
- scroll_down: Scroll webpage down
- scroll_up: Scroll webpage up
- wait: Wait seconds (seconds: 2)

IMPORTANT: 
1. Use keyboard input for calculator
2. For web searches, extract the FULL search term
3. For scrolling, use scroll_down or scroll_up actions

Respond with ONLY a JSON array:
[
  {{"action": "action_name", "parameters": {{"param": "value"}}}}
]

Examples:
For "search for blue car videos and scroll":
[
  {{"action": "open_browser_search", "parameters": {{"search_term": "blue car videos"}}}},
  {{"action": "wait", "parameters": {{"seconds": 3}}}},
  {{"action": "scroll_down", "parameters": {{}}}},
  {{"action": "scroll_down", "parameters": {{}}}}
]

For "open calculator and add 5 and 3":
[
  {{"action": "open_calculator", "parameters": {{}}}},
  {{"action": "calculator_operation", "parameters": {{"expression": "5+3"}}}}
]

Your response:"""
        
        actions = self.call_ollama(prompt)
        if actions:
            return actions
        
        # Simple fallback
        return self.enhanced_fallback(user_goal)
    
    def enhanced_fallback(self, user_goal):
        """Enhanced rule-based fallback with web browsing"""
        goal = user_goal.lower()
        
        # Search with scrolling
        if "search" in goal and "scroll" in goal:
            if "for" in goal:
                search_part = goal.split("for")[1]
                if "and scroll" in search_part:
                    search_term = search_part.split("and scroll")[0].strip()
                else:
                    search_term = search_part.strip()
            else:
                search_term = goal.replace("search", "").replace("scroll", "").strip()
            
            return [
                {"action": "open_browser_search", "parameters": {"search_term": search_term}},
                {"action": "wait", "parameters": {"seconds": 3}},
                {"action": "scroll_down", "parameters": {}},
                {"action": "scroll_down", "parameters": {}}
            ]
        
        # Just search
        elif "search" in goal:
            if "for" in goal:
                search_term = goal.split("for")[1].strip()
            else:
                search_term = goal.replace("search", "").strip()
            return [{"action": "open_browser_search", "parameters": {"search_term": search_term}}]
        
        # Calculator with math
        elif "calculator" in goal and any(op in goal for op in ["add", "+", "plus"]):
            numbers = re.findall(r'\d+', goal)
            if len(numbers) >= 2:
                expression = f"{numbers[0]}+{numbers[1]}"
                return [
                    {"action": "open_calculator", "parameters": {}},
                    {"action": "calculator_operation", "parameters": {"expression": expression}}
                ]
        
        # Just calculator
        elif "calculator" in goal:
            return [{"action": "open_calculator", "parameters": {}}]
        
        # Math operations
        elif any(op in goal for op in ["add", "+", "plus"]):
            numbers = re.findall(r'\d+', goal)
            if len(numbers) >= 2:
                expression = f"{numbers[0]}+{numbers[1]}"
                return [{"action": "calculator_operation", "parameters": {"expression": expression}}]
        
        # Scrolling only
        elif "scroll" in goal:
            if "down" in goal:
                return [{"action": "scroll_down", "parameters": {}}]
            elif "up" in goal:
                return [{"action": "scroll_up", "parameters": {}}]
            else:
                return [{"action": "scroll_down", "parameters": {}}]
        
        # Open apps
        elif "open" in goal:
            app_name = goal.replace("open", "").strip()
            return [{"action": "open_app", "parameters": {"app_name": app_name}}]
        
        return [{"action": "wait", "parameters": {"seconds": 1}}]
    
    def run_goal(self, user_goal):
        """Execute user goal"""
        print(f"Analyzing: {user_goal}")
        
        actions = self.get_llm_decision(user_goal)
        print(f"Plan: {len(actions)} actions")
        
        for i, action_data in enumerate(actions):
            print(f"Step {i+1}: {action_data['action']}")
            self.execute_action(action_data['action'], action_data.get('parameters', {}))
            time.sleep(1)

def main():
    agent = KeyboardAgent()
    
    print("\nKEYBOARD-BASED DESKTOP AGENT")
    print("Uses keyboard input for reliable automation")
    print("Try: 'open calculator and add 1 and 2'")
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