import os.path

import dateutil.parser
import petl as etl
import requests

BASE_SW_API = "https://swapi.dev/api"


class Fetcher:
    """
    Use to fetch and extract only the useful data from SW API
    """

    def _fetch(self, url):
        return requests.get(url)

    def get_data(self):
        """
        Fetch data from all pages the api and reformat them to remove the unused one (pagination...)

        :return: a json containing data
        """
        url = os.path.join(BASE_SW_API, "people/")
        json_response = self._fetch(url).json()
        total_count = json_response["count"]
        all_results = json_response["results"]

        # got thought all the page next by next until we get all objects or next_url is None
        while len(all_results) < total_count:
            next_url = json_response["next"]
            if next_url is None:
                break
            json_response = self._fetch(next_url).json()
            all_results += json_response["results"]
        return all_results


class PeopleManager:
    """
    Manage json data representing people
    Transform  and prepare them top be saved as CSV
    """
    # contain the homeworld_map path as key and the real name as value
    homeworld_map = {}

    def _get_homeworld_name(self, homeworld_path):
        """
        return the homeworld name from the homeworld_path
        use the homeworld_map as cache to avoid fetch it everytime

        :param homeworld_path:
        :return: the homeworld name
        """
        homeworld_name = self.homeworld_map.get(homeworld_path, None)
        if homeworld_name is None:
            # Homeworld is hasn't been fetched, get it and put it in the cache
            homeworld_data = requests.get(homeworld_path).json()
            homeworld_name = homeworld_data["name"]
            # insert the new pair path/name into the cache
            self.homeworld_map[homeworld_path] = homeworld_name
        return homeworld_name

    def parse_date(self, date):
        """
        parse a string datetime and return the date format
        :param date: a string date
        :return a parsed and reformatted date as string in the correct format "%Y-%m-%d"
        """
        datetime = dateutil.parser.isoparse(date)
        return datetime.strftime("%Y-%m-%d")

    def get_clean_table(self, data):
        """
        Add a new "date" key based on "edited" key
        Resolve homeworld
        remove unused fields
        """
        table = etl.fromdicts(data)
        # replace the edited column to date
        table = table.rename("edited", "date")
        table = table.convert('date', self.parse_date)

        # resolve all homeworld using the function _get_homeworld
        table = table.convert('homeworld', self._get_homeworld_name)

        # remove all the unused fields
        fields_to_remove = ("films", "species", "vehicles", "starships", "created", "url")
        for field_name in fields_to_remove:
            table = table.cutout(field_name)
        return table
