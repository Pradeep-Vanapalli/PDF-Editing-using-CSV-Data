import os
import fitz
import pandas as pd

def is_nan(value):
    return value != value

def replace_pdf_text(input_pdf,replace_text,adhaar):
    # Prompt user for input of search and replace text
    search_replace_list=[]
    for items in replace_text.items():
        search_replace_list.append(list(items))


        pdf_file = fitz.open(input_pdf)
        found = False
        for page in pdf_file:
            for search_text, replace_text in search_replace_list:
                draft = page.search_for(search_text.strip(), hit_max=16, quads=True, quads_tol=0.01)
                #print(draft)
                #print(replace_text)
                #print(input_pdf)
                if draft:
                    found = True
                    for rect in draft:
                        if len(replace_text)<=6 or replace_text=="Very High":
                            annot = page.add_redact_annot(rect, text=replace_text, fontname="hebo", fontsize=10)
                        else:
                            annot = page.add_redact_annot(rect, text=replace_text, fontname="helv", fontsize=10)

                    page.apply_redactions()
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

        if found:
            output_file_name = f'/home/pradeep/trustr/site1/Trustr_site1_{first_name}_{adhaar}.pdf'
            pdf_file.save(output_file_name, garbage=False, deflate=True, encryption=False)
            #print(f"Changes saved to {output_file_name}")
        else:
            print(f"No search text found in {input_pdf}")

        pdf_file.close()


input_pdf_file= '/home/pradeep/trustr/files/pdf_temp.pdf'
user_df=pd.read_csv('/home/pradeep/trustr/files/health_data_site1.csv')
#user_df.fillna(0, inplace=True)
print(f"shape of df:{user_df.shape}[0]")

# Keep track of processed Aadhaar numbers
processed_vitals = set()


for row in range(0,user_df.shape[0]):
    first_name=user_df.iloc[row]['first_name']
    gender=user_df.iloc[row]['gender']
    age=int(user_df.iloc[row]['age'])
    adhaar=user_df.iloc[row]['aadhar_number'][-4:]
    HR=int(user_df.iloc[row]['heart_rate'])
    OS = int(user_df.iloc[row]['spo2'])
    BR =int(user_df.iloc[row]['br'])
    SL = user_df.iloc[row]['sl']
    BP = user_df.iloc[row]['bp']
    DATE = user_df.iloc[row]['updated_at']

    # Skip if this Aadhaar number has already been processed
    if first_name in processed_vitals:
        print(f"Aadhaar {first_name} already processed. Skipping...")
        continue

    # Record that this Aadhaar number has been processed
    processed_vitals.add(first_name)

    replacements = {
        "Aug 06, 2023, 01:20 AM": f"{DATE}",
        "M nameshalini santosh sai": f"{first_name}",
        "ABCD/Female":f'{age}/{gender}',
        'XXXX XXXX EFGH':f'XXXX XXXX {adhaar}',
        'IJKL':f'{HR}',
        'IJKP':f'{OS}',
        'IJKT':f'{BR}',
        'Normalk':f'{SL}',
        'UVWX':f'{BP}'
    }

    replace_pdf_text(input_pdf_file,replacements,adhaar)
    if row==user_df.shape[0]:
        break