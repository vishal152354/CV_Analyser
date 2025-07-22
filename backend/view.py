from controller import *
def write_csv(csv_filename):
    applicants = add_applicant()
    print (applicants)
    try:
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
         writer = csv.writer(file)
         writer.writerow(["Name", "Email", "Mobile"])
         for applicant in applicants:
           writer.writerow([applicant.name, applicant.email, applicant.mobile])
        print(f"\nData successfully written to {csv_filename}")
    except IOError as e:
        print(f"Error writing to CSV file {csv_filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
write_csv("applicant_data.csv")