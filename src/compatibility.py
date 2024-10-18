from src.utils import clear_screen

class Compatibility:
    def __init__(self, inventory_object):
        self.inventory_object = inventory_object
        self.total_power_consuption: int = 0

    def update_power_draw(self, item_type, wattage):
        if item_type != "PSU":
            wattage = wattage * -1

        self.total_power_consuption = self.total_power_consuption + wattage

    def check_ids(self, item_id_list):
        # Creating a parts dict with item objects for organization for later.
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
        if motherboard.socket != cpu.socket:
            print(f"{cpu.name} ({cpu.id}) is not compatible with {motherboard.name} "
                  f"({motherboard.id})")
        else:
            print(f"{cpu.name} ({cpu.id}) is compatible with {motherboard.name} ({motherboard.id})")

    def ram_id_validation(self, ram_list):
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
        motherboard_ram_slots = int(motherboard.ram_slots)
        ram_list_len = len(ram_list)

        if ram_list_len <= motherboard_ram_slots:
            print("Motherboard is able to support the total number of RAM listed.")
        else:
            print("The total amount of RAM listed is greater than the number of slots on the \
                  motherboard.")

    def power_draw_check(self):
        if self.total_power_consuption > 0:
            print("The powerdraw for these parts is within the PSU's available capacity.")
        elif self.total_power_consuption < 0:
            print("The powerdraw for these parts exceeds the PSU. You will need to upgrade it.")
        else:
            print("The powerdraw for these parts is at max capacity. Consider upgrading the PSU.")

    def compatibility_check(self):
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
        clear_screen()
        self.total_power_consuption = build_power_draw
        #TODO: validate that a motherboard exists
        if not build_object["Motherboard"]:
            print("A valid build requires a single motherboard. Please select one for your build.")
            return False

        #TODO: validate that a ram exists
        if not build_object["RAM"]:
            print("A valid build requires RAM. Please add to your build.")
            print("Keep in mind that your Motherboard has a limited number of RAM slots.")
            return False

        #TODO: validate that a cpu exists
        elif not build_object["CPU"]:
            print("A valid build requires a CPU. Please select one for your build.")
            print("Please note that your Motherboard socket and CPU socket need to match.")
            return False

        #TODO: validate that storage exists
        elif not build_object["Storage"]:
            print("A valid build requires Storage. Please select one for your build.")
            return False

        #TODO: validate that a psu exists
        elif not build_object["PSU"]:
            print("A valid build requires a Power Supply (PSU). Please select one for your build.")
            return False

        else:
             #TODO: validate motherboard and cpu are compatible
            self.motherboard_cpu_validation(build_object["Motherboard"], build_object["CPU"])

            #TODO: validate that motherboard ram slots <= total number of ram
            self.motherboard_ram_slot_validation(build_object["Motherboard"], build_object["RAM"])

            #TODO: validate that ram types are the same if 2>
            self.ram_id_validation(build_object["RAM"])

            #TODO: validate that the PSU can support the power draw
            self.power_draw_check()
            print("")
            return True
