"""
This module contains the `Compatibility` class, which is used to validate the 
compatibility of computer hardware components. The class supports checking 
compatibility for various parts such as CPUs, GPUs, RAM, power supplies (PSUs), 
motherboards, and storage devices. It ensures that components are correctly 
matched in terms of sockets, RAM slots, and power consumption.

Key functionality includes:
- Validating if CPU and motherboard sockets are compatible.
- Checking if the number of RAM modules fits within the available motherboard slots.
- Ensuring that power draw from components does not exceed the PSU's capacity.
- Validating if all necessary components for a build are included and compatible.

Usage:
Create an instance of `Compatibility` by passing an inventory object. Then use
methods like `compatibility_check` or `build_check` to perform the validation 
process.
"""
from src.utils import clear_screen

class Compatibility:
    """
    Compatibility class to check and validate the compatibility of various computer parts,
    such as CPU, RAM, PSU, Motherboard, and Storage. It also calculates the power consumption 
    and performs various validation checks on the selected parts.
    """
    def __init__(self, inventory_object):
        self.inventory_object = inventory_object
        self.total_power_consuption: int = 0

    def update_power_draw(self, item_type, wattage):
        """
        Updates the total power consumption based on the item type and its wattage.
        If the item is not a PSU, its power draw is subtracted from the total.

        Args:
            item_type (str): The type of the item (e.g., CPU, GPU).
            wattage (int): The power draw or supply of the item in watts.
        """
        if item_type != "PSU":
            wattage = wattage * -1

        self.total_power_consuption = self.total_power_consuption + wattage

    def check_ids(self, item_id_list):
        """
        Validates the provided item IDs, matches them with the inventory, and organizes them into 
        categories.

        Args:
            item_id_list (list): List of item IDs provided by the user.

        Returns:
            dict: A dictionary with categorized parts (CPU, GPU, RAM, etc.), or None if invalid ID 
            is provided.
        """
        part_dict = {
            "CPU": [],
            "GPU": [],
            "RAM": [],
            "PSU": [],
            "Motherboard": [],
            "Storage": []
        }

        # Check that each user provided item id exists within the inventory data.
        id_list = []

        # Creating a list of IDs to validate the user's input before processing.
        for item in self.inventory_object.items:
            id_list.append(item.id)

        # validating user input and adding valid items to the dict.
        for individual_item in item_id_list:
            if individual_item.upper() in id_list:
                for item in self.inventory_object.items:
                    if item.id.lower() == individual_item.lower():
                        part_dict[item.type].append(item)

                        # Update Power Draw / Supply variable
                        if item.type != "PSU":
                            self.update_power_draw(item.type, item.power_draw)
                        else:
                            self.update_power_draw(item.type, item.power_supplied)
            else:
                # Ending the validation process and returning None if the user provides
                # an invalid part id.
                return None

        # return the completed dict.
        return part_dict

    def motherboard_cpu_validation(self, motherboard, cpu):
        """
        Validates whether the CPU is compatible with the motherboard based on the socket type.

        Args:
            motherboard (object): The motherboard object.
            cpu (object): The CPU object.
        """
        if motherboard.socket != cpu.socket:
            print(f"{cpu.name} ({cpu.id}) is not compatible with {motherboard.name} "
                  f"({motherboard.id})")
        else:
            print(f"{cpu.name} ({cpu.id}) is compatible with {motherboard.name} ({motherboard.id})")

    def ram_id_validation(self, ram_list):
        """
        Validates whether all provided RAM sticks are identical in terms of ID.

        Args:
            ram_list (list): List of RAM objects to be validated.
        """
        if len(ram_list) == 1:
            print(f"All motherboards are compatible when only given 1 RAM.")
        else:
            first_ram_id = ram_list[0].id
            for ram_object in ram_list[1:]:
                if ram_object.id != first_ram_id:
                    print("RAM ID's Do Not Match. All motherboards require matching RAM.")
                    break
                else:
                    print("RAM Matches")

    def motherboard_ram_slot_validation(self, motherboard, ram_list):
        """
        Validates whether the number of RAM sticks can be supported by the motherboard's available 
        slots.

        Args:
            motherboard (object): The motherboard object.
            ram_list (list): List of RAM objects.
        """
        motherboard_ram_slots = int(motherboard.ram_slots)
        ram_list_len = len(ram_list)

        if ram_list_len <= motherboard_ram_slots:
            print("Motherboard is able to support the total number of RAM listed.")
        else:
            print("The total amount of RAM listed is greater than the number of slots on the \
                  motherboard.")

    def power_draw_check(self):
        """
        Checks whether the total power draw is within the PSU's capacity.
        """
        if self.total_power_consuption > 0:
            print("The powerdraw for these parts is within the PSU's available capacity.")
        elif self.total_power_consuption < 0:
            print("The powerdraw for these parts exceeds the PSU. You will need to upgrade it.")
        else:
            print("The powerdraw for these parts is at max capacity. Consider upgrading the PSU.")

    def compatibility_check(self):
        """
        Performs a compatibility check on the selected parts provided by the user.
        Validates the power draw, CPU-motherboard compatibility, and RAM-motherboard compatibility.
        """
        clear_screen()
        print("What part(s) do you want to perform a compatibility check on?")
        print("Provide part IDs only and separate using commas.")
        print("Example: part_id01, part_id02,...")
        user_input = input("\nItem IDs: ")

        # Clean the list of item_ids
        item_id_list = [item_id.strip() for item_id in user_input.split(',')]

        # Validate there is more than one item_id in the list
        if len(item_id_list) <= 1:
            clear_screen()
            print("""The compatibility check requires two or more parts.\nUnable to complete this \
                  request.""")
            return None

        valid_id_dict = self.check_ids(item_id_list)

        try:
            clear_screen()
            print(f"Power Draw: {self.total_power_consuption}W")
            print(f"Listed Items: {user_input}")

            # Run through each check for each motherboard in the list.
            if valid_id_dict["Motherboard"]:
                for motherboard in valid_id_dict["Motherboard"]:
                    # Loop through each item in the "CPU" list.
                    if valid_id_dict["CPU"]:
                        for cpu in valid_id_dict["CPU"]:
                            self.motherboard_cpu_validation(motherboard, cpu)
                    if valid_id_dict["RAM"]:
                        self.motherboard_ram_slot_validation(motherboard, valid_id_dict["RAM"])

            if valid_id_dict["RAM"]:
                self.ram_id_validation(valid_id_dict["RAM"])

            if valid_id_dict["PSU"]:
                self.power_draw_check()
        except TypeError as e:
            clear_screen()
            print("There was an error when attempting to process this request. Please try again.")

    def build_check(self, build_object, build_power_draw):
        """
        Validates whether a complete build is compatible and functional.
        Ensures that all necessary parts are present, and checks compatibility between the parts.

        Args:
            build_object (dict): A dictionary containing the build's parts.
            build_power_draw (int): The total power draw of the build.
        
        Returns:
            bool: True if the build is valid, False otherwise.
        """
        clear_screen()
        self.total_power_consuption = build_power_draw
        #Validate that a motherboard exists
        if not build_object["Motherboard"]:
            print("A valid build requires a single motherboard. Please select one for your build.")
            return False

        #Validate that a ram exists
        if not build_object["RAM"]:
            print("A valid build requires RAM. Please add to your build.")
            print("Keep in mind that your Motherboard has a limited number of RAM slots.")
            return False

        #Validate that a cpu exists
        elif not build_object["CPU"]:
            print("A valid build requires a CPU. Please select one for your build.")
            print("Please note that your Motherboard socket and CPU socket need to match.")
            return False

        #Validate that storage exists
        elif not build_object["Storage"]:
            print("A valid build requires Storage. Please select one for your build.")
            return False

        #Validate that a psu exists
        elif not build_object["PSU"]:
            print("A valid build requires a Power Supply (PSU). Please select one for your build.")
            return False

        else:
             #Validate motherboard and cpu are compatible
            self.motherboard_cpu_validation(build_object["Motherboard"], build_object["CPU"])

            #Validate that motherboard ram slots <= total number of ram
            self.motherboard_ram_slot_validation(build_object["Motherboard"], build_object["RAM"])

            #Validate that ram types are the same if 2>
            self.ram_id_validation(build_object["RAM"])

            #Validate that the PSU can support the power draw
            self.power_draw_check()
            print("")
            return True
