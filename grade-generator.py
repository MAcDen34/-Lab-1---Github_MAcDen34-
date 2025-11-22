import csv

class Assignment:
    def __init__(self, name, category, grade, weight):
        self.name = name
        self.category = category.upper()
        self.grade = float(grade)
        self.weight = float(weight)

class GradeCalculator:
    def __init__(self):
        self.assignments = []
        self.total_FA_weight = 0
        self.total_SA_weight = 0
        self.total_FA_grade = 0
        self.total_SA_grade = 0

    def validate_input(self, category, grade, weight):
        """Validate all input parameters"""
        errors = []
        
        # Validate category
        if category.upper() not in ['FA', 'SA']:
            errors.append("Category must be 'FA' or 'SA'")
        
        # Validate grade
        try:
            grade_float = float(grade)
            if not (0 <= grade_float <= 100):
                errors.append("Grade must be between 0 and 100")
        except ValueError:
            errors.append("Grade must be a number")
        
        # Validate weight
        try:
            weight_float = float(weight)
            if weight_float <= 0:
                errors.append("Weight must be positive")
        except ValueError:
            errors.append("Weight must be a number")
        
        return errors

    def add_assignment(self):
        """Add a new assignment with validation"""
        print("\n--- Add New Assignment ---")
        
        name = input("Assignment Name: ").strip()
        while name == "":
            print("✗ Assignment name cannot be empty.")
            name = input("Assignment Name: ").strip()

        category = input("Category (FA/SA): ").strip()

        while category.upper() not in ['FA', 'SA']:
            print("✗ Invalid category. Must be 'FA' or 'SA'.")
            category = input("Category (FA/SA): ").strip()

        grade = input("Grade (0-100): ").strip()

        while grade == "" or not grade.replace('.', '', 1).isdigit() or not (0 <= float(grade) <= 100):
            print("✗ Invalid grade. Must be a number between 0 and 100.")
            grade = input("Grade (0-100): ").strip()

        weight = input("Weight: ").strip()

        while weight == "" or not weight.replace('.', '', 1).isdigit() or float(weight) <= 0:
            print("✗ Invalid weight. Must be a positive number.")
            weight = input("Weight: ").strip()
        
        # Validate input
        # errors = self.validate_input(category, grade, weight)
        # if errors:
        #     print("Validation errors:")
        #     for error in errors:
        #         print(f"  - {error}")
        #     return False
        
        # Create and store assignment
        assignment = Assignment(name, category, grade, weight)
        self.assignments.append(assignment)
        
        # Update totals
        weighted_grade = (assignment.grade / 100) * assignment.weight
        if assignment.category == 'FA':
            self.total_FA_weight += assignment.weight
            self.total_FA_grade += weighted_grade
        else:  # SA
            self.total_SA_weight += assignment.weight
            self.total_SA_grade += weighted_grade
            
        print(f"Assignment '{name}' added successfully!")
        return True

    def calculate_results(self):
        """Calculate final results"""
        total_grade = self.total_FA_grade + self.total_SA_grade
        cp_score = (total_grade / 100) * 5.0 if total_grade > 0 else 0
        
        # Pass/Fail logic
        FA_pass = self.total_FA_grade >= (self.total_FA_weight * 0.5) if self.total_FA_weight > 0 else True
        SA_pass = self.total_SA_grade >= (self.total_SA_weight * 0.5) if self.total_SA_weight > 0 else True
        overall_pass = FA_pass and SA_pass
        
        return {
            'total_FA_grade': self.total_FA_grade,
            'total_FA_weight': self.total_FA_weight,
            'total_SA_grade': self.total_SA_grade,
            'total_SA_weight': self.total_SA_weight,
            'total_grade': total_grade,
            'cp_score': cp_score,
            'overall_pass': overall_pass,
            'FA_pass': FA_pass,
            'SA_pass': SA_pass
        }

    def print_summary(self):
        """Print results summary to console"""
        results = self.calculate_results()
        
        print("\n" + "="*50)
        print("GRADE SUMMARY")
        print("="*50)
        
        print(f"Total Formative: {results['total_FA_grade']:.2f} / {results['total_FA_weight']:.2f}")
        print(f"Total Summative: {results['total_SA_grade']:.2f} / {results['total_SA_weight']:.2f}")
        print(f"Total Grade: {results['total_grade']:.2f} / 100")
        print(f"CP Score: {results['cp_score']:.3f}")
        
        # Determine class based on CP score
        cp = results['cp_score']
        if cp >= 4.5:
            grade_class = "1st Class"
        elif cp >= 3.5:
            grade_class = "2nd Class Upper"
        elif cp >= 2.5:
            grade_class = "2nd Class Lower"
        elif cp >= 1.5:
            grade_class = "3rd Class"
        else:
            grade_class = "Fail"
        
        print(f"Class: {grade_class}")
        print(f"Status: {'PASS' if results['overall_pass'] else 'FAIL'}")
        
        if results['overall_pass'] is False:
            print("Resubmission : Discussion Forum")


        # if not results['FA_pass']:
        #     print("Must resubmit Formative assignments")
        # if not results['SA_pass']:
        #     print("Must resubmit Summative assignments")

    def export_to_csv(self):
        """Export assignments to CSV file"""
        filename = "grades.csv"
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Assignment', 'Category', 'Grade', 'Weight'])
                
                for assignment in self.assignments:
                    writer.writerow([
                        assignment.name,
                        assignment.category,
                        assignment.grade,
                        assignment.weight
                    ])
            
            print(f"\n Grades exported to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error exporting to CSV: {e}")
            return False

    def run(self):
        """Main program loop"""
        print("="*50)
        print("GRADE GENERATOR CALCULATOR")
        print("="*50)
        
        while True:
            self.add_assignment()
            
            # Ask if user wants to add another assignment
            while True:
                another = input("\nAdd another assignment? (y/n): ").strip().lower()
                if another in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if another == 'n':
                break
        
        if self.assignments:
            self.print_summary()
            self.export_to_csv()
        else:
            print("No assignments were added.")

if __name__ == "__main__":
    calculator = GradeCalculator()
    calculator.run()
