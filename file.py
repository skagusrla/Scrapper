from extractor.wwr import extract_wwr_jobs
from extractor.indeed import extract_indeed_jobs


def save_to_file(file_name, jobs):

    file = open(f"{file_name}.csv", "w")
    file.write("Position, Company, Location, URL")

    for job in jobs:
        file.write(
            f"{job['position']},{job['company']},{job['location']},{job['link']}\n"
        )
    file.close()
