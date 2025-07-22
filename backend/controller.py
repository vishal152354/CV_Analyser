from model import *
folder_path = r"Your_file_path"
a = check_folder(folder_path)
if a==0 :
    print("folder empty")
else:
    print ("folder non-empty")

n = number_of_files(folder_path)
print("number of files",n)

paths = find_paths_files(folder_path,recursive = False)
print(paths)
content = extract_text(paths)
def get_details():
    all_details = []
    for i in range(len(content)):
        mail_info = get_email(content[i])
        mobile_info = get_mobile(content[i])
        name_info = get_name(content[i])
        details = [mail_info,mobile_info,name_info]
        all_details.append(details)
    return all_details

def add_applicant():
    counting = 0
    n = number_of_files(folder_path)
    applicants = []
    details = get_details()
    for i in range(len(details)):
        applicant = Applicant((details[i][2]),(details[i][1]),(details[i][0]))
        applicants.append(applicant)
        counting+=1

    print("\nCreated Applicant Objects")
    return applicants
