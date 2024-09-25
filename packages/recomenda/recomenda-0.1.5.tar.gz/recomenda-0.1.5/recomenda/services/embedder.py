import logging
from typing import Any, List
import asyncio
from openai import OpenAI, AsyncOpenAI, OpenAIError

from recomenda.core.config import config
from recomenda.core.logger import logger


class Embedder:
    def __init__(
        self,
        model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL,
        api_key: str = config.EMBEDDER.OPENAI_API_KEY
    ) -> None:
        """
        Initializes the Embedder with the specified model and API key.

        Args:
            model (str): The name of the embedding model to use. Defaults to the value in config.
            api_key (str): The API key for the OpenAI service. Defaults to the value in config.
        """
        logger.debug(f"Using OpenAI API Key: {'*' * 4 + api_key[-4:]}")
        self.sync_client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        self.model = model
        logger.debug(f"Embedder initialized with model: {self.model}")

    def normalize_to_embed(self, items: List[Any]) -> List[str]:
        """
        Normalizes items into string representations suitable for embedding.

        Args:
            items (List[Any]): A list of items to be normalized.

        Returns:
            List[str]: A list of normalized string representations of the input items.
        """
        logger.debug(f"Normalizing items for embedding: {items}")
        normalized_items = [self.stringify_item(item) for item in items]
        logger.debug(f"Normalized items: {normalized_items}")
        return normalized_items

    def stringify_item(self, item: Any) -> str:
        """
        Converts an item to its string representation.

        Args:
            item (Any): The item to be converted to a string.

        Returns:
            str: The string representation of the input item.
        """
        logger.debug(f"Stringifying item: {item}")
        if isinstance(item, str):
            return item
        elif isinstance(item, dict):
            return ', '.join(f"{key}: {value}" for key, value in item.items())
        elif hasattr(item, '__dict__'):
            return ', '.join(f"{key}: {value}" for key, value in item.__dict__.items())
        else:
            logger.warning(f"Unexpected item type: {type(item)}. Converting to string.")
            return str(item)

    async def embed_item_async(self, item: Any) -> List[float]:
        """
        Asynchronously generates an embedding for a single item.

        Args:
            item (Any): The item to be embedded.

        Returns:
            List[float]: The embedding vector for the input item.

        Raises:
            OpenAIError: If there's an error with the OpenAI API.
            Exception: If there's any other unexpected error.
        """
        logger.debug(f"Async embedding single item: {item}")
        try:
            normalized_item = self.normalize_to_embed([item])
            response = await self.async_client.embeddings.create(model=self.model, input=normalized_item)
            embedding = response.data[0].embedding
            logger.debug(f"Generated async embedding for item: {embedding}")
            return embedding
        except OpenAIError as e:
            logger.error(f"OpenAI API error while embedding item: {item} | Error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error while embedding item: {item} | Error: {e}", exc_info=True)
            raise

    def embed_item_sync(self, item: Any) -> List[float]:
        """
        Synchronously generates an embedding for a single item.

        Args:
            item (Any): The item to be embedded.

        Returns:
            List[float]: The embedding vector for the input item.

        Raises:
            OpenAIError: If there's an error with the OpenAI API.
            Exception: If there's any other unexpected error.
        """
        logger.debug(f"Sync embedding single item: {item}")
        try:
            normalized_item = self.normalize_to_embed([item])
            response = self.sync_client.embeddings.create(model=self.model, input=normalized_item)
            embedding = response.data[0].embedding
            logger.debug(f"Generated sync embedding for item: {embedding}")
            return embedding
        except OpenAIError as e:
            logger.error(f"OpenAI API error while embedding item: {item} | Error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error while embedding item: {item} | Error: {e}", exc_info=True)
            raise

    async def embed_items_async(self, items: List[Any]) -> List[List[float]]:
        """
        Asynchronously generates embeddings for multiple items.

        Args:
            items (List[Any]): A list of items to be embedded.

        Returns:
            List[List[float]]: A list of embedding vectors, one for each input item.

        Raises:
            OpenAIError: If there's an error with the OpenAI API.
            Exception: If there's any other unexpected error.
        """
        logger.debug(f"Async embedding multiple items: {items}")
        try:
            normalized_items = self.normalize_to_embed(items)
            response = await self.async_client.embeddings.create(model=self.model, input=normalized_items)
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Generated async embeddings for items: {embeddings}")
            return embeddings
        except OpenAIError as e:
            logger.error(f"OpenAI API error while embedding items: {items} | Error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error while embedding items: {items} | Error: {e}", exc_info=True)
            raise

    def embed_items_sync(self, items: List[Any]) -> List[List[float]]:
        """
        Synchronously generates embeddings for multiple items.

        Args:
            items (List[Any]): A list of items to be embedded.

        Returns:
            List[List[float]]: A list of embedding vectors, one for each input item.

        Raises:
            OpenAIError: If there's an error with the OpenAI API.
            Exception: If there's any other unexpected error.
        """
        logger.debug(f"Sync embedding multiple items: {items}")
        try:
            normalized_items = self.normalize_to_embed(items)
            response = self.sync_client.embeddings.create(model=self.model, input=normalized_items)
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Generated sync embeddings for items: {embeddings}")
            return embeddings
        except OpenAIError as e:
            logger.error(f"OpenAI API error while embedding items: {items} | Error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error while embedding items: {items} | Error: {e}", exc_info=True)
            raise
