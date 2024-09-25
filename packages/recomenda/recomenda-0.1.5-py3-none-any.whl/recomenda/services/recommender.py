import logging
from typing import List, Optional, Dict, Any, Union
import hashlib

from recomenda.services.embedder import Embedder
from recomenda.services.base_recommender import BaseRecommender
from recomenda.core.config import config
from recomenda.core.logger import logger
from recomenda.utils.hashing import generate_hash, update_hashes


class Recommender(BaseRecommender):
    def __init__(
        self,
        embedder: Optional[Embedder] = None,
        how: str = "default",
        how_many: int = 5,
        options: Optional[List[Dict[str, Any]]] = None,
        to: Optional[str] = None,
        api_key: str = config.EMBEDDER.OPENAI_API_KEY,
        model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL,
        logger_instance: Optional[logging.Logger] = None
    ) -> None:
        """
        Initializes the Recommender with the specified parameters.

        Args:
            embedder (Optional[Embedder]): An instance of the Embedder class. If None, a new one will be created.
            how (str): The method to use for recommendations. Defaults to "default".
            how_many (int): The number of recommendations to generate. Defaults to 5.
            options (Optional[List[Dict[str, Any]]]): A list of options to recommend from. Defaults to None.
            to (Optional[str]): The target to generate recommendations for. Defaults to None.
            api_key (str): The API key for the embedding service. Defaults to the value in config.
            model (str): The name of the embedding model to use. Defaults to the value in config.
            logger_instance (Optional[logging.Logger]): A custom logger instance. If None, a default logger will be used.
        """
        super().__init__(api_key=api_key, model=model, embedder=embedder, logger_instance=logger_instance)
        self.how = how
        self.how_many = how_many
        self._options: List[Dict[str, Any]] = options or []
        self.to = to
        self.options_embeddings: Optional[List[List[float]]] = None
        self.to_embeddings: Optional[List[float]] = None
        self._recommendation: Optional[Dict[str, Any]] = None
        self._recommendations: Optional[List[Dict[str, Any]]] = None
        self._options_hash: Dict[str, str] = {}

        if self._options:
            self._initialize_embeddings_sync()
        logger.debug(f"Initialized with how={how}, how_many={how_many}, options={options}, to={to}")

    @staticmethod
    def hash_option(option: Dict[str, Any]) -> str:
        """
        Generates a hash for a given option.

        Args:
            option (Dict[str, Any]): The option to hash.

        Returns:
            str: A hash string representing the option.
        """
        return generate_hash(option)
      
    def update_option_hashes(self) -> List[Union[Dict[str, Any], str]]:
        """
        Updates the hashes for the current options.

        Returns:
            List[Union[Dict[str, Any], str]]: A list of options that need to be re-embedded.
        """
        # Using the utility function to update hashes
        options_to_embed, self._options_hash = update_hashes(self._options, self._options_hash)
        return options_to_embed

    @property
    def options(self) -> List[Dict[str, Any]]:
        """
        Gets the current options.

        Returns:
            List[Dict[str, Any]]: The current list of options.
        """
        return self._options

    @options.setter
    def options(self, new_options: List[Dict[str, Any]]):
        """
        Sets new options and updates embeddings if necessary.

        Args:
            new_options (List[Dict[str, Any]]): The new list of options to set.
        """
        logger.debug("Options updated. Checking for changes.")
        self._options = new_options
        options_to_embed = self.update_option_hashes()
        if options_to_embed:
            logger.info(f"New or modified options detected, embedding required for {len(options_to_embed)} options.")
            self._initialize_embeddings_sync(options_to_embed)
        else:
            logger.info("No changes detected in options. No re-embedding needed.")

    def _initialize_embeddings_sync(self, options_to_embed: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Initializes embeddings for options synchronously.

        Args:
            options_to_embed (Optional[List[Dict[str, Any]]]): A list of options to embed. If None, all options will be embedded.
        """
        logger.debug("Initializing embeddings for options synchronously.")
        self._initialize_embeddings(options_to_embed)

    def generate_recommendations(
        self,
        to: Optional[str] = None,
        how_many: Optional[int] = None,
        force: bool = False  # Added force parameter
    ) -> List[Dict[str, Any]]:
        """
        Generates recommendations based on the given parameters.

        Args:
            to (Optional[str]): The target to generate recommendations for. If None, uses the instance's 'to' attribute.
            how_many (Optional[int]): The number of recommendations to generate. If None, uses the instance's 'how_many' attribute.
            force (bool): If True, forces regeneration of recommendations even if they already exist.

        Returns:
            List[Dict[str, Any]]: A list of recommended options with their similarities.

        Raises:
            ValueError: If options data is empty or no target is provided.
        """
        logger.debug("Starting generate_recommendations method")

        if not force and self._recommendations and (how_many is None or len(self._recommendations) >= how_many):
            return self._recommendations[:how_many]

        if not self.options_embeddings:
            self._initialize_embeddings_sync()

        if not self.options_embeddings:
            logger.error("Options data is empty. Please set the options data first.")
            raise ValueError("Options data is empty. Please set the options data first.")

        target = to or self.to
        if not target:
            logger.error("No target provided for recommendations.")
            raise ValueError("No target provided for recommendations.")

        try:
            logger.debug(f"Generating embeddings for target: {target}")
            self.to_embeddings = self.embedder.embed_item_sync(target)

            logger.debug("Calculating similarities and sorting recommendations")
            recommendations = [
                {
                    'option': option,
                    'similarity': self.calculate_similarity(self.to_embeddings, embedding)
                }
                for option, embedding in zip(self.options, self.options_embeddings)
            ]

            logger.debug(f"Unsorted recommendations: {recommendations}")

            recommendations.sort(key=lambda x: x['similarity'], reverse=True)
            n = how_many if how_many is not None else self.how_many
            self._recommendations = recommendations[:n]
            if not self._recommendation:
                self._recommendation = self._recommendations[0]['option'] if self._recommendations else None

            logger.debug(f"Generated {len(self._recommendations)} recommendations")
            return self._recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}", exc_info=True)
            raise
        finally:
            logger.debug("Finished generate_recommendations method")

    def generate_recommendation(self) -> Optional[Dict[str, Any]]:
        """
        Generates a single recommendation.

        Returns:
            Optional[Dict[str, Any]]: The recommended option, or None if no recommendation could be generated.
        """
        logger.debug("Starting generate_recommendation method")
        if not self._recommendation:
            if not self._recommendations:
                # Generate recommendations only if they don't exist
                self.generate_recommendations(how_many=1, force=True)
            if self._recommendations:
                self._recommendation = self._recommendations[0]['option']
        logger.debug(f"Generated single recommendation: {self._recommendation}")
        return self._recommendation

    @property
    def complete_recommendations(self) -> List[Dict[str, Any]]:
        """
        Gets the complete list of recommendations with similarity scores.

        Returns:
            List[Dict[str, Any]]: A list of recommended options with their similarities.
        """
        logger.debug("Accessing complete_recommendations property")
        if self._recommendations is None and self.to:
            self.generate_recommendations(force=True)  # Force to ensure full recommendations list
        return self._recommendations or []

    @property
    def complete_recommendation(self) -> Optional[Dict[str, Any]]:
        """
        Gets the top recommendation with similarity score.

        Returns:
            Optional[Dict[str, Any]]: The top recommended option with its similarity, or None if no recommendation is available.
        """
        logger.debug("Accessing complete_recommendation property")
        if self._recommendation is None and self.to:
            self.generate_recommendation()
        return self._recommendation

    def show_complete_recommendations(self) -> None:
        """
        Displays all complete recommendations with their similarities and rankings.
        """
        logger.debug("Showing all complete recommendations")
        if self._recommendations is None:
            self.generate_recommendations(force=True)
        if self._recommendations:
            for index, reco in enumerate(sorted(self._recommendations, key=lambda x: x['similarity'], reverse=True)):
                print(f"Option: {reco['option']}, Similarity: {reco['similarity']}, Ranking: {index + 1}")
        else:
            logger.warning("No recommendations available to show.")
            logger.debug(f"Current recommendations: {self._recommendations}")

    def show_complete_recommendation(self) -> None:
        """
        Displays the top complete recommendation.
        """
        logger.debug("Showing single complete recommendation")
        if self._recommendation is None:
            self.generate_recommendation()
        if self._recommendation:
            print(f"Recommended Option: {self._recommendation}")
        else:
            logger.warning("No recommendation available to show.")
            logger.debug(f"Current recommendation: {self._recommendation}")

    @property
    def recommendations(self) -> List[Any]:  # Only returning options without extra details
        """
        Gets the list of recommended options without similarity scores.

        Returns:
            List[Any]: A list of recommended options.
        """
        logger.debug("Accessing recommendations property")
        if self._recommendations is None and self.to:
            self.generate_recommendations(force=True)
        return [reco['option'] for reco in (self._recommendations or [])]

    @property
    def recommendation(self) -> Optional[Any]:  # Only returning single option without extra details
        """
        Gets the top recommended option without similarity score.

        Returns:
            Optional[Any]: The top recommended option, or None if no recommendation is available.
        """
        logger.debug("Accessing recommendation property")
        if self._recommendation is None and self.to:
            self.generate_recommendation()
        return self._recommendation

    def show_recommendations(self) -> None:  # Simplified display of options
        """
        Displays all recommended options without similarity scores.
        """
        logger.debug("Showing all recommendations")
        if self._recommendations is None:
            self.generate_recommendations(force=True)
        if self._recommendations:
            for reco in self._recommendations:
                print(f"Option: {reco['option']}")
        else:
            logger.warning("No recommendations available to show.")
            logger.debug(f"{self._recommendations}")

    def show_recommendation(self) -> None:  # Simplified display of a single option
        """
        Displays the top recommended option without similarity score.
        """
        logger.debug("Showing single recommendation")
        if self._recommendation is None:
            self.generate_recommendation()
        if self._recommendation:
            print(f"{self._recommendation}")
        else:
            logger.warning("No recommendation available to show.")
            logger.debug(f"Current recommendation: {self._recommendation}")

    def __str__(self) -> str:
        """
        Returns a string representation of the Recommender instance.

        Returns:
            str: A string representation of the Recommender.
        """
        return f"Recommender(how={self.how}, how_many={self.how_many}, options={self.options}, to={self.to})"