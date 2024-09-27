# AIDSTK Library

A modular and flexible AI library for processing text data using customizable prompts and configurations. This library allows you to easily integrate AI models into your data processing pipelines, with the ability to dynamically change prompts and configurations without modifying your main codebase.

Primarily aimed to help handle tabular data and make some data preparations more efficient

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Customization](#customization)
  - [Prompts](#prompts)
  - [Configurations](#configurations)
- [Examples](#examples)
  - [Categorizing Text Data](#categorizing-text-data)
  - [Sentiment Analysis](#sentiment-analysis)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)
- [What Can Be Accomplished with This Library](#what-can-be-accomplished-with-this-library)
- [Future Plans](#future-plans)
- [Conclusion](#conclusion)

---

## Features

- **Dynamic Prompts**: Easily edit and switch between different prompts stored in separate files.
- **Multiple Configurations**: Maintain multiple model configurations for different use cases.
- **Modular Design**: Clean separation between models, functions, prompts, and configurations.
- **Easy Integration**: Simple API for integrating with pandas DataFrames and other data sources.
- **Progress Monitoring**: Built-in support for progress bars using `tqdm`.
- **Error Handling**: Robust error handling to ensure smooth processing.

---

## Installation

Install the library via `pip`:

```bash
pip install AIDSTK
```

Or install from source:

```bash
git clone https://github.com/yourusername/AIDSTK.git
cd AIDSTK
pip install -e .
```

---

## Quick Start

Here's a quick example of how to use the library in your project:

```python
import pandas as pd
from AIDSTK.models import initialize_model
from AIDSTK.functions import process_dataframe

# Initialize the model with the desired configuration and prompt
ollama_model = initialize_model('config1.json', 'prompt1.txt')

# Load your data
df = pd.read_csv('your_data.csv')

# Process the dataframe
processed_df = process_dataframe(df, 'text_column_name', ollama_model)

# Save or use the processed dataframe
processed_df.to_csv('processed_data.csv', index=False)
```

---

## Customization

### Prompts

Prompts are stored in the `AIDSTK/prompts/` directory. You can edit existing prompts or add new ones.

**Example: Creating a new prompt**

1. **Create a new file** in the `prompts` directory, e.g., `prompt2.txt`.

   ```text
   # AIDSTK/prompts/prompt2.txt
   Analyze the sentiment of the following text and classify it as 'positive', 'negative', or 'neutral'.
   Provide the result in JSON format.

   Example:

   Input: "I love sunny days."
   Output: {"sentiment": "positive"}
   ```

2. **Use the new prompt** in your code:

   ```python
   ollama_model = initialize_model('config1.json', 'prompt2.txt')
   ```

### Configurations

Configurations are stored in the `AIDSTK/configs/` directory in JSON format. They define model parameters and settings.

**Example: Creating a new configuration**

1. **Create a new file** in the `configs` directory, e.g., `config2.json`.

   ```json
   {
       "base_url": "http://192.168.0.73:11434",
       "model": "sentiment-analyzer",
       "temperature": 0.7,
       "metadata": {"seed": 123},
       "format": "json"
   }
   ```

2. **Use the new configuration** in your code:

   ```python
   ollama_model = initialize_model('config2.json', 'prompt2.txt')
   ```

---

## Examples

### Categorizing Text Data

```python
import pandas as pd
from AIDSTK.models import initialize_model
from AIDSTK.functions import process_dataframe

# Initialize the model
ollama_model = initialize_model('config1.json', 'prompt1.txt')

# Load your data
df = pd.read_csv('text_data.csv')

# Process the data
processed_df = process_dataframe(df, 'text_column', ollama_model)

# View the results
print(processed_df[['text_column', 'ai_category', 'ai_subcategory']].head())
```

### Sentiment Analysis

```python
import pandas as pd
from AIDSTK.models import initialize_model
from AIDSTK.functions import process_dataframe

# Initialize the model with sentiment analysis configuration
ollama_model = initialize_model('config2.json', 'prompt2.txt')

# Load your data
df = pd.read_csv('customer_reviews.csv')

# Process the data
processed_df = process_dataframe(df, 'review_text', ollama_model)

# View the results
print(processed_df[['review_text', 'sentiment']].head())
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**: `git checkout -b feature/your-feature-name`.
3. **Commit your changes**: `git commit -am 'Add new feature'`.
4. **Push to the branch**: `git push origin feature/your-feature-name`.
5. **Submit a pull request**.

Please ensure all new code follows the existing style and includes appropriate tests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you have any questions or need help, feel free to open an issue on the GitHub repository or contact me directly at [your-email@example.com](mailto:your-email@example.com).

---

## Acknowledgments

- [LangChain Community](https://github.com/hwchase17/langchain)
- [Pandas](https://pandas.pydata.org/)
- [Tqdm](https://tqdm.github.io/)

---

## What Can Be Accomplished with This Library

This library simplifies the integration of AI models into your data processing workflows. With it, you can:

- **Perform Text Classification**: Categorize text data into predefined categories and subcategories.
- **Sentiment Analysis**: Analyze and classify the sentiment of text data.
- **Custom AI Tasks**: Define your own prompts and configurations to perform various AI tasks such as summarization, translation, and more.
- **Batch Processing**: Efficiently process large datasets with progress tracking.
- **Experimentation**: Quickly switch between different models, prompts, and configurations to experiment and find the best setup for your use case.

---

## Future Plans

- **Expand Model Support**: Include support for more AI models and backends.
- **Add More Examples**: Provide more sample prompts and configurations.
- **Improve Documentation**: Enhance the documentation with detailed guides and tutorials.
- **Community Contributions**: Encourage community involvement to add new features and improvements.

---

## Conclusion

By leveraging this library, you can streamline the incorporation of AI functionalities into your projects, making it easier to process and analyze text data. Whether you're performing classification, sentiment analysis, or experimenting with custom AI tasks, this library provides a flexible and modular foundation to build upon.

---

*Happy Coding!*

---

```
