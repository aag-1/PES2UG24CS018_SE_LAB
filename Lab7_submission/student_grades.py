import re


def average_marks(marks_csv):
    if not isinstance(marks_csv, str):
        return None
    marks = []
    for m in marks_csv.split(','):
        m = m.strip()
        if not (m.isascii() and m.isdigit() and len(m) <= 3) or int(m) > 100:
            return None
        marks.append(int(m))
    return round(sum(marks) / len(marks), 2)

def parse_srn(srn):
    if not isinstance(srn, str):
        return None
    srn = srn.strip().upper()
    if not re.fullmatch(r"PES[0-9]UG[0-9]{2}[A-Z]{2}[0-9]{3}", srn):
        return None
    return srn[:4], int(srn[6:8]), srn[8:10]

def short_name(full_name):
    if not isinstance(full_name, str):
        return None
    parts = full_name.split()
    if len(parts) < 2:
        return None
    return parts[0][0].upper() + ". " + parts[-1].capitalize()

def main():
    print("==== Running average_marks ====")
    user_input = input("Enter marks as CSV (e.g. 78,85,92): ")
    result = average_marks(user_input)
    print("Average Marks:", result if result is not None else "Invalid input")

    print("\n==== Running parse_srn ====")
    user_input = input("Enter an SRN (e.g. PES1UG23CS123): ")
    result = parse_srn(user_input)
    print("Campus, Year and Dept:", result if result is not None else "Invalid input")

    print("\n==== Running short_name ====")
    user_input = input("Enter first and last name (e.g. ravi kumar): ")
    result = short_name(user_input)
    print("Short Name:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
