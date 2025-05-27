
# 📊 Statistics Calculator

A web-based statistics calculator built using **Flask (Python)** and **Vanilla JavaScript**. This tool allows users to compute the **mean, median, and mode** for both **ungrouped and grouped data**, generate **cumulative frequency tables**, and plot **histograms** for grouped data.

## 🚀 Features

- 📈 Supports both **ungrouped** and **grouped** datasets
- 📊 Computes **mean**, **median**, and **mode**
- 📉 Generates **cumulative frequency tables**
- 🖼️ Plots **histograms** for grouped data
- 🎨 Clean, responsive UI with modern styling

## 🧱 Project Structure

```
.
├── app.py                  # Flask backend
├── stat_1.py               # CentralTendency class for all statistical calculations
├── templates/
│   └── index.html          # Frontend HTML with UI for user input
├── static/
│   ├── css/
│   │   └── style.css       # Styling for the app
│   └── js/
│       └── script.js       # Handles DOM and client-side interactions
```

## 📦 Dependencies

Ensure you have the following Python packages installed:

```bash
pip install flask matplotlib colorama tabulate
```

## 🛠️ How to Run

1. **Clone or Download** this repository.
2. Navigate to the project directory.
3. Run the Flask server:

```bash
python app.py
```

4. Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 💡 Usage

- Choose between **Ungrouped Data** or **Grouped Data** using the toggle.
- Enter:
  - For ungrouped: comma-separated numbers (e.g., `10, 20, 30`)
  - For grouped: class intervals (`10-20,20-30,...`) and frequencies (`5,10,...`)
- Click:
  - **Compute Statistics** to get mean, median, and mode.
  - **Generate Cumulative Frequency** to view the table.
  - **Generate Histogram** to visualize grouped data.

## 🧠 Core Logic

All statistical computations are handled by the `CentralTendency` class in `stat_1.py`, which includes methods to:

- Calculate **mean**, **median**, **mode** (for both grouped and ungrouped)
- Generate cumulative frequency tables
- Plot histograms using `matplotlib`

## 📸 Screenshot

![App Screenshot](/assest/screenshot_1.jpg)
![App Screenshot](/assest/screenshot_2.jpg)
![app screenshot](/assest/screenshot_3.jpg)
![App screenshot](/assest/screenshot_4.jpg)
## 📝 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

## 👤 Author

Himanshu and contributors  
BTech in Computer Science | Statistics & Data Visualization Enthusiast
