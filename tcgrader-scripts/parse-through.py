import json
from collections import Counter
import csv
import os

def process_card_data(json_data):
    # Parse the JSON data
    data = json.loads(json_data)
    
    # Initialize sets and counters
    users = set()
    grade_frequencies = Counter()
    grade_10_cards = []
    
    # Process each card in the cards array
    for card in data.get("cards", []):
        # Extract user information
        if "user" in card and "_id" in card["user"] and "name" in card["user"]:
            user_id = card["user"]["_id"]
            user_name = card["user"]["name"]
            users.add((user_id, user_name))
        
        # Extract overall final grade if it exists
        try:
            final_grade = card["grades"]["overall"]["final"]
            grade_frequencies[final_grade] += 1
            
            # Save cards with grade 10
            if final_grade == 10:
                grade_10_cards.append(card)
        except (KeyError, TypeError):
            # Skip if the grade structure doesn't exist
            continue
    
    return users, grade_frequencies, grade_10_cards

def main():
    # For testing, you can replace this with file input
    json_input = open('bros-entire-database.json', 'r').read()
    
    # Process the data
    users, grade_frequencies, grade_10_cards = process_card_data(json_input)
    
    # Write users to CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'users.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['User ID', 'User Name'])  # Header
        for user_id, user_name in users:
            csv_writer.writerow([user_id, user_name])
    print(f"\nUsers exported to {csv_path}")
    
    # Write grade frequencies to CSV file
    grade_freq_path = os.path.join(os.path.dirname(__file__), 'grade-frequency.csv')
    with open(grade_freq_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Grade', 'Count'])  # Header
        for grade, count in grade_frequencies.items():
            csv_writer.writerow([grade, count])
    print(f"Grade frequencies exported to {grade_freq_path}")
    
    # Save cards with grade 10 to JSON file
    if grade_10_cards:
        grade_10_path = os.path.join(os.path.dirname(__file__), 'cards-with-grade-10.json')
        with open(grade_10_path, 'w') as jsonfile:
            json.dump(grade_10_cards, jsonfile, indent=2)
        print(f"Cards with grade 10 exported to {grade_10_path}")

if __name__ == "__main__":
    main()