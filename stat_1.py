import json as js
import statistics
from colorama import Fore, Style # type: ignore
from tabulate import tabulate # type: ignore
import matplotlib.pyplot as plt # type: ignore
from io import BytesIO
import base64

class CentralTendency:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = []
        self.grouped = False
        self.classes = []
        self.frequencies = []
        
    def read_data(self):
        """Read data from JSON file"""
        try:
            with open(self.input_file, 'r') as f:
                content = js.load(f)
                self.grouped = content.get('grouped', False)
                if self.grouped:
                    self.classes = content['classes']
                    self.frequencies = content['frequencies']
                else:
                    self.data = content['data']
            print(Fore.GREEN,"Data loaded successfully from file.", Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED, f"Error reading file: {e}", Style.RESET_ALL)

    def input_data(self):
        """Manually input data"""
        print("1. Ungrouped Data")
        print("2. Grouped Data")
        choice = input("Enter choice: ")

        if choice == '1':
            self.grouped = False
            self.data = []
            print("Enter ungrouped data (press Enter without input to stop):")
            while True:
                num = input()
                if num == "":
                    break
                try:
                    self.data.append(float(num))  
                except ValueError:
                    print("Enter valid numbers only.")

        elif choice == '2':
            self.grouped = True
            self.classes = []
            self.frequencies = []
            print("Enter class intervals (like 10-20) and corresponding frequencies:")
            while True:
                interval = input("Enter the interval (or press Enter to stop): ")
                if interval == '':
                    break
                freq = input("Enter respective frequency: ")
                if freq == "":
                    break
                self.classes.append(interval)
                self.frequencies.append(int(freq))
        else:
            print("Invalid choice. Defaulting to Ungrouped Data.")
            self.grouped = False
            self.input_data()

    def calculate_mean(self):
        """Calculate mean for grouped or ungrouped data"""
        if not self.grouped:
            if not self.data:
                return None
            return statistics.mean(self.data)
        else:
            if not self.classes or not self.frequencies:
                return None
            midpoints = []
            for interval in self.classes:
                if interval.strip() != '':
                    lower, upper = map(float, interval.split('-'))
                    midpoints.append((lower + upper) / 2)
                else:
                    print("Warning: Found empty class interval. Skipping.")
            if not midpoints:
                return None

            total_fx = sum(f * x for f, x in zip(self.frequencies, midpoints))
            total_f = sum(self.frequencies)
            if total_f == 0:
                return None
            return total_fx / total_f

    def calculate_median(self):
        """Calculate median for grouped or ungrouped data"""
        if not self.grouped:
            if not self.data:
                return None
            return statistics.median(self.data)
        else:
            if not self.classes or not self.frequencies:
                return None
            cumulative_freq = []
            cum_sum = 0
            for freq in self.frequencies:
                cum_sum += freq
                cumulative_freq.append(cum_sum)

            N = cumulative_freq[-1]
            Nby2 = N / 2
            median_class_index = 0
            for i, cf in enumerate(cumulative_freq):
                if cf >= Nby2:
                    median_class_index = i
                    break

            L, U = map(float, self.classes[median_class_index].split('-'))
            f = self.frequencies[median_class_index]
            CF = cumulative_freq[median_class_index - 1] if median_class_index != 0 else 0
            h = U - L

            median = L + ((Nby2 - CF) / f) * h
            return median

    def calculate_mode(self):
        """Calculate mode for grouped or ungrouped data"""
        if not self.grouped:
            if not self.data:
                return None
            modes = statistics.multimode(self.data)
            if len(modes) == 1:
                return modes[0]
            else:
                return modes
        else:
            if not self.classes or not self.frequencies:
                return None
            modal_class_index = self.frequencies.index(max(self.frequencies))
            f1 = self.frequencies[modal_class_index]
            f0 = self.frequencies[modal_class_index - 1] if modal_class_index != 0 else 0
            f2 = self.frequencies[modal_class_index + 1] if modal_class_index != len(self.frequencies) - 1 else 0
            L, U = map(float, self.classes[modal_class_index].split('-'))
            h = U - L

            try:
                mode = L + ((f1 - f0) / (2 * f1 - f0 - f2)) * h
            except ZeroDivisionError:
                mode = (L + U) / 2  
            return mode

    def compute_all(self):
        """Compute Mean, Median, Mode"""
        if not self.data and not self.classes:
            return {}

        mean = self.calculate_mean()
        median = self.calculate_median()
        mode = self.calculate_mode()

        result = {
            "Grouped": self.grouped,
            "Mean": round(mean, 2) if mean is not None else None,
            "Median": round(median, 2) if median is not None else None,
            "Mode": round(mode, 2) if isinstance(mode, (int, float)) else mode
        }
        return result
    
    def generate_cumulative_frequency_table(self):
        if not self.grouped or not self.classes or not self.frequencies :
            print(Fore.RED, "The comulative table only generated for the Grouped data.", Style.RESET_ALL)
        
        cumultive = []
        cum_sum = 0
        for freq in self.frequencies :
            cum_sum += freq
            cumultive.append(cum_sum)
        
        table = []
        for cls, freq, cum_freq in zip(self.classes, self.frequencies, cumultive):
            table.append({
                "Class Interval" : cls,
                "Frequency" : freq,
                "Cumulative Frequecny" : cum_freq
            })

        try :
            with open("C:/Users/HP/Desktop/Himanshu/My Projects/Python projects/Statistics/cumulative.json", 'w') as f:
                js.dump(table, f, indent= 2)
            print(Fore.GREEN,"Data Saved successfully.", Style.RESET_ALL)
        except Exception as e:
            print(f"❌ Error saving cumulative frequency file: {e}")
        
        return table
    
    def plot_histogram(self):
        if not self.grouped or not self.classes or not self.frequencies:
            print(Fore.RED, "Histogram requires grouped data.", Style.RESET_ALL)
        else :
            midpoint = []
            width = []
            for interval in self.classes:
                if interval.strip() != '-':
                    lower, upper = map(float, interval.split('-'))
                    mid = (lower + upper)/2
                    width.append(upper - lower) 
                    midpoint.append(mid)

            class_width = sum(width) / len(width)
            plt.figure(figsize = (8, 5))
            plt.bar(midpoint, self.frequencies, width=class_width * 0.9, edgecolor = 'black')
            plt.xlabel('Class Midpoint')
            plt.ylabel('Frequencies')
            plt.title("Histogram of Grouped Data")
            plt.grid(axis='y', linestyle = '--', alpha = 0.7)
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format = 'png')
            plt.close()
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return img_base64 

    def save_file(self, result):
        """Save the computed results to output JSON file"""
        try:
            with open(self.output_file, 'w') as f:
                js.dump(result, f, indent=4)
            print(Fore.BLUE, f"Results saved successfully to {self.output_file}", Style.RESET_ALL)
        except Exception as e:
            print(f"Error saving file: {e}")

if __name__ == '__main__':
    ct = CentralTendency(
        'C:/Users/HP/Desktop/Himanshu/My Projects/Python projects/Statistics/input.json',
        'C:/Users/HP/Desktop/Himanshu/My Projects/Python projects/Statistics/output.json'
    )
    choice = input("Press 1 to manually input data, 2 to load from JSON file: ")
    if choice == '1':
        ct.input_data()
    elif choice == '2':
        ct.read_data()
    else:
        print("Invalid choice. Defaulting to manual input.")
        ct.input_data()
    table = ct.generate_cumulative_frequency_table()
    print(tabulate(table,headers= 'keys', tablefmt= 'grid'))
    result = ct.compute_all()
    print(Fore.CYAN,"\nResults:",Style.RESET_ALL, Fore.GREEN, result, Style.RESET_ALL)
    ct.plot_histogram()
    ct.save_file(result)