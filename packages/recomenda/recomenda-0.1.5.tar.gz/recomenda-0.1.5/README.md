# Recomenda

![GitHub stars](https://img.shields.io/github/stars/kevinqz/recomenda?style=social)
![License](https://img.shields.io/github/license/kevinqz/recomenda)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

**Recomenda** is **the most simple-to-use Recommender System** designed to seamlessly integrate with your projects. Powered by **OpenAI Embeddings**, Recomenda delivers accurate and efficient recommendations with minimal setup.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Synchronous Recommender](#synchronous-recommender)
  - [Asynchronous Recommender](#asynchronous-recommender)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## Features

- **Simplicity:** Easy-to-use API with minimal configuration.
- **Powered by OpenAI:** Utilizes OpenAI Embeddings for high-quality recommendations.
- **Synchronous & Asynchronous:** Choose between synchronous and asynchronous operations based on your project needs.
- **Extensible:** Easily extend and customize the recommender to fit your specific requirements.
- **Robust Logging:** Comprehensive logging for debugging and monitoring.
- **Configuration Management:** Flexible configuration through environment variables.

---

## Installation

Ensure you have Python 3.8 or higher installed. You can install Recomenda via `pip`:

```bash
pip install recomenda
```

Alternatively, clone the repository and install manually:

```bash
git clone https://github.com/yourusername/recomenda.git
cd recomenda
pip install -r requirements.txt
```

---

## Quick Start

Here's a quick example to get you started with Recomenda.

### 1. Set Up Environment Variables

Ensure you have the `OPENAI_API_KEY` set in your environment. You can create a `.env` file or set it directly in your shell.

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

### 2. Initialize the Recommender

```python
from recomenda import Recommender

# Define your options
options = [
    {"id": 1, "name": "Option A"},
    {"id": 2, "name": "Option B"},
    {"id": 3, "name": "Option C"},
    {"id": 4, "name": "Option D"},
    {"id": 5, "name": "Option E"},
]

# Initialize the Recommender
recommender = Recommender(options=options)

# Generate recommendations based on a target
target = "Your target input here"
recommendations = recommender.generate_recommendations(to=target, how_many=3)

print("Top Recommendations:")
for rec in recommendations:
    print(rec)
```

---

## Usage

Recomenda offers both synchronous and asynchronous Recommender interfaces to cater to different application needs.

### Synchronous Recommender

Ideal for applications where blocking operations are acceptable.

```python
from recomenda import Recommender

options = [
    {"id": 1, "name": "Option A"},
    {"id": 2, "name": "Option B"},
    # Add more options
]

recommender = Recommender(options=options)
target = "Sample input for recommendation"
recommendations = recommender.generate_recommendations(to=target, how_many=5)

for rec in recommendations:
    print(rec)
```

### Asynchronous Recommender

Perfect for high-performance applications requiring non-blocking operations.

```python
import asyncio
from recomenda import AsyncRecommender

async def main():
    options = [
        {"id": 1, "name": "Option A"},
        {"id": 2, "name": "Option B"},
        # Add more options
    ]

    recommender = AsyncRecommender(options=options)
    target = "Sample input for recommendation"
    recommendations = await recommender.generate_recommendations(to=target, how_many=5)

    for rec in recommendations:
        print(rec)

asyncio.run(main())
```

---

## Configuration

Recommender is highly configurable through environment variables. Below are the primary configurations:

### Embedder Configuration

- `OPENAI_API_KEY`: **(Required)** Your OpenAI API key.
- `OPENAI_EMBEDDING_MODEL`: **(Optional)** The OpenAI embedding model to use. Defaults to `text-embedding-3-small`.

### Database Configuration

- `DATABASE_URL`: **(Optional)** The database URL for storing embeddings. Defaults to `sqlite:///./recomenda.db`.

Ensure these variables are set in your environment or defined in a `.env` file.

---

## API Reference

### `Recommender`

The synchronous recommender class.

**Initialization:**

```python
Recommender(
    embedder: Optional[Embedder] = None,
    how: str = "default",
    how_many: int = 5,
    options: Optional[List[Dict[str, Any]]] = None,
    to: Optional[str] = None,
    api_key: str = config.EMBEDDER.OPENAI_API_KEY,
    model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL
)
```

**Methods:**

- `generate_recommendations(to: Optional[str], how_many: Optional[int], force: bool = False) -> List[Dict[str, Any]]`
- `generate_recommendation() -> Optional[Dict[str, Any]]`
- `show_recommendations() -> None`
- `show_recommendation() -> None`

### `AsyncRecommender`

The asynchronous recommender class.

**Initialization:**

```python
AsyncRecommender(
    embedder: Optional[Embedder] = None,
    how: str = "default",
    how_many: int = 5,
    options: Optional[List[Dict[str, Any]]] = None,
    to: Optional[str] = None,
    api_key: str = config.EMBEDDER.OPENAI_API_KEY,
    model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL
)
```

**Methods:**

- `await generate_recommendations(to: Optional[str], how_many: Optional[int]) -> List[Dict[str, Any]]`
- `await generate_recommendation() -> Optional[Dict[str, Any]]`
- `await show_recommendations() -> None`
- `await show_recommendation() -> None`
- `await get_recommendations_str() -> str`

For detailed documentation, refer to the [docs](https://github.com/yourusername/recomenda/docs).

---

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit your Changes**
   ```bash
   git commit -m "Add YourFeature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request**

Please ensure your contributions adhere to the project's code of conduct and guidelines.

---

## License

Distributed under the [MIT License](LICENSE). See `LICENSE` for more information.

---

## Support

If you encounter any issues or have questions, feel free to [open an issue](https://github.com/yourusername/recomenda/issues) or reach out via [email](mailto:support@yourdomain.com).

---

## Acknowledgements

- [OpenAI](https://openai.com/) for providing powerful embedding models.
- [Scipy](https://www.scipy.org/) for the cosine similarity implementation.
- [Python Logging](https://docs.python.org/3/library/logging.html) for robust logging capabilities.

---

*Happy Recommending! 🚀*