
# PokeAPI SDK

A simple Python SDK for interacting with the [PokeAPI](https://pokeapi.co/), allowing you to retrieve details about Pokémon, generations, and more.

## Features

- Fetch details about a specific Pokémon by its ID or name
- Retrieve a paginated list of Pokémon
- Fetch a list of Pokémon generations
- Retrieve information about Pokémon in a specific generation

## Installation

Install the SDK using pip after building and publishing it (or directly from the source):

```bash
pip install pokeapi-sdk
```

## Usage

### 1. Initialize the PokeAPI Client

To start using the SDK, you need to initialize the `PokeAPIClient` class.

```python
from pokeapi_sdk.client import PokeAPIClient

client = PokeAPIClient()
```

### 2. Fetch Pokémon Details

You can fetch details of a Pokémon by providing its ID or name.

```python
pokemon = client.get_pokemon("pikachu")
```

### 3. Fetch a Paginated List of Pokémon

You can fetch a list of Pokémon with pagination using the `limit` and `offset` parameters.

```python
pokemons = client.get_pokemons(limit=10, offset=0)
```

### 4. Fetch Pokémon Generations

You can retrieve a list of Pokémon generations:

```python
generations = client.get_pokemon_generation_list()
```

### 5. Fetch Pokémon by Generation

You can fetch all Pokémon in a specific generation by its identifier:

```python
generation = client.get_pokemon_by_generation("generation-i")
```

## Error Handling

The SDK uses custom exceptions to handle various error cases:

- **`PokeAPIError`**: Raised when a general error occurs with the PokeAPI.
- **`PokemonNotFoundError`**: Raised when a specific Pokémon is not found (404 error).

You can handle these exceptions as shown in the examples above to ensure your application handles errors gracefully.
