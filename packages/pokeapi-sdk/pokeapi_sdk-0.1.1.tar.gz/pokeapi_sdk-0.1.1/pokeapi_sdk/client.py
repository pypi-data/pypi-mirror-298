import requests

from pokeapi_sdk.errors import PokeAPIError, PokemonNotFoundError


class PokeAPIClient:
    BASE_URL = "https://pokeapi.co/api/v2"

    def __init__(self):
        """Initialize the PokeAPI client."""
        pass

    def get_pokemon(self, pokemon_identifier):
        """
        Fetch details about a specific Pokémon by its ID or name.

        :param identifier: Pokémon ID (int) or name (str)
        :return: JSON response containing Pokémon data
        :raises PokeAPIError: If the request fails or the Pokémon is not found
        """
        url = f"{self.BASE_URL}/pokemon/{pokemon_identifier}/"
        response = requests.get(url)

        if response.status_code == 404:
            raise PokemonNotFoundError(f"Pokémon {pokemon_identifier} not found (404).")
        elif response.status_code != 200:
            raise PokeAPIError(f"Error fetching Pokémon {pokemon_identifier}: {response.status_code} - {response.text}")

        return response.json()

    def get_pokemons(self, limit=20, offset=0):
        """
        Fetch a list of Pokémon with pagination (limit and offset).

        :param limit: The number of Pokémon to return (default: 20)
        :param offset: The starting point for results (default: 0)
        :return: JSON response containing a list of Pokémon and pagination info
        :raises PokeAPIError: If the request fails
        """
        url = f"{self.BASE_URL}/pokemon?limit={limit}&offset={offset}"
        response = requests.get(url)

        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching Pokémon list: {response.status_code} - {response.text}")

        return response.json()

    def get_pokemon_generation_list(self):
        url = f"{self.BASE_URL}/generation/"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise PokeAPIError(f"Error fetching Pokémon generation list: {response.status_code} - {response.text}")

    def get_pokemon_by_generation(self, generation_identifier):
        url = f"{self.BASE_URL}/generation/{generation_identifier}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise PokeAPIError(f"Error fetching Pokémon generation: {response.status_code} - {response.text}")
