import argparse
import urllib.request
import logging
import datetime

def download_data(url):
    """
    Reads data from a URL and returns the data as a string

    :param url:
    :return: the content of the URL
    """
    # read the URL
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    # return the data
    return response


def processData(file_content):
    personData = {}
    logger = logging.getLogger('assignment2')

    lines = file_content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        if line_number == 1:
            continue

        person = line.split(',')

        person_id = int(person[0])
        name = person[1]
        birthday = person[2]

        try:
            birthday = datetime.datetime.strptime(birthday, '%d/%m/%Y')
            personData[person_id] = (name, birthday)
        except ValueError:
            logger.error(
                "Error processing line #%s for ID #%s",
                line_number,
                person_id
            )

    return personData
            


def displayPerson(id, personData):
    if id not in personData:
        print("No user found with that id")
        return
    name, birthday = personData[id]
    print("Person #{} is {} with a birthday of {}".format(
        id, name, birthday.strftime('%Y-%m-%d')
    ))

def main(url):
    try:
        csvData = download_data(url)
    except Exception as e:
        print("Error downloading data:", e)
        return
    logging.basicConfig(
        filename='error.log',
        level=logging.ERROR,
        format='%(message)s'
    )
    personData = processData(csvData)

    while True:
        user_id = int(input("Enter an ID to lookup: "))

        if user_id <= 0:
            break

        displayPerson(user_id, personData)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
