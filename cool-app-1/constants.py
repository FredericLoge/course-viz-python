import pandas as pd
import numpy as np

# characters -----

# the dates of death were not recorded with the mention ABY or BBY, hence this leads to many incoherences when working with this data, correcting in the data
died_after_yavin = ['General Hux', 'Kylo Ren', 'Captain Phasma', 'Luke Skywalker', 'Leia Organa', 'Jyn Erso', 'Biggs Darklighter',
 'Bodhi Rook', 'Han Solo', 'Val',  'Kanan Jarrus', 'Dryden Vos',  'Rio Durant', 'Darth Vader',  'Greedo',
 'Saw Gerrera',  'Supreme Leader Snoke', 'Beckett',  'Admiral Raddus', 'Orson Krennic',  'Pong Krell', 'Admiral Ackbar',  'Baze Malbus', 
 'Obi-Wan Kenobi',  'Admiral Piett', 'Bib Fortuna',  'Bail Organa', 'Emperor Palpatine',  'Jabba the Hutt', 'Yoda']

# read characters dataset
characters = (
    pd
    .read_csv('star_wars_characters.csv')
    .assign(year_died=lambda df: df.apply(lambda r: -r.year_died if r['name'] in died_after_yavin else r.year_died, axis=1))
)

# characters group -----

characters_group = [
  "Yoda", "Jedi Council",
  "Mace Windu", "Jedi Council",
  "Plo Koon", "Jedi Council",
  "Ki-Adi-Mundi", "Jedi Council",
  "Obi-Wan Kenobi", "Jedi", 
  "Qui-Gon Jinn", "Jedi", 
  "Anakin Skywalker", "Jedi",
  "Luke Skywalker", "Jedi",
  "Darth Sidious", "Sith",
  "Darth Vader", "Sith",
  "Darth Maul", "Sith",
  "Dooku", "Sith",
  "Palpatine", "Politician",
  "Padmé Amidala", "Politician",
  "Bail Prestor Organa", "Politician",
  "Leia Organa", "Politician",
  "Finis Valorum", "Politician",
  "Greedo", "Bounty Hunters",
  "Boba Fett", "Bounty Hunters",
  "Chewbacca", "Thieves",
  "Lando Calrissian", "Thieves",
  "Han Solo", "Thieves"]

characters_group = pd.DataFrame(
    np.reshape(characters_group, [len(characters_group)//2, 2]), 
    columns=['name', 'category']
)

# characters network -----

characters_edges = [
  # jedi teacher-apprentice
  "Obi-Wan Kenobi", "taught", "Anakin Skywalker",
  "Obi-Wan Kenobi", "taught", "Luke Skywalker",
  "Qui-Gon Jinn", "taught", "Obi-Wan Kenobi",
  # sith teacher-apprentice
  "Darth Sidious", "taught", "Darth Vader",
  "Darth Sidious", "taught", "Darth Maul",
  # transition
  "Palpatine", "was in fact", "Darth Sidious",
  "Anakin Skywalker", "became", "Darth Vader",
  # parent of
  "Anakin Skywalker", "parent", "Leia Organa",
  "Padmé Amidala", "parent", "Luke Skywalker",
  "Anakin Skywalker", "parent", "Luke Skywalker",
  "Padmé Amidala", "parent", "Leia Organa",
  "Shmi Skywalker", "parent", "Anakin Skywalker",
  # who killed who
  "Anakin Skywalker", "killed", "Padmé Amidala",
  "Darth Vader", "killed", "Obi-Wan Kenobi",
  "Darth Maul", "killed", "Qui-Gon Jinn",
  "Darth Vader", "killed", "Palpatine"
]

characters_edges = pd.DataFrame(
    np.reshape(characters_edges, [len(characters_edges)//3, 3]),
    columns=['name_1', 'action', 'name_2']
)

# filming locations -----

filming_locations = pd.DataFrame({
  'country': ["Ajim - Mos Eisly spaceport", "Gour Beni Mzab - Dunes", 'Ksar Ommarsia - Mos Espa'],
  'lat': [33.716667, 33.87, 33.34745],
  'lon': [10.75, 7.75, 10.492067]
})