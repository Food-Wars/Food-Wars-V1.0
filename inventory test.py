# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:52:31 2024

"""
#crafting slot 10
if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
     if inventory.slots[f'slot_{num}'][2] == 0:
         crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
         crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
         self.crafted = True
elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
       if item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
           pass
       else:
           crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
           crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]
           self.crafted = True


#normal
if inventory.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
     if inventory.slots[f'slot_{num}'][2] == 0:
        if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
            inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
            inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
            if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
        else:
           inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
           inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
     else:
        inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
        inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
elif inventory.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
       if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.slots[f'slot_{num}'][2])][2] == True:
          inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
          if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
              inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
       elif item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
            inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
            inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
       else:
           inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
           inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]