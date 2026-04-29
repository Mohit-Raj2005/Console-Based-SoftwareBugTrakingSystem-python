#reg no:24105129038 MOHIT RAJ




import csv
import os
from datetime import datetime
import pickle

BUG_FILE = "bugs.csv"
USERS_FILE = "users.pkl"
import pickle

USER_FILE = "users.pkl"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "rb") as f:
            return pickle.load(f)
    else:
        users = {
            "tester1": {"role": "Tester","name":"Bob Tester", "assigned_bugs": set()},
            "dev1": {"role": "Developer","name":"Alice Developer", "assigned_bugs": set()},
            "mgr1": {"role": "Manager","name":"Nick Manager", "assigned_bugs": set()}
        }
        save_users(users)
        return users

def save_users(users):
    with open(USER_FILE, "wb") as f:
        pickle.dump(users, f)

users = load_users()


def load_bugs():

    bugs = []

    if not os.path.exists(BUG_FILE):
        return bugs

    with open(BUG_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            bug = {
                "id": int(row.get("id", 0)),
                "title": row.get("title", "").strip(),
                "desc": row.get("desc", "").strip(),
                "priority": int(row.get("priority", 0)),
                "status": row.get("status", "New"),
                "reported_by": row.get("reported_by", ""),
                "assigned_to": row.get("assigned_to", ""),
                "resolution_time": row.get("resolution_time", ""),
                "comments": []
            }
            bugs.append(bug)

    return bugs


def save_bugs(bugs):

    with open(BUG_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer=csv.writer(f)
        writer.writerow(["id", "title", "desc", "priority", "status", "reported_by", "assigned_to", "resolution_time"])
        for b in bugs:
            assigned=b["assigned_to"] if b["assigned_to"] else None
            writer.writerow([b["id"],b["title"],b["desc"],b["priority"],b["status"],b["reported_by"],assigned,b["resolution_time"] ])


#Starting With TESTER ROLE...


#1.REPORT BUG BY TESTER
def report_bug(bugs, user):
    print("\n-- Report a New Bug --")
    title = input("Enter Bug Title: ").strip().title()
    desc = input("Enter Bug Description: ").strip().title()

    while True:
        try:
            priority = int(input("Enter Priority (1–5): "))
            if 1 <= priority <= 5:
                break
            else:
                print("Priority must be between 1 and 5!")
        except Exception as e:
            print("Enter a number between 1 and 5.")

    bug_id = max([b["id"] for b in bugs], default=0) + 1

    new_bug = {
        "id": bug_id,
        "title": title,
        "desc": desc,
        "priority": priority,
        "status": "New",
        "reported_by": user,
        "assigned_to": set(),
        "resolution_time": None,
        "comments": []
    }

    bugs.append(new_bug)
    save_bugs(bugs)
    print(f"\n Bug {bug_id} reported successfully!  Status: New")



#2.VIEW MY BUG BY TESTER
def view_my_bugs(bugs, user):
    print("\n-- My Reported Bugs --")
    my_bugs = [b for b in bugs if b["reported_by"] == user]
    if not my_bugs:
        print("No bugs reported yet.")
        return
    print("+----+------------------------------+----------+-----------+")
    print("| ID | Title                        | Priority | Status    |")
    print("+----+------------------------------+----------+-----------+")
    for b in my_bugs:
        print(f"| {b['id']:<3} | {b['title'][:28]:<28} | {b['priority']:^8} | {b['status']:^9} |")
    print("+----+------------------------------+----------+-----------+")

#3.ADD COMMENT BY TESTER
def add_comment(bugs, user):
    print("\n--- Add Comment ---")

    bug_id = input("Enter Bug ID: ")

    if not bug_id.isdigit():
        print("Invalid ID! Please enter a number.")
        return

    bug_id = int(bug_id)

    bug = None
    for b in bugs:
        if b["id"] == bug_id:
            bug = b
            break

    if bug is None:
        print("Bug not found!")
        return

    comment = input("Enter your comment: ")

    today = datetime.now().strftime("%Y-%m-%d")
    bug["comments"].append((user, today, comment))

    print("Comment added successfully!")


#Next one--> DEVELOPER ROLE....

#1.CLAIM BUG BY DEVELOPER
def claim_bug(bugs, user):
    print("\n--- Claim a Bug ---")
    bug_id = input("Enter Bug ID to claim: ")

    if not bug_id.isdigit():
        print("Invalid Bug ID!")
        return

    bug_id = int(bug_id)
    for b in bugs:
        if b["id"] == bug_id:
            b["assigned_to"] = user
            b["status"] = "Assigned"
            save_bugs(bugs)
            print(f" Bug {bug_id} claimed successfully by {user}.")
            return

    print("Bug not found!")

#2.UPDATE STATUS BY DEVELOPER
def update_status(bugs, user):
    print("\n --- Update Bug Status --- ")
    bug_id = input("Enter Bug ID: ")

    if not bug_id.isdigit():
        print("Invalid Bug ID!")
        return

    bug_id = int(bug_id)
    for b in bugs:
        if b["id"] == bug_id and b["assigned_to"] == user:
            new_status = input("Enter new status : ").strip().title()
            b["status"] = new_status
            save_bugs(bugs)
            print(f" Bug {bug_id} status updated to {new_status}.")
            return

    print("This bug is not assigned to you. Claim it first!!!")

#3.VIEW ASSIGNED BUG BY DEVELOPER
def view_assigned_bugs(bugs, user):
    print("\n--- My Assigned Bugs ---")

    found = False
    print("+----+------------------------------+----------+-----------+")
    print("| ID | Title                        | Priority | Status    |")
    print("+----+------------------------------+----------+-----------+")
    for b in bugs:
        if b["assigned_to"] == user:

            print(f"| {b["id"]:<2} | {b["title"][:28]:<28} | {b["priority"]:^8} | {b["status"]:^9} |")  ########
            print("+----+------------------------------+----------+-----------+")
            found = True

    if not found:
        print("No bugs assigned to you...")


#4.RESOLVE BUG BY DEVELOPER
def resolve_bug(bugs, user):
    print("\n--- Resolve Bug ---")
    bug_id = input("Enter Bug ID: ")

    if not bug_id.isdigit():
        print("Invalid Bug ID!")
        return

    bug_id = int(bug_id)

    bug = None
    for b in bugs:
        if b["id"] == bug_id:
            bug = b
            break

    if bug is None:
        print("Bug not found!")
        return

    if bug["assigned_to"] != user:
        print("This bug is not assigned to you. Claim it first!!!")
        return

    if bug["status"] == "Resolved":
        print("This bug is already resolved.")
        return

    days = input("Enter number of days taken to resolve: ")
    if not days.isdigit():
        print("Please enter a valid number.")
        return

    bug["resolution_time"] = days
    bug["status"] = "Resolved"
    save_bugs(bugs)
    print(f"✓ Bug {bug_id} resolved in {days} days.")




#FROM HERE MANAGER ROLE FUNCTIONS

#1.VIEW DASHBOARD BY MANAGER
def ViewDashboard(bugs, user):
    print("\n--- View Dashboard ---")
    totalbugs = len(bugs)
    print(f"Total Bugs: {totalbugs}")
    openbugs=0
    resolvedbugs=0
    totaldays=0
    OpenbugPercentage=0
    avgResolutionTime=0

    for b in bugs:
        if b["status"] == "New" or b["status"] == "Assigned":
            openbugs += 1
            OpenbugPercentage = openbugs / totalbugs * 100
        if b["status"] == "Resolved":
            resolvedbugs += 1
            totaldays = totaldays + int(b["resolution_time"])
            avgResolutionTime=totaldays / resolvedbugs
    print(f"\nOpen Bugs: {openbugs}({OpenbugPercentage:.2f}%)")
    print(f"Resolved Bugs: {resolvedbugs} (Average resolution time: {avgResolutionTime} days)")
    print("Priority Distribution:",end="")
    bugsPerdev = 0

    for b in bugs:
        print(f"{b["id"]}:{b['priority']}, ",end="")


    print("\nBugs per dev:",end="")
    dev = set()
    for b in bugs:
        dev.add(b["assigned_to"])

    for d in dev:
        for b in bugs:
            if b["assigned_to"] == d:
                bugsPerdev += 1
            else:
                continue

        print(f"{d}:{bugsPerdev} ", end="")
        bugsPerdev = 0








#2.ASSIGN BUG by manager
def assignBug(bugs, user):
    print("\n--- Assign Bug ---")
    bug_id = input("Enter Bug ID to assign: ")
    try:
        bug_id = int(bug_id)
    except Exception as e:
        print("Enter a valid Bug ID!!!")
        return
    found_bug = False
    for b in bugs:
        if b["id"] == bug_id:
                assignee=input("Enter your assignee: ")
                b["assigned_to"]=assignee
                b["status"]="Assigned"
                print(f"The Bug Successfully assigned to {assignee} .")
                save_bugs(bugs)
                found_bug = True
    if not found_bug:
        print("BUG ID NOT FOUND...This bug id doesnot exist yet.!!!")
        return






#3.GENERATE REPORT BY MANAGER
def generate_report(bugs):
    print("\n--- Generate Bug Report ---")
    if not bugs:
        print("No bugs found! Report not generated.")
        return

    os.makedirs("reports", exist_ok=True)
    reportfile = f"reports/bug report {datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(reportfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["ID", "Title", "Priority", "Status", "Reported By", "Assigned To", "Resolution Time", "Comments"])

        for b in bugs:
            comments = "; ".join([f"{u}: {d} - {c}" for (u, d, c) in b.get("comments", [])])
            writer.writerow([
                b["id"], b["title"], b["priority"], b["status"],
                b["reported_by"], b["assigned_to"], b["resolution_time"], comments
            ])

    print(f"Report generated successfully: {reportfile}")


#4 SEARCH BUG BY MANAGER
def searchBug(bugs, user):
    print("\n--- Search Bug ---")
    print("Search by: 1>Status 2>Priority 3>Assignee")
    ch=input("Enter your choice: ")
    if ch=="1":
        status=input("Enter Bug Status(Open / Resolved): ")
        status=status.capitalize()
        if status=="Open":
            print("Opening Bugs...")
            print("+----+------------------------------+----------+-----------+-------------+")
            print("| ID | Title                        | Priority | Status    |Reported By  |")
            print("+----+------------------------------+----------+-----------+-------------+")
            for b in bugs:
                if b["status"] == "Assigned" or b["status"] == "New":
                    print(f"| {b["id"]:<2} | {b["title"][:28]:<28} | {b["priority"]:^8} | {b["status"]:^9} | {b["reported_by"]:^9} |")
                    print("+----+------------------------------+----------+-----------+-------------+")
        elif status=="Resolved":
            print("Resolved Bugs...")
            print("+----+------------------------------+----------+-----------+-------------+")
            print("| ID | Title                        | Priority | Status    |Reported By  |")
            print("+----+------------------------------+----------+-----------+-------------+")

            for b in bugs:
                if b["status"] == "Resolved":
                    print(f"| {b["id"]:<2} | {b["title"][:28]:<28} | {b["priority"]:^8} | {b["status"]:^9} | {b["reported_by"]:^9} |")
                    print("+----+------------------------------+----------+-----------+-------------+")
        else:
            print("Enter a valid status as stated above!!!")
            return
    elif ch=="2":
        priority=input("Enter priority: ")
        try:
            priority=int(priority)
        except Exception as e:
            print("Please enter a valid number!!!")
            return
        print("+----+------------------------------+----------+-----------+-------------+")
        print("| ID | Title                        | Priority | Status    |Reported By  |")
        print("+----+------------------------------+----------+-----------+-------------+")
        found=False
        for b in bugs:
            if b["priority"] == priority:
                print(f"| {b["id"]:<2} | {b["title"][:28]:<28} | {b["priority"]:^8} | {b["status"]:^9} | {b["reported_by"]:^9} |")
                print("+----+------------------------------+----------+-----------+-------------+-------------+")

                continue
            # else:
            #     print("Priority not found!")
            #     return

            # else:
            #     continue

    elif ch=="3":
            assignee=input("Enter assignee: ")
            found = False
            print("+----+------------------------------+----------+-----------+-------------+-----------+")
            print("| ID | Title                        | Priority | Status    |Reported By  | Assignee  |")
            print("+----+------------------------------+----------+-----------+-------------+-----------+")

            for b in bugs:
                if assignee in b["assigned_to"] :
                    print(f"| {b["id"]:<2} | {b["title"][:28]:<28} | {b["priority"]:^8} | {b["status"]:^9} | {b["reported_by"]:^9}   | {b["assigned_to"]}")
                    print("+----+------------------------------+----------+-----------+-------------+-------------+")
                    found = True
            if not found :
                print("Assignee not found!")
                return
    else:
        print("Please enter a valid number!!!")
        return





def login():
    print("=== Welcome to Software Bug Tracking System ===")
    while True:
        print("\nAvailable users:")
        for u, info in users.items():
            print(f" - {u} ({info['role']})")
        role = input("\nEnter your role (Tester/Developer/Manager): ").strip()
        username = input("\nLogin As: ").strip()
        if username in users:
            print(f" Logged in as {username} ({users[username]['role']})")
            return username , users[username]["role"]
        else:
            print(" Invalid username! Try again.")


def main():
    bugs = load_bugs()
    while True:
        username, role = login()
        if role == "Tester":

            while True:
                print("\n--- TESTER MENU ---")
                print("1. Report Bug\n2. View My Bugs\n3. Add Comment\n4. Save & Logout")
                ch = input("Enter choice: ")
                if ch == "1":
                    report_bug(bugs,username)
                elif ch == "2":
                    view_my_bugs(bugs,username)
                elif ch == "3":
                    add_comment(bugs,username)
                elif ch == "4":
                    save_bugs(bugs)
                    save_users(users)
                    print("Saved And Logged out.")
                    break
                else:
                    print("Invalid choice!")

        elif role=="Developer":

            while True:
                print("\n = = = DEVELOPER MENU = = =")
                print("1. Claim Bug\n2. Update Status\n3. View Assigned Bugs\n4. Resolve Bug\n5. Logout")
                ch = input("Enter choice: ")
                if ch == "1":
                    claim_bug(bugs, username)
                elif ch == "2":
                    update_status(bugs, username)
                elif ch == "3":
                    view_assigned_bugs(bugs, username)
                elif ch == "4":
                    resolve_bug(bugs, username)
                elif ch == "5":
                    save_bugs(bugs)
                    save_users(users)
                    print(" Logged out...")
                    break
                else:
                    print("Invalid choice!")
            continue

        elif role=="Manager":
            while True:
                print("\n = = = MANAGER MENU = = =")
                print("1.View Dashboard \n 2. Assign Bug  \n 3.Generate Report \n 4. Search Bugs \n 5. Save & Logout")
                ch=input("Enter choice: ")
                if ch == "1":
                    ViewDashboard(bugs, username)
                elif ch == "2":
                    assignBug(bugs, username)
                elif ch == "3":
                    generate_report(bugs)
                elif ch == "4":
                    searchBug(bugs, username)
                elif ch == "5":
                    save_bugs(bugs)
                    save_users(users)
                    print(" Saved and logged out")
                    break
                else:
                    print("Invalid choice!")
            continue



if __name__ == "__main__":
        main()
