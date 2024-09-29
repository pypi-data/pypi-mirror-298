# Data-Pipeline

## Motivation
Hate speech detection faces challenges due to the diverse manifestations of abusive language across different tasks and languages. There is no universal model, as existing solutions target specific phenomena like racial discrimination or abusive language individually. With the rise of foundation models, there is a growing need for a unified dataset that integrates various hate speech datasets to support a comprehensive solution. Additionally, the lack of multilingual data, especially for low-resource languages, further complicates model development. A flexible, scalable data processing pipeline is essential to address these challenges, streamline dataset integration, and support future model advancements in hate speech detection across languages and tasks.

## Dataset-to-SQLite Pipeline
The dataset-to-SQLite pipeline is composed of modular components, each responsible for a distinct phase of the data management workflow. This design ensures flexibility, maintainability, and ease of extension across stages like configuration, data insertion, validation, and querying.

`config` **Module**

The `config` module simplifies the process of importing data files (e.g., CSV, TSV) that may not match the target database schema. A configuration file is used to map source file columns to the correct database tables, ensuring smooth integration. This module is built on a base class with an inheritance structure, allowing easy adaptation for future schema changes without breaking compatibility with the validator.


`loader` **Module**

The `loader` module is responsible for validating, formatting, and loading datasets into the database. It operates in a structured, phase-based manner:

- **Validator**: Ensures the integrity of the incoming datasets by checking that all required files and columns (as specified in the configuration file) are present. This prevents incomplete or corrupted data from entering the pipeline.
- **Formatter**: Breaks down validated datasets into multiple dataframes, formatting them to match the target database schema. This step improves clarity and efficiency in the loading process.
- **Loader**: Manages the data insertion process, handling both single and multi-file datasets. It ensures data integrity by controlling commit and rollback operations on a per-dataset basis.


`database` **Module**

The `database` module manages schema setup and data querying to ensure smooth integration and retrieval:

- **Setup**: Creates all database tables in the correct order, maintaining foreign key constraints. It also offers a reset function to clear tables when needed, simplifying schema management.
- **Querying**: Provides two main interfaces—one for displaying dataset-text-label information (with optional source language details) and another for executing queries from external SQL files. Both include a `show_lines` parameter for previewing rows and support exporting query results to CSV or TSV files.

`utils` **Module**

The `utils` module includes a set of helpful tools for data analysis and selection during the dataset preparation phase:

- **Distribute Tool**: Analyzes the distribution of one column relative to another, helping users identify balanced or imbalanced data points, useful for dataset selection.
- **Fuzzysearch Tool**: Allows approximate matching within the dataset, helping locate relevant data, such as label definitions or metadata, without requiring exact queries.
- **Sampling Tool**: Provides three pre-configured sampling strategies to ensure balanced and representative data subsets for experimental setups.

# License
This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/Master-Project-Hate-Speech/Data-Pipeline/blob/main/LICENSE) file for details.