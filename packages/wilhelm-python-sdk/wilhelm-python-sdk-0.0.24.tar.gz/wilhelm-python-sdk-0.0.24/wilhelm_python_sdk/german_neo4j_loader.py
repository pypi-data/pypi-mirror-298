# Copyright Jiaqi (Hutao of Emberfire)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os

from neo4j import GraphDatabase

from wilhelm_python_sdk.vocabulary_database_loader import (
    GERMAN, get_definitions, get_vocabulary, save_a_link_with_attributes,
    save_a_node_with_attributes)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URI = os.environ["NEO4J_URI"]
DATABASE = os.environ["NEO4J_DATABASE"]
AUTH = (os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])


def is_noun(word: object) -> bool:
    return word["term"].startswith(("der"))
    # return word["term"].startswith(("der", "die", "das"))


def is_adjectival_noun(word: object) -> bool:
    return is_noun(word) and is_adjective(word)


def is_adjective(word: object) -> bool:
    """
    Returns whether or not a German word is an adjective.

    A word is an adjective if it contains a "declension" field with the following 3 sub-fields:

    1. strong declension (without article)
    2. weak declension (with definite article)
    3. mixed declension (with indefinite article)

    For example, the following entry represents an adjective:

    .. code-block:: python

       - term: interessiert
         definition: (adj.) interested
         declension:
           strong declension (without article): ...
           weak declension (with definite article): ...
           mixed declension (with indefinite article): ...

    :param word:  A YAML vocabulary item as a Dict from wilhelm-vocabulary

    :return: `True` if the vocabulary is a German adjective, or `False` otherwise
    """
    return "declension" in word and all(
        key in word["declension"] for key in ["strong declension (without article)",
                                              "weak declension (with definite article)",
                                              "mixed declension (with indefinite article)"]
    )


def get_attributes(word: object) -> dict:
    attributes = {"name": word["term"], "language": GERMAN}

    if is_noun(word) and not is_adjectival_noun(word):
        declension = word["declension"]

        for i, row in enumerate(declension):
            for j, col in enumerate(row):
                attributes[f"declension-{i}-{j}"] = declension[i][j]

    return attributes


def load_into_database(yaml_path: str):
    """
    Upload https://github.com/QubitPi/wilhelm-vocabulary/blob/master/german.yaml to Neo4j Database.

    :param yaml_path:  The absolute or relative path (to the invoking script) to the YAML file above
    """
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

    vocabulary = get_vocabulary(yaml_path)

    for word in vocabulary:
        term = word["term"]

        save_a_node_with_attributes(driver, "Term", get_attributes(word))

        definitions = get_definitions(word)
        for definition_with_predicate in definitions:
            predicate = definition_with_predicate[0]
            definition = definition_with_predicate[1]

            save_a_node_with_attributes(driver, "Definition", {"name": definition})

            if predicate:
                save_a_link_with_attributes(GERMAN, driver, term, definition, {"name": predicate})
            else:
                save_a_link_with_attributes(GERMAN, driver, term, definition, {"name": "definition"})
