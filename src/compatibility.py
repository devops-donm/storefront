from src.utils import clear_screen

class Compatibility:
    def __init__(self, inventory_object):
        self.inventory_object = inventory_object
    
    def compatibility_check(self):
        print("What part(s) do you want to perform a compatibility check on?")
        print("Provide part IDs only and separate using commas.")
        print("Example: part_id01, part_id02,...")
        user_input = input("\nItem IDs: ")

        #TODO: clean the list of item_ids
        item_id_list = [item_id.strip() for item_id in user_input.split(',')]

        #TODO: validate there is more than one item_id
        if len(item_id_list) <= 1:
            print("""The compatibility check requires two or more parts.\n
                  Unable to complete this request.""")
            return

        # This is here to keep it out of the way. Please don't move it. Thanks!
        part_dict = {
            "cpu": [],
            "gpu": [],
            "ram": [],
            "psu": [],
            "motherboard": [],
            "storage": []
        }
        total_power_consuption: int = 0

        # Check that each user provided item id exists within the inventory data.
        for item_id in item_id_list:
            id_check = self.inventory_object.get_details(part_id=item_id)
            
            if id_check is None:
                print("id_check failed")
            else:
                # Organize each item by type or organization sake.
                item_key = id_check["item"]
                item_type = item_key["type"].lower()
                
                if item_type != 'psu':
                    total_power_consuption = total_power_consuption + int(item_key["power_draw"])

                if item_type in part_dict:
                    part_dict[item_type].append(item_key)
                else:
                    print(f"Unknown item type: {item_type}")
        
        # Perform a compatibility check again MOTHERBOARD and CPU sockets.
        # Check if there is at least one motherboard and cpu
        clear_screen()
        print(f"Listed Items: {item_id_list}\n")
        if part_dict["motherboard"] and part_dict["cpu"]:
            # Handle the event where there are multiple motherboards to check
            for motherboards in part_dict["motherboard"]:
                # Check compatibility for each CPU if multiple against each motherboard.
                for cpus in part_dict["cpu"]:
                    if motherboards["socket"] != cpus["socket"]:
                        print(f"\n- Motherboard ({motherboards['id']}) and CPU ({cpus['id']}) are not compatible due to different socket types.")
                    else:
                        print(f"\n- Motherboard ({motherboards['id']}) and CPU ({cpus['id']}) are compatible.")
            
        #TODO: 2. Perform check to verify that RAM IDs are the same when placed with a motherboard
        if part_dict["ram"] and part_dict["motherboard"] and len(part_dict["ram"]) >= 2:
            
            # Handle the event where the RAM IDs are not the same.
            first_ram_id = part_dict["ram"][0]["id"]
            ram_check = False
            for ram in part_dict["ram"][1:]:
                if ram["id"] != first_ram_id:
                    ram_check = False
            #TODO: We need to fix this so that if all of the RAM is the same we print a message to the user.
            # With more time I think this would be better.
                    print(f"\n- {first_ram_id} and {ram['id']} do not match. All motherboards require matching RAM.")
                
                    
            # Handle the event where there are multiple motherboards to check
            for motherboard in part_dict["motherboard"]:
                available_ram_slots = motherboard['ram_slots']
                if len(part_dict["ram"]) > available_ram_slots:
                    print(f'\n- Motherboard {motherboard} can\'t support all the {part_dict["ram"]} RAM you provided.')
                else:
                    print(f'\n- Motherboard {motherboard['id']} can support the total number of RAM provided.')
        
        #TODO: 4. Perform a powerdraw check. If more than one PSD is provided just give an error for that check
        if len(part_dict["psu"]) >= 2:
            print("""\n- This compatibility checker only supports 1 instance of a PSU.
                  Please remove additional units and try again.""")
        else:
            available_power_draw = part_dict["psu"][0]["power_supplied"]
            if available_power_draw < total_power_consuption:
                print(f"""\n- Based on the items you input you will max out the PDU's total power supply.
                      {available_power_draw}/{total_power_consuption}\n""")
            else:
                print("\n- The provided PDU can support the total power draw of all the listed items.")            
        