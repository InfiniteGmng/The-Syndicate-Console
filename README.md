I need you to create a json file with 2 main objects. The objects should be called "Total Points" and "Weekly Contributors". The "Total Points" object should contain "Player" objects that have fields of their name (Name:), their total points (Score:), whether or not they're still active (Active:), and the week they joined the alliance (Week Joined:). That object should be ordered by names alphabetically (a-z). Now the "Weekly Contributors" object should have "Week #" objects inside. These week objects should have fields of player names and those fields should have how many points they got that week. The "Week" objects should also be sorted numerically (1 being first, then 2, etc.).

Here is the format for the json file: "./template.json"

Ok so I want you to write a python console menu script for my Marvel Snap Alliance called "The Syndicate" that gives me Menu 1: 1. Weeks, 2. Players, 3. Commands, 4. Exit. Every menu should be able to be controlled by either inputing the number associated with the option or by inputing the name (value) of the option. When the user makes a choice other than "Exit", after the function is done, don't stop the program, but bring back Menu 1. This way the script stays running until they exit out of it. Please write this in parts, when you finish one part, stop and ask me to move on and etc. The script should load this file path="./TheSyndicate.json" and use the data inside. The script's purpose is to update this json file with new data.

- The script starts and runs Menu 1, which has 4 functions (Weeks, Players, Points, and Exit).

- Weeks opens up Menu 2, which has 4 functions (Create, Update, Delete, and Exit).

- Players opens up Menu 3, which has 4 functions (Add, Modify, Delete, and Exit).

- Commands opens up Menu 4, which has 5 functions (Total, Week, Player, Status, and Exit).

- Delete opens up Menu 5, which has 2 functions (Confirm and Cancel).

- Modify opens up Menu 6, which has 5 functions (Name, Total Points, Week Joined, Active, and Exit).

This console should be modular, where each Menu pulls functions to use in the needed menu. For example, "Exit" is an option included in most menus, it should always be the last option in the menu it's in, and it should just call the "Exit" function. "Delete" is another function used by multiple menus, but does something different depending on which Menu you use it in.

1. Weeks: This should give the user another menu (Menu 2) with the following options: 1. Create, 2. Update, 3. Delete, and 4. Exit. If the user chooses 1: it should create a new "Week" object (i.e. Week 1, Week 2) and it should automatically add this object with the next highest number (i.e. if the previous week was 12, then add Week 13. You need to make a variable (currentWeek) that permanently stores a number starting at 0, then updates this variable by +1 each time a week is created) then give a confirmation message to the user with what week it added. If the user chooses option 2: it should ask the user for a week number and save that input to a variable called "userWeek", the user must enter a number (i.e. 1, 2, 3 etc.) and then it should give me the name of a single active player (ordered alphabetically (a-z)) and ask for a point value. Then the user will enter a point value, and that value should be added to that player's "Points:" field for the inputed week (userWeek). If that player's point value is anything other than 0, ask for confirmation from the user before updating the player's point value. If that player's point value is 0, update it with the new point value. Once that happens, loop through this for every active player, making sure the "check" happens for each player.

2. Players: This should give a menu (Menu 3) with these options: 1. Add, 2. Modify, 3. Delete, 4. Exit. For option 1, this should create a new "Player" object (into the "Total Points" object) with a default "Score:" value of 0, a boolean field of "Active": true, and it should ask the user for a "Name:" string and "Week Joined:" number. If a player already has that name value, it should throw an error message telling the user, and give Menu 3 again instead. For option 2, this should give the user a numerical list of all player names (sorted alphabetically) and ask the user for an input. Then, store that input (either the number or name) in a variable (userInput) and give the user Menu 6.

3. Commands: This should give a menu (Menu 4) with these options: 1. Total, 2. Week, 3. Player, 4. Status, 5. Exit. Option 1 should add the total of each player's points from each week. This should be done by summing the value of all "Week" keys, updating the "Score" field in the player objects with the new value, and saving this data back to the original file ("TheSyndicate.json"). Option 2 should ask the user for a week number, which should be saved to the "userWeek" variable, then it should print out that week object to the console. Option 3 should ask the user for a player "Name", which should be saved to a "userName" variable, then it should print out that player object to the console. Option 4 should print out a list of all players (just their names) and sort them into 2 sections labled "Active" and "Inactive" depending on the player's "Active:" value (true=active and false=inactive).

If the user selects "Delete": it should check which menu it's in (either Weeks or Players), if in "Players", give the user a numerical list of all player names (sorted alphabetically) and ask the user for an input. Then, using that input (either the number or name), it should send the user a confirmation message, printing out that object (either Week or Player depending on "currentMenu") to the console, and give the user Menu 5. If Menu 5 continues, delete/remove that entire object (either Week or Player depending on "currentMenu") from the json file. And if it's in "Weeks", ask the user for a week number, the user will enter a number (i.e. 1, 2, 3 etc.), then it should send the user a confirmation message, printing out that object (either Week or Player depending on "currentMenu") to the console, and give the user Menu 5. If Menu 5 continues, delete/remove that entire object (either Week or Player depending on "currentMenu") from the json file.

If the user selects "Exit": It should close and end the python script.

Menu 5 has these choices: 1. Confirm and 2. Cancel. Option 1 confirms the choice and lets the function continue, while option 2 stops the current function and gives the user Menu 1 again.

Menu 6 has these choices: 1. Name, 2. Total Points, 3. Week Joined, 4. Active, and 5. Exit. Options 1, 2, 3, and 4 all let the user change that field in the inputed "Player" object. It asks the user what they want to change the value to, then it takes that input and updates the object. If the user inputs an invalid data type, throw an error message and give Menu 6 again. Make sure if this happens that the "userInput" variable doesn't get reset.

After the user is prompted for a week number, ask the user what data they want to view. If the user enters "all/a/0" give them all the data from that week object (this is what it does currently without asking what data). If the user says, "top/t #" (#=a number, stored in a user_count var), give the user_week with only the first user_count number of players from that week (make sure week is ordered highest points first). If the user says, "bottom/b #" give the user_week with only the last user_count number of players from that week (it should give the user_count lowest point players from that week). If the user inputs a negative number for user_count, this should "invert" the order of which players it gives. For example if the user inputs "t 3" it should give the 3 highest point players from that week, but if the user inputs "t -3" it should give the 3 lowest point players from that week.

# ADD THIS -> Make sure all functions have catches for negative numbers.

# ADD THIS -> Add a way to update a players points per week not just score

# MAYBE ADD THIS -> If the user updates the Active field, it should prompt the user for week_kicked. If the user inputs "current/c" make the week_kicked = current_week.
