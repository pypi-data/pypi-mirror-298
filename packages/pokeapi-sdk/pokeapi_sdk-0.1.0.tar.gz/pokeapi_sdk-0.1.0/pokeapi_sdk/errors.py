class PokeAPIError(Exception):
    """Custom exception for PokeAPI errors."""

    pass


class PokemonNotFoundError(PokeAPIError):
    """Custom exception when a Pokémon is not found."""

    pass
