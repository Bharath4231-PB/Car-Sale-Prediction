# 🚀 HOW TO RUN - Car Sales Price Prediction System

## ⚡ Quick Start (10 minutes total)

Follow these steps in order:

---

## STEP 1: Open Terminal/Command Prompt
**Windows:**
- Press `Win + R`
- Type `cmd`
- Press Enter

**Or use PowerShell:**
- Right-click in project folder
- Click "Open PowerShell here"

---

## STEP 2: Navigate to Project Folder
```powershell
cd "e:\car sales prediction\car_sales_prediction"
```

Check you're in the right folder:
```powershell
dir
```

You should see files like: `app.py`, `train_model.py`, etc.

---

## STEP 3: Install Python Packages (ONE TIME ONLY)
```powershell
pip install -r requirements.txt
```

⏱️ **Takes 2-3 minutes**

Wait for it to finish. You'll see:
```
Successfully installed Flask-3.0.0 pandas-2.1.4 ...
```

---

## STEP 4: Start MySQL Database
**Windows Command Prompt (as Administrator):**
```cmd
net start MySQL80
```

**Or manually:**
- Open Services (services.msc)
- Find "MySQL80"
- Right-click → Start

**Or use MySQL Workbench:**
- Open MySQL Workbench
- Click "Local instance MySQL80"

---

## STEP 5: Create Database (ONE TIME ONLY)
```powershell
mysql -u root -pben10 < database.sql
```

You should see no errors. Done!

---

## STEP 6: Train the ML Model (ONE TIME ONLY)
```powershell
python train_model.py
```

⏱️ **Takes 10-20 seconds**

You'll see:
```
Loading dataset...
Dataset shape: (50, 8)
Preprocessing data...
Training RandomForestRegressor model...

Model Performance:
Training R² Score: 0.9234
Test R² Score: 0.8945

✓ Model saved as model.pkl
✓ Label encoders saved as label_encoders.pkl
```

---

## STEP 7: RUN THE APPLICATION
```powershell
python app.py
```

⏱️ **Starts immediately**

You'll see:
```
==================================================
🚗 Car Sales Price Prediction System
==================================================
Starting Flask app on http://127.0.0.1:5000
Press CTRL+C to stop the server

 * Running on http://127.0.0.1:5000
```

---

## STEP 8: Open in Browser
Click this link or copy-paste in browser:

**http://127.0.0.1:5000**

You should see the home page with features and buttons!

---

## STEP 9: Login or Register

### Option A: Login with Test Admin Account
```
Username: admin
Password: admin123
```

Click "Login" button

### Option B: Create New Account
Click "Register"
- Enter username
- Enter email
- Enter password (min 6 characters)
- Click "Register"
- Then login

---

## STEP 10: Make a Prediction

After login:
1. Click "Predict Price" button
2. Fill in car details:
   - Car Name: Select from dropdown
   - Year: Enter year (e.g., 2018)
   - Present Price: Enter price in Lakhs (e.g., 12.5)
   - KMs Driven: Enter KMs (e.g., 30000)
   - Fuel Type: Select Petrol or Diesel
   - Seller Type: Select Dealer or Individual
   - Transmission: Select Manual or Automatic
   - Owner: Select count (1, 2, 3, 4+)
3. Click "Predict Price"
4. See result instantly!

---

## ✅ Everything Working?

Check:
- ✅ Home page loads
- ✅ Can register user
- ✅ Can login
- ✅ Dashboard shows stats
- ✅ Can make prediction
- ✅ Result displays
- ✅ History saves predictions

If yes → **All working! 🎉**

---

## 🛑 TO STOP THE SERVER

In terminal where Flask is running:
```
Press CTRL + C
```

---

## 🔄 TO RUN AGAIN NEXT TIME

Just do:
```powershell
cd "e:\car sales prediction\car_sales_prediction"
python app.py
```

**That's it!** (Steps 1-6 only needed once)

---

## 📋 Summary of Commands

| Command | What it Does | Run When |
|---------|------------|----------|
| `pip install -r requirements.txt` | Install packages | First time only |
| `net start MySQL80` | Start database | Each time (Windows) |
| `mysql -u root -pben10 < database.sql` | Create database | First time only |
| `python train_model.py` | Train ML model | First time only |
| `python app.py` | Run the app | Every time you want to use it |

---

## ⚠️ Common Issues & Solutions

### Issue: "Python: command not found"
**Solution:**
- Python not installed or not in PATH
- Try: `python3 app.py`
- Or install Python from python.org

### Issue: "Connection refused" (Database)
**Solution:**
- MySQL not running
- Run: `net start MySQL80`
- Or open MySQL Workbench

### Issue: "model.pkl not found"
**Solution:**
- Train model first
- Run: `python train_model.py`

### Issue: "404 Not Found" (CSS/Images)
**Solution:**
- Browser cache issue
- Press: `Ctrl + Shift + Delete` to clear cache
- Reload page: `Ctrl + F5`

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
- Packages not installed
- Run: `pip install -r requirements.txt`

---

## 🎯 First Time Full Setup

```powershell
# Step 1: Go to folder
cd "e:\car sales prediction\car_sales_prediction"

# Step 2: Install packages (takes 2-3 minutes)
pip install -r requirements.txt

# Step 3: Start MySQL (in another terminal as admin)
net start MySQL80

# Step 4: Create database
mysql -u root -pben10 < database.sql

# Step 5: Train model (takes 10-20 seconds)
python train_model.py

# Step 6: Run app
python app.py

# Step 7: Open browser
# http://127.0.0.1:5000
```

**Total time: ~5 minutes** ⚡

---

## 📞 Need Help?

- Read: **README.md** (comprehensive guide)
- Read: **QUICKSTART.txt** (detailed setup)
- Read: **INDEX.md** (file reference)

All in the project folder!

---

**Ready? Start with Step 1!** 🚀
