import json
import os
import webbrowser
from datetime import datetime

# ==========================================
# CSBS PROJECT: THE PRODUCTIVITY SUITE
# ==========================================

DATA_FILE = "student_data.json"

class ProductivitySuite:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """Loads data from a JSON file to ensure persistence."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        else:
            # Default structure if file doesn't exist
            return {
                "exams": [],      # For Scheduler
                "resources": {},  # For Resource Hub
                "analytics": {}   # For Efficiency Engine (Subject: {hours: 0, marks: 0})
            }

    def save_data(self):
        """Saves current state to JSON."""
        with open(DATA_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)

    # ----------------------------------------------------
    # MODULE A: SMART SCHEDULER
    # ----------------------------------------------------
    def add_exam(self):
        subject = input("Enter Subject Name: ")
        date_str = input("Enter Exam Date (DD-MM-YYYY): ")
        try:
            # Validate date format
            exam_date = datetime.strptime(date_str, "%d-%m-%Y")
            self.data["exams"].append({"subject": subject, "date": date_str})
            self.save_data()
            print(f"✅ Exam for {subject} added successfully!")
        except ValueError:
            print("❌ Invalid Date Format! Please use DD-MM-YYYY.")

    def show_schedule(self):
        print("\n--- 📅 UPCOMING EXAMS & DEADLINES ---")
        if not self.data["exams"]:
            print("No exams scheduled.")
        
        today = datetime.now()
        for exam in self.data["exams"]:
            exam_date = datetime.strptime(exam['date'], "%d-%m-%Y")
            days_left = (exam_date - today).days + 1
            
            if days_left < 0:
                status = "COMPLETED"
            elif days_left <= 3:
                status = "🚨 CRITICAL (Start Cramming!)"
            else:
                status = "🟢 On Track"
                
            print(f"• {exam['subject']}: {days_left} days left | Status: {status}")

    # ----------------------------------------------------
    # MODULE B: RESOURCE HUB
    # ----------------------------------------------------
    def add_resource(self):
        subject = input("Enter Subject for this resource: ")
        # Tip: You can paste a website URL or a file path here
        link = input("Enter Link (URL or File Path): ")
        
        if subject not in self.data["resources"]:
            self.data["resources"][subject] = []
        
        self.data["resources"][subject].append(link)
        self.save_data()
        print("✅ Resource saved!")

    def open_resource(self):
        print("\n--- 📚 RESOURCE LIBRARY ---")
        subjects = list(self.data["resources"].keys())
        
        if not subjects:
            print("No resources found.")
            return

        for idx, sub in enumerate(subjects, 1):
            print(f"{idx}. {sub}")
            
        choice = int(input("Select a Subject Number: ")) - 1
        
        if 0 <= choice < len(subjects):
            selected_sub = subjects[choice]
            links = self.data["resources"][selected_sub]
            
            print(f"Links for {selected_sub}:")
            for i, link in enumerate(links, 1):
                print(f"{i}. {link}")
                
            link_choice = int(input("Select Link to Open: ")) - 1
            if 0 <= link_choice < len(links):
                print(f"Opening... {links[link_choice]}")
                webbrowser.open(links[link_choice]) # Python magic to open browser/file
            else:
                print("❌ Invalid Link choice.")
        else:
            print("❌ Invalid Subject choice.")

    # ----------------------------------------------------
    # MODULE C: EFFICIENCY ENGINE (ROI CALC)
    # ----------------------------------------------------
    def log_study_session(self):
        subject = input("Subject studied: ")
        hours = float(input("Hours spent: "))
        
        if subject not in self.data["analytics"]:
            self.data["analytics"][subject] = {"hours": 0, "marks": 0}
            
        self.data["analytics"][subject]["hours"] += hours
        self.save_data()
        print(f"✅ Logged {hours} hours for {subject}.")

    def log_marks(self):
        subject = input("Enter Subject: ")
        marks = float(input("Enter Marks Obtained (out of 100): "))
        
        if subject in self.data["analytics"]:
            self.data["analytics"][subject]["marks"] = marks
            self.save_data()
            print("✅ Marks updated.")
        else:
            print("❌ No study data found for this subject. Log hours first.")

    def show_roi(self):
        print("\n--- 📈 EFFICIENCY ANALYTICS (ROI) ---")
        print(f"{'Subject':<15} {'Hours':<10} {'Marks':<10} {'ROI (Marks/Hour)'}")
        print("-" * 55)
        
        for sub, stats in self.data["analytics"].items():
            h = stats["hours"]
            m = stats["marks"]
            
            # Avoid division by zero
            roi = round(m / h, 2) if h > 0 else 0
            
            # Simple Analysis
            if roi > 5:
                performance = "🔥 High Efficiency"
            elif roi > 2:
                performance = "✅ Good"
            else:
                performance = "⚠️ Needs Improvement"
                
            print(f"{sub:<15} {h:<10} {m:<10} {roi} ({performance})")

# ==========================================
# MAIN MENU LOOP
# ==========================================
def main():
    app = ProductivitySuite()
    
    while True:
        print("\n" + "="*40)
        print(" 🚀 PRODUCTIVITY SUITE (CSBS FY)")
        print("="*40)
        print("1. Add Exam Date")
        print("2. Show Upcoming Schedule")
        print("3. Add Study Resource (Link/File)")
        print("4. Open a Resource")
        print("5. Log Study Hours")
        print("6. Log Exam Marks")
        print("7. View Efficiency (ROI) Analysis")
        print("8. Exit")
        
        choice = input("\nEnter Choice (1-8): ")
        
        if choice == '1': app.add_exam()
        elif choice == '2': app.show_schedule()
        elif choice == '3': app.add_resource()
        elif choice == '4': app.open_resource()
        elif choice == '5': app.log_study_session()
        elif choice == '6': app.log_marks()
        elif choice == '7': app.show_roi()
        elif choice == '8': 
            print("Exiting... Good luck with your studies! 👋")
            break
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()