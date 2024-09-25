import logging
from typing import List, Optional, Any, Dict
from scipy.spatial.distance import cosine

from recomenda.services.embedder import Embedder
from recomenda.core.config import config
from recomenda.core.logger import logger
from recomenda.utils.hashing import generate_hash, update_hashes


class BaseRecommender:
    def __init__(
        self,
        api_key: str = config.EMBEDDER.OPENAI_API_KEY,
        model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL,
        embedder: Optional[Embedder] = None,
        logger_instance: Optional[logging.Logger] = None
    ) -> None:
        """
        Initializes the BaseRecommender with the specified API key, model, and logger.

        Args:
            api_key (str): The API key for the embedding service. Defaults to the value in config.
            model (str): The name of the embedding model to use. Defaults to the value in config.
            embedder (Optional[Embedder]): An instance of the Embedder class. If None, a new one will be created.
            logger_instance (Optional[logging.Logger]): A custom logger instance. If None, a default logger will be used.
        """
        self.api_key: str = api_key
        self.model: str = model
        self.embedder = embedder or Embedder(model=self.model, api_key=self.api_key)
        self.logger = logger_instance or logging.getLogger(__name__)
        self.logger.debug(f"BaseRecommender initialized with model: {self.model} and api_key: {self.api_key}")

    async def generate_embeddings(self, data: List[str]) -> List[List[float]]:
        """
        Asynchronously generates embeddings for a list of data items.

        Args:
            data (List[str]): A list of strings to generate embeddings for.

        Returns:
            List[List[float]]: A list of embeddings, where each embedding is a list of floats.

        Raises:
            Exception: If there's an error during the embedding generation process.
        """
        logger.debug(f"Generating embeddings for data: {data}")
        try:
            embeddings = await self.embedder.embed_items_async(data)
            logger.debug(f"Generated embeddings: {embeddings}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}", exc_info=True)
            raise

    def generate_embeddings_sync(self, data: List[str]) -> List[List[float]]:
        """
        Synchronously generates embeddings for a list of data items.

        Args:
            data (List[str]): A list of strings to generate embeddings for.

        Returns:
            List[List[float]]: A list of embeddings, where each embedding is a list of floats.

        Raises:
            Exception: If there's an error during the embedding generation process.
        """
        logger.debug(f"Generating embeddings for data synchronously: {data}")
        try:
            embeddings = self.embedder.embed_items_sync(data)
            logger.debug(f"Generated embeddings: {embeddings}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}", exc_info=True)
            raise

    def calculate_similarity(self, embed1: List[float], embed2: List[float]) -> float:
        """
        Calculates cosine similarity between two embeddings.

        Args:
            embed1 (List[float]): The first embedding vector.
            embed2 (List[float]): The second embedding vector.

        Returns:
            float: The cosine similarity between the two embeddings.

        Raises:
            Exception: If there's an error during the similarity calculation.
        """
        try:
            similarity = 1 - cosine(embed1, embed2)
            logger.debug(f"Calculated similarity: {similarity}")
            return similarity
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}", exc_info=True)
            raise

    def set_logger(self, logger_instance: logging.Logger) -> None:
        """
        Sets a custom logger instance for this BaseRecommender instance.

        Args:
            logger_instance (logging.Logger): The logger instance to use.
        """
        self.logger = logger_instance
        self.logger.debug("Logger instance has been updated for this BaseRecommender instance.")

    def _initialize_embeddings(self, options_to_embed: Optional[List[Dict[str, Any]]] = None) -> List[List[float]]:
        """
        Initializes embeddings for options. Can be used by both sync and async subclasses.

        Args:
            options_to_embed (Optional[List[Dict[str, Any]]]): A list of options to embed. If None, self._options will be used.

        Returns:
            List[List[float]]: A list of embeddings for the provided options.

        Raises:
            Exception: If there's an error during the embedding initialization process.
        """
        logger.debug("Initializing embeddings for options.")
        if not self._options:
            logger.warning("No options available to embed.")
            return []

        if options_to_embed is None:
            options_to_embed = self._options

        try:
            new_embeddings = self.embedder.embed_items_sync(options_to_embed)

            if self.options_embeddings is None:
                self.options_embeddings = []

            for option, embedding in zip(options_to_embed, new_embeddings):
                option_hash = self.hash_option(option)
                if option_hash in self._options_hash:
                    index = list(self._options_hash.keys()).index(option_hash)
                    if index < len(self.options_embeddings):
                        self.options_embeddings[index] = embedding
                    else:
                        self.options_embeddings.append(embedding)
                else:
                    self.options_embeddings.append(embedding)

            logger.info("Embeddings updated successfully for modified options.")
            return new_embeddings
        except Exception as e:
            logger.error(f"Error updating embeddings: {e}", exc_info=True)
            raise

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

    def update_option_hashes(self) -> List[Dict[str, Any]]:
        """
        Updates the hashes for the current options.

        Returns:
            List[Dict[str, Any]]: A list of options that need to be re-embedded.
        """
        # Using the utility function to update hashes
        options_to_embed, self._options_hash = update_hashes(self._options, self._options_hash)
        return options_to_embed