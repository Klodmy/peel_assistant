import csv
import json
import re
from datetime import date



def main():

    # creates two lists - Assignments and Reports
    try:
        list_a = load_csv("A.csv")
        list_r = load_csv("R.csv")
    except:
        raise ValueError("Check files. Assignments should be named A, Contractor Reports should be named R.")

    # creates a list of work order numbers from assignments
    list_of_wos = assignments_wo(list_a)

    # creates the list of dicts of reports that has no additional assignments on their work order numbers
    list_completed = to_invoice(list_of_wos, list_r)

    # makes a formated list of dicts
    formated_completed = format(list_completed)

    # sorts by headers
    final = final_sort(formated_completed)

    # writes proper CSV
    write_csv(final, f"To invoice {date.today()}.csv")



# loads dictionaries to a list
def load_csv(filepath):
    with open(filepath, newline='', encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))



# creates a list of work order numbers from assignments
def assignments_wo(l):
    wo_list = []
    for r in l:
        wo_list.append(r["Work Order ID"])
    return wo_list




# formats problem codes to eliminate ones w/o descriptions
def problem_code(code):
    
    allowed = [
        "222307 - SANITARY MAINTENANCE HOLE REHA",
        "51004 - FLAT RATE TURN ON/OFF (COPPER)",
        "51103 - WATERMAIN BREAK REPAIR (C_UT)",
        "51104 - WATERMAIN FLUSHING",
        "51108 - WATERMAIN COMPLAINT INVEST.",
        "51303 - WATER VALVE REPAIRS",
        "51304 - WATER VALVE BOX REPAIRS",
        "51305 - WATER VALVE INSTALL/REPLACE",
        "51307 - WATER VALVE CHAMB REP",
        "51503 - WATER HYDRANT REPAIRS",
        "51504 - WATER HYDRANT INST/REPL/REMOV",
        "51702- W/S REPLACEMENT",
        "51703 - WATER SERVICE REPAIR",
        "51704 - WATER SERVICE BOX REP/REPL",
        "51710 - W/S BOX REPAIR-VACTOR",
        "52103 - SEWER MAIN REPAIRS",
        "52303B - SEWER MH REPAIR - MAJOR W SUB",
        "52503A - SEWER LATERAL SPOT REPAIR",
        "61103 - WATERMAIN BREAK REPAIR (WOLF)",
        "61108 - WATERMAIN COMPLAINT INVEST.",
        "61303 - WATER VALVE REPAIRS",
        "61304 - WATER VALVE BOX REPAIRS",
        "61305 - WATER VALVE INSTALL/REPLACE",
        "61307 - WATER VALVE CHAMB REP",
        "61503 - WATER HYDRANT REPAIRS",
        "61701 - WATER/CUSTOMER SERVICE",
        "61702 - WATER SERVICE REPLACEMENT",
        "61703 - WATER SERVICE REPAIR",
        "61704 - WATER SERVICE BOX REP/REPL",
        "61710 - W/S BOX REPAIR-VACTOR",
        "62001 - SEWER RECOVERY COSTED",
        "62103 - SEWER MAIN REPAIRS",
        "62303B - SEWER MH REPAIR - MAJOR W SUB",
        "62503A - SEWER LATERAL SPOT REPAIR",
        "Other"
        ]

    # if problem code is in the list, just returns it back
    if code in allowed:
        return code

    # if not, tries to find similar code and returns proper one from allowed
    for item in allowed:
        if re.search(f".*{code}.*", item):
            return item
    # if nothing above worked, just returns initial problem code
    return code


# creates a list of dicts with reports that are ready to be invoiced
def to_invoice(assignments, reports):
# empty list to fill
    non_match = []
    for r in reports:
        if r["Work Order Number:"] not in assignments:
            non_match.append(r)
    return non_match


# returns formated list of reports with only values that are necessary for invoicing
def format(ready_reports):
    # list of needed headers in specific order
    keep = ["Address:", "Work Order Number:", "Problem Code:", "Yard", "Assignment Type:", "Area:"]
    # list to be filled with formated dicts
    filtered = []
    for row in ready_reports:
        # dict that will be filled in new format
        new_format = {}
        # loops through "keep" list and compares with each key in ready_reports
        for k in keep:
            # since in most casees are is not given, calculates area as length * width, or makes it equal to length if it is a curb
            if k == "Area:":
                try:
                    new_format[k] = str(float(row["Length:"]) * float(row["Width:"]))
                except ValueError:
                    new_format[k] = row["Length:"]
            elif k == "Problem Code:":
                new_format[k] = problem_code(row["Problem Code:"])
            else:
                new_format[k] = row[k]
        # adds formated dict to the list
        filtered.append(new_format)       
    return filtered


# sorts formated data making it ready for invoicing without additional sorting
def final_sort(formated_reports):
    formated_reports.sort(key=lambda x: x["Area:"])  # Least important
    formated_reports.sort(key=lambda x: x["Problem Code:"])
    formated_reports.sort(key=lambda x: x["Assignment Type:"])
    formated_reports.sort(key=lambda x: x["Work Order Number:"])
    formated_reports.sort(key=lambda x: x["Yard"])
    return formated_reports
        

# writes formated CSV ready for invoicing
def write_csv(data, filename):
    if not data:
        raise ValueError("Something wrong with provided data.")
    else:
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[1].keys())
            writer.writeheader()
            writer.writerows(data)
    

if __name__ == "__main__":
    main()


