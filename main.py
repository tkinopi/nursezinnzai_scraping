from component import *

def main():
    url_list = get_job_list_url()
    urls = get_job_url(url_list)
    # urls = ['https://www.nursejinzaibank.com/office_916345/job_473493/','https://www.nursejinzaibank.com/office_4476/job_568001/']
    jobs = []
    for url in urls:
        result = get_job_info(url)
        print(result)
        jobs.append(result)

    # jobs = []
    # for url in flat_urls:
    #     result_dict = get_job_info(url)
    #     jobs.append(result_dict)
    # print(jobs)
    write_to_spreadsheet(jobs)


if __name__ == "__main__":
    main()