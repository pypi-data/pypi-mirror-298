from importlib.metadata import metadata

from .blackjack import Card, Dealer, GameMaster, Player, main

__all__ = ["Card", "Dealer", "GameMaster", "Player", "main"]
_package_metadata = metadata(__package__)
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")
