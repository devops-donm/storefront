# CCD JQR Project 1 - Python Storefront
---
A command-line utility that offers a personalized shopping experience for building custom computers, ensuring part compatibility and budget management in real-time.

## Usage
#### 1. Run the script:
```
python storefront.py inventory.json
```

#### 2. Starting the Store:
- Upon starting, the script will prompt you to enter your name and budget.
- After entering this information, a text-based menu will appear with various options.
- Use the Number/Character options to perform an action.
Example: In the main menu. To list parts press option "1"

#### 3. Available Menu Options
- **1. list:**
List all of the available parts from the inventory based on part category (All, CPU, GPU, ...)

- **2. details:**
Display the details of a particular part from the inventory by providing the item's id (cpu_01, gpu_01, ...)

- **compatibility:**
Check the compatibility of particular parts by providing a comma separated list of item ids
``cpu_01, gpu_01, ram_01, psu_01``

- **build:**
Build a custom computer. Provides you the ability to track the build process, add/remove parts, check compatibility, and add to shopping cart.

- **cart:**
Manage the stores shopping cart. Provides you the ability to track the individual parts / custom build, manage costs, add/remove parts/build from cart, and checkout.

- **change budget:**
Allows you to update your available budget.

- **change name:**
Allows you to update your name.

- **Help**
Provides the above information about each command within the terminal

- **Exit**
Allows you to gracefully exit the program.
Ctrl + c also allows you to gracefully exit.

#### 4. Contributing
Contributions are welcome! To contribute, follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request