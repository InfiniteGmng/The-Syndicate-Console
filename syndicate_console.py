import json
import os

# Path to the JSON file
JSON_PATH = "./TheSyndicate.json"

# Loads the JSON data from the file.
def load_data():
    default_data = {
        "Current Week": 1,
        "Total Points": [],
        "Weekly Contributors": {}
    }

    if not os.path.exists(JSON_PATH) or os.stat(JSON_PATH).st_size == 0:
        with open(JSON_PATH, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data

    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        with open(JSON_PATH, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data

    for key, value in default_data.items():
        if key not in data:
            data[key] = value

    global current_week
    current_week = data.get("Current Week", 1)

    # NOT CURRENTLY WORKING
    if isinstance(data["Weekly Contributors"], dict):
        for week_key, week_data in data["Weekly Contributors"].items():
            if not isinstance(week_data, list):
                data["Weekly Contributors"][week_key] = [
                    {"Name": player["Name"], "Points": player["Points"]} for player in week_data
                ]
    return data


# Saves the JSON data to the file, sorting players and weekly contributors.
def save_data(data):
    formatted_weekly_contributors = {} # NOT CURRENTLY WORKING
    
    # NOT CURRENTLY WORKING
    for week_key, week_data in data["Weekly Contributors"].items():
        if isinstance(week_data, list):
            formatted_weekly_contributors[week_key] = [
                {"Name": player["Name"], "Points": player["Points"]} for player in week_data
            ]
        else:
            formatted_weekly_contributors[week_key] = week_data

    data["Weekly Contributors"] = formatted_weekly_contributors

    data["Total Points"].sort(key=lambda player: player["Score"], reverse=True)
    
    sorted_weeks = {}
    for week_key in sorted(data["Weekly Contributors"], key=lambda wk: int(wk.split()[1])):
        sorted_weeks[week_key] = sorted(
            data["Weekly Contributors"][week_key],
            key=lambda contributor: contributor["Points"],
            reverse=True
        )
    data["Weekly Contributors"] = sorted_weeks

    data["Current Week"] = current_week

    with open(JSON_PATH, 'w') as f:
        json.dump(data, f, indent=4)


# Main menu for the Syndicate console.
def main_menu():
    options = {
        "1": "Weeks",
        "2": "Players",
        "3": "Commands",
        "4": "Time",
        "5": "Exit"
    }
    while True:
        print("\nMain Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nChoose an option: ").strip()
        
        # Matches the input to the appropriate option
        if choice.lower() == "e":
            action = "Exit"
        elif choice in options:
            action = options[choice]
        elif choice.capitalize() in options.values():
            action = choice.capitalize()
        else:
            print("\nInvalid input, please try again.")
            continue

        data = load_data()
        
        # Runs the Week Menu function.
        if action == "Weeks":
            week_menu()

        # Runs the Player Menu function.
        elif action == "Players":
            player_menu()

        # Runs the Command Menu function.
        elif action == "Commands":
            command_menu()

        # Runs the Time Menu function.
        elif action == "Time":
            time_menu(data)

        # Ends the script.
        elif action == "Exit":
            print("\nExiting the Syndicate console. Goodbye!")
            break


# Menu for managing weeks.
def week_menu():
    global current_week
    options = {
        "1": "Create",
        "2": "Update",
        "3": "Delete",
        "4": "Exit"
    }
    while True:
        print("\nWeek Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nChoose an option: ").strip()

        # Matches the input to the appropriate option
        if choice.lower() == "e":
            action = "Exit"
        elif choice in options:
            action = options[choice]
        elif choice.capitalize() in options.values():
            action = choice.capitalize()
        else:
            print("\nInvalid input, please try again.")
            continue

        data = load_data()

        # Runs the Create Week function.
        if action == "Create":
          create_week(data)

        # Updates an existing week.
        elif action == "Update":
            user_week = input("\nEnter the week number to update: ").strip()
            try:
                week_key = f"Week {int(user_week)}"
                if week_key not in data["Weekly Contributors"]:
                    print(f"\nWeek {user_week} does not exist.")
                    continue
                print(f"\nUpdating {week_key}...")
                update_points(data, week_key)
            except ValueError:
                print("\nInvalid week number. Please enter a valid number.")

        # Deletes an existing week.
        elif action == "Delete":
            user_week = input("\nEnter the week number to delete: ").strip()
            try:
                week_key = f"Week {int(user_week)}"
                if week_key not in data["Weekly Contributors"]:
                    print(f"\nWeek {user_week} does not exist.")
                    continue
                confirm_delete(data, week_key, "Weekly Contributors")
            except ValueError:
                print("\nInvalid week number. Please enter a valid number.")

        # Ends the script.
        elif action == "Exit":
            break


# Creates a new week object.
def create_week(data):
    global current_week
    week_key = f"Week {current_week}"

    if not data["Total Points"]:
        print("\nError: Cannot create week, no players found.")
        return
    
    new_week = []
    for player in data["Total Points"]:
        if (player.get("Active", False) and player.get("Week Joined") <= current_week) or \
           (not player.get("Active", False) and player.get("Week Joined") <= current_week and player.get("Week Kicked") >= current_week):
            new_week.append({
                "Name": player["Name"],
                "Points": 0
            })

    if not new_week:
        print("\nError: No eligible players found.")
        return
    
    data["Weekly Contributors"][week_key] = new_week
    current_week += 1
    save_data(data)
    print(f"\nCreated '{week_key}' with {len(new_week)} players.")


# Updates points for all players in the specified week.
def update_points(data, week_key):
    week_data = data["Weekly Contributors"].get(week_key, [])
    eligible_players = [
        p for p in data["Total Points"]
        if any(player["Name"] == p["Name"] for player in week_data)
    ]
    eligible_players.sort(key=lambda p: p["Name"])

    if week_key not in data["Weekly Contributors"]:
        print(f"\nError: {week_key} does not exist.")
        return

    week_data = data["Weekly Contributors"][week_key]

    for player in eligible_players:
        name = player["Name"]
        week_player = next((p for p in week_data if p["Name"] == name), None)
        
        if not week_player:
            continue
        
        current_points = week_player["Points"]
        print(f"\nCurrent points for {name}: {current_points}")
        
        new_points = confirm_update(player, current_points)
        
        if new_points is not None:
            week_player["Points"] = new_points

    save_data(data)
    print(f"\nPoints updated for {week_key}.")


# Helper function to ask for new points and confirmation.
def confirm_update(player, current_points):
    while True:
        new_points = input(f"Enter new points for {player['Name']}: ").strip()

        if new_points == "-" or int(new_points) < 0:
            print(f"\nSkipping {player['Name']}...")
            return None

        try:
            new_points = int(new_points)

            if current_points != 0:
                confirm = input(f"\nAre you sure you want to update {player['Name']}'s points from {current_points} to {new_points}? (yes/no): ").strip().lower()
                if confirm in ["yes", "y"]:
                    return new_points
                elif confirm in ["no", "n"]:
                    continue
                else:
                    print("\nInvalid input. Please respond with 'yes' or 'no'.")
            else:
                return new_points

        except ValueError:
            print("\nInvalid input. Please enter a valid number for points.")


# Helper function to handles delete confirmation.
def confirm_delete(data, key, menu_name):
    confirm = input(f"\nAre you sure you want to delete '{key}'? (yes/no): ").strip().lower()

    if confirm in ["yes", "y"]:
        if menu_name == "Weekly Contributors":
            del data["Weekly Contributors"][key]
        elif menu_name == "Total Points":
            data["Total Points"] = [p for p in data["Total Points"] if p["Name"] != key]
        save_data(data)
        print(f"\n'{key}' has been deleted.")
    else:
        print(f"\n'{key}' was not deleted.")


# Menu for managing players.
def player_menu():
    options = {
        "1": "Add",
        "2": "Modify",
        "3": "Delete",
        "4": "Exit"
    }
    while True:
        print("\nPlayer Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nChoose an option: ").strip()

        # Matches the input to the appropriate option
        if choice.lower() == "e":
            action = "Exit"
        elif choice in options:
            action = options[choice]
        elif choice.capitalize() in options.values():
            action = choice.capitalize()
        else:
            print("\nInvalid input, please try again.")
            continue

        data = load_data()

        # Runs the Add Player function.
        if action == "Add":
            add_player(data)

        # Runs the Modify Player function.
        elif action == "Modify":
            modify_player(data)

        # Runs the Delete Player function.
        elif action == "Delete":
            delete_player(data)

        # Ends the script.
        elif action == "Exit":
            break


# Adds a new player.
def add_player(data):
    global current_week
    name = input("\nEnter the player's name: ").strip()

    if any(player["Name"].lower() == name.lower() for player in data["Total Points"]):
        print(f"\nPlayer '{name}' already exists.")
        return

    try:
        week_joined = int(input("\nEnter the week the player joined: ").strip())
        if week_joined < 0:
            week_joined = None
        elif week_joined - 1 > current_week:
            print(f"\nInvalid week number. The current week is {current_week}.")
            return
    except ValueError:
        print("\nInvalid input. Please enter a valid number for the week.")
        return

    # Create new player object
    new_player = {
        "Name": name,
        "Score": 0,
        "Active": True,
        "Week Joined": week_joined,
        "Week Kicked": None
    }

    data["Total Points"].append(new_player)
    save_data(data)
    print(f"\nAdded new player: {name}")


# Modifies a player's details.
def modify_player(data):
    players = sorted(data["Total Points"], key=lambda p: p["Name"])
    if not players:
        print("\nNo players to modify.")
        return

    print("\nList of Players:")
    for i, player in enumerate(players, start=1):
        print(f"{i}. {player['Name']}")

    choice = input("\nEnter the name of the player to modify: ").strip()

    try:
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(players):
                user_input = players[index]
            else:
                print("\nInvalid choice. Please try again.")
                return
        else:
            user_input = next((p for p in players if p["Name"].lower() == choice.lower()), None)
            if not user_input:
                print("\nPlayer not found. Please try again.")
                return
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return

    print(f"\nSelected Player: {user_input}")
    modify_menu(data, user_input)


# Deletes a player.
def delete_player(data):
    players = sorted(data["Total Points"], key=lambda p: p["Name"])
    if not players:
        print("\nNo players to delete.")
        return

    print("\nList of Players:")
    for i, player in enumerate(players, start=1):
        print(f"{i}. {player['Name']}")

    choice = input("\nEnter the name of the player to delete: ").strip()

    try:
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(players):
                player_to_delete = players[index]
            else:
                print("\nInvalid choice. Please try again.")
                return
        else:
            player_to_delete = next((p for p in players if p["Name"].lower() == choice.lower()), None)
            if not player_to_delete:
                print("\nPlayer not found. Please try again.")
                return
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return

    confirm_delete(data, player_to_delete["Name"], "Total Points")


# Menu for modifying a player's details.
def modify_menu(data, player):
    global current_week
    options = {
        "1": "Name",
        "2": "Score",
        "3": "Active",
        "4": "Week Joined",
        "5": "Week Kicked",
        "6": "Exit"
    }
    while True:
        print("\nModify Player Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nChoose an option: ").strip()

        # Matches the input to the appropriate option
        if choice.lower() == "e":
            action = "Exit"
        elif choice in options:
            action = options[choice]
        elif choice.capitalize() in options.values():
            action = choice.capitalize()
        else:
            print("\nInvalid input, please try again.")
            continue

        # Updates the Name of a player.
        if action == "Name":
            new_name = input("\nEnter the new name: ").strip()
            if not new_name:
                print("\nName cannot be empty.")
                continue
            # Check for duplicate names
            if any(p["Name"].lower() == new_name.lower() for p in data["Total Points"] if p != player):
                print("\nA player with that name already exists. Please choose a different name.")
                continue
            
            old_name = player["Name"]
            player["Name"] = new_name

            # Update the player's name in all weeks
            for week_key, players in data["Weekly Contributors"].items():
                for week_player in players:
                    if week_player["Name"] == old_name:
                        week_player["Name"] = new_name

            print(f"\nPlayer name updated from {old_name} to {new_name}.")

        # Runs the Update Score function.
        elif action == "Score":
            update_score(data, player)
            
        # Changes an existing player's status.
        elif action == "Active":
            active_status = input("\nIs the player active? (yes/no): ").strip().lower()
            if active_status in ["yes", "y"]:
                player["Active"] = True
            elif active_status in ["no", "n"]:
                player["Active"] = False
                if player.get("Week Kicked") is None:
                    player["Week Kicked"] = current_week - 1
            else:
                print("\nInvalid input. Please enter 'yes' or 'no'.")
                continue
            
        # Changes an existing player's join date.
        elif action == "Week Joined":
            try:
                new_week = int(input("\nEnter the new week joined: ").strip())

                if new_week - 1 > current_week or new_week <= 0:
                    print(f"\nInvalid week number. Current week: ({current_week})")
                    continue

                player["Week Joined"] = new_week
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                continue
            
        # Changes an existing player's kick date.
        elif action == "Week Kicked":
            try:
                new_week_kicked_input = input("\nEnter the new week kicked: ").strip()

                if new_week_kicked_input.lower() in ["none", "null"] or new_week_kicked_input.startswith("-") or not new_week_kicked_input:
                    new_week_kicked = None
                else:
                    new_week_kicked = int(new_week_kicked_input)
                    if new_week_kicked > current_week or new_week_kicked < player.get("Week Joined"):
                        print(f"\nInvalid week number. Current week: ({current_week})")
                        continue

                player["Week Kicked"] = new_week_kicked
                save_data(data)
                if new_week_kicked is None:
                    print("\nWeek Kicked has been set to None.")
                else:
                    print(f"\nWeek Kicked has been updated to Week {new_week_kicked}.")
            except ValueError:
                print("\nInvalid input. Please enter a valid number, 'None', or 'Null'.")
                continue
            
        # Ends the script.
        elif action == "Exit":
            break

        save_data(data)
        print(f"\nUpdated player: {player}")


# Updates a player's points for a specific week.
def update_score(data, player):
    try:
        # Ask the user for a week
        user_week = input("\nEnter the week number to modify: ").strip()
        week_key = f"Week {int(user_week)}"
        
        if week_key not in data["Weekly Contributors"]:
            print(f"\nWeek {user_week} does not exist.")
            return
        
        # Confirm the player is in the selected week
        week_data = data["Weekly Contributors"][week_key]
        player_in_week = next((p for p in week_data if p["Name"].lower() == player["Name"].lower()), None)

        if not player_in_week:
            print(f"\nPlayer {player['Name']} is not listed in Week {user_week}.")
            return

        # Ask for the new score
        print(f"\nCurrent points for Week {user_week}: {player_in_week['Points']}")
        new_score = int(input("Enter the new points: ").strip())
        if new_score < 0:
            new_score = 0

        # Update the player's score in the specified week
        player_in_week["Points"] = new_score
        print(f"\n{player_in_week['Name']}'s points for {week_key} have been updated to {new_score}.")

        # Recalculate the total points
        score_calculator(data)

        # Save the updated data
        save_data(data)
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


# Menu for viewing the JSON file data.
def command_menu():
    options = {
        "1": "Total",
        "2": "Week",
        "3": "Player",
        "4": "Status",
        "5": "Exit"
    }
    while True:
        print("\nCommand Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nChoose an option: ").strip()
        
        # Matches the input to the appropriate option
        if choice.lower() == "e":
            action = "Exit"
        elif choice in options:
            action = options[choice]
        elif choice.capitalize() in options.values():
            action = choice.capitalize()
        else:
            print("\nInvalid input, please try again.")
            continue

        data = load_data()

        # Prints the total points for each player across all weeks.
        if action == "Total":
            # Calculate scores for all players
            score_calculator(data)

            # Separate active and inactive players, and sort by total points (descending)
            active_players = sorted(
                [p for p in data["Total Points"] if p["Active"]],
                key=lambda p: p["Score"],
                reverse=True
            )
            inactive_players = sorted(
                [p for p in data["Total Points"] if not p["Active"]],
                key=lambda p: p["Score"],
                reverse=True
            )

            # Print active players
            print("\nActive Players:")
            if active_players:
                for player in active_players:
                    print(f" - {player['Name']}: {player['Score']}")
            else:
                print("  No active players found.")

            # Print inactive players
            print("\nInactive Players:")
            if inactive_players:
                for player in inactive_players:
                    print(f" - {player['Name']}: {player['Score']}")
            else:
                print("  No inactive players found.")

            # Save the updated data
            save_data(data)
            print("\nTotal points updated for all players.")

        # Runs the View Week function.
        elif action == "Week":
          view_week(data)

        # Prints out a specific player to view.
        elif action == "Player":
            user_name = input("\nEnter the player's name: ").strip()
            player = next((p for p in data["Total Points"] if p["Name"].lower() == user_name.lower()), None)

            if player:
                print(f"\nName: {player['Name']}")
                print(f"Total Points: {player['Score']}")
                print(f"Active: {'Yes' if player['Active'] else 'No'}")
                print(f"Week Joined: {player['Week Joined']}")
                print(f"Week Kicked: {player.get('Week Kicked', 'None')}")
            else:
                print(f"\nPlayer '{user_name}' not found.")
          
        # Prints out a list of all players.
        elif action == "Status":
            active_players = sorted(
                [p for p in data["Total Points"] if p["Active"]],
                key=lambda p: p["Score"],
                reverse=True
            )
            inactive_players = sorted(
                [p for p in data["Total Points"] if not p["Active"]],
                key=lambda p: p["Score"],
                reverse=True
            )

            # Print active players
            print("\nActive Players:")
            if active_players:
                for player in active_players:
                    print(f" - {player['Name']}")
            else:
                print(" - None")

            # Print inactive players
            print("\nInactive Players:")
            if inactive_players:
                for player in inactive_players:
                    print(f" - {player['Name']}")
            else:
                print(" - None")

        # Ends the script.
        elif action == "Exit":
            break


# Calculates and updates the score for each player.
def score_calculator(data):
    for player in data["Total Points"]:
        total_points = sum(
            contributor["Points"]
            for week in data["Weekly Contributors"].values()
            for contributor in week
            if contributor["Name"].lower() == player["Name"].lower()
        )
        player["Score"] = total_points

    # Sort the players by total score and update the data
    data["Total Points"] = sorted(data["Total Points"], key=lambda p: p["Score"], reverse=True)


# Prints out a specific week and players to view.
def view_week(data):
    user_week = input("\nEnter the week number to view: ").strip()
    try:
        week_key = f"Week {int(user_week)}"
        if week_key in data["Weekly Contributors"]:
            data_choice = input("\nWhat players would you like to view: ").strip().lower()

            # Sort by points descending by default
            week_data = sorted(
                data["Weekly Contributors"][week_key],
                key=lambda player: player["Points"],
                reverse=True
            )

            # Show all data
            if data_choice in ["all", "a", "0"]:
                print(f"\n- {week_key}")
                for player in week_data:
                    print(f"  {player['Name']}: {player['Points']}")
            
            # Show top players
            elif data_choice.startswith("top") or data_choice.startswith("t"):
                try:
                    user_count = int(data_choice.split()[-1])
                    if user_count < 0:
                        user_count = abs(user_count)
                        week_data = sorted(week_data, key=lambda player: player["Points"])
                        print(f"\n- {week_key} (Bottom {user_count} Players)")
                    else:
                        print(f"\n- {week_key} (Top {user_count} Players)")
                    for player in week_data[:user_count]:
                        print(f"  {player['Name']}: {player['Points']}")
                except (ValueError, IndexError):
                    print("\nInvalid input for 'top'. Please use 'top #' format.")

            # Show bottom players
            elif data_choice.startswith("bottom") or data_choice.startswith("b"):
                try:
                    user_count = int(data_choice.split()[-1])
                    if user_count < 0:
                        user_count = abs(user_count)
                        week_data = sorted(week_data, key=lambda player: player["Points"])
                        print(f"\n- {week_key} (Top {user_count} Players)")
                    else:
                        print(f"\n- {week_key} (Bottom {user_count} Players)")
                    for player in week_data[-user_count:]:
                        print(f"  {player['Name']}: {player['Points']}")
                except (ValueError, IndexError):
                    print("\nInvalid input for 'bottom'. Please use 'bottom #' format.")
            else:
                print("\nInvalid choice. Please use 'all', 'top', or 'bottom'.")
        else:
            print(f"\nWeek {user_week} does not exist.")
    except ValueError:
        print("\nInvalid week number. Please enter a valid number.")


# Menu for managing the current week.
def time_menu(data):
    global current_week
    options = {
        "1": "View",
        "2": "Adjust",
        "3": "Exit"
    }
    while True:
        print("\nTime Menu:")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nChoose an option: ").strip()
        
        # Matches the input to the appropriate option
        if choice.lower() == "e":
            action = "Exit"
        elif choice in options:
            action = options[choice]
        elif choice.capitalize() in options.values():
            action = choice.capitalize()
        else:
            print("\nInvalid input, please try again.")
            continue
        
        # Prints out the current week.
        if action == "View":
            print(f"\nThe current week is: {current_week}")
            continue

        # Updates the current_week variable
        elif action == "Adjust":
            try:
                print(f"\nThe current week is: {current_week}")
                new_current = int(input("Enter the new Current Week: ").strip())
                if new_current < 1:
                    print("\nError: Current Week must be a positive integer.")
                    continue
                if any(new_current < player["Week Joined"] for player in data["Total Points"]):
                    print("\nError: New week cannot be earlier than any player's join week.")
                    continue

                current_week = new_current
                data["Current Week"] = current_week
                save_data(data)
                print(f"\nCurrent Week successfully updated to {current_week}.")
            except ValueError:
                print("\nInvalid input. Please enter a valid integer.")

        # Ends the script.
        elif action == "Exit":
            break


if __name__ == "__main__":
    main_menu()
