
# Cold Email Generator 📧

**Cold-EmailGen** is an automated tool designed to streamline the creation of cold emails. Utilizing AI and document loaders, this app simplifies the process of personalizing and generating effective email content for marketing, business outreach, and lead generation. It supports integration with advanced tools like LangChain, ChromaDB, and leverages Python's NLTK for efficient natural language processing.

## Key Features 🔑
- **Automated Cold Email Generation**: Generates personalized cold emails with a focus on your target audience.
- **Language Processing**: Integrated with NLTK to ensure effective and coherent email construction.
- **Web Scraping for Personalized Content**: Extracts relevant information from websites to enhance the email's personalization.
- **ChromaDB for Vector Search**: Leverages ChromaDB to enable fast and efficient vector search, making it easy to manage large databases of personalized email templates.
- **Streamlit Integration**: Easy-to-use front-end that allows users to interact with the tool locally and generate emails in real-time.

## Installation ⚙️
To get started with Cold-EmailGen, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/RexO77/Cold-EmailGen.git
    cd Cold-EmailGen
    ```

2. **Set up your environment**:
   Install the necessary dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. **Add your API keys**:
   - Create a `.env` file in the root directory.
   - Add your required API keys as follows:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

4. **Run the app locally**:
   Start the Streamlit app:
    ```bash
    streamlit run App/main.py
    ```

## How It Works ⚙️
- **Natural Language Processing**: Cold-EmailGen uses NLTK for breaking down complex text structures and identifying the most appropriate sentence patterns for business emails.
- **Personalization**: The tool uses LangChain to pull relevant data from websites, which can be used to personalize the content of the emails.
- **ChromaDB for Document Search**: Integrated with ChromaDB for fast, scalable vector-based search across email templates.

## Technologies Used 🛠️
- **LangChain**: Facilitates seamless document handling and content extraction.
- **ChromaDB**: Handles the efficient storage and retrieval of large data collections for vector searches.
- **NLTK**: For natural language processing and text analysis.
- **Streamlit**: Provides an intuitive web-based front-end for interacting with the tool.

## Future Improvements 🛠️
- **Deployment on Streamlit Cloud**: Although functional locally, future iterations will focus on seamless cloud deployment for broader accessibility.
- **Advanced Analytics**: Incorporating metrics and feedback loops for optimizing email content.

## Contributing 🤝
Contributions are welcome! Please create a pull request or open an issue for any bugs or feature requests.
