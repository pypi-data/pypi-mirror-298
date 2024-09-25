# Research summarizer
Leveraging LLMs for Research Synthesis

This package is designed to leverage the power of Large Language Models (LLMs) to summarize and synthesize research papers. It combines Natural Language Processing (NLP) techniques and LLMs to extract and summarize key sections from research papers. We provide two methods allowing users to either summarize the full article(s) from the Introduction onwards or start the summary from the methodology onwards. We used a **prompt engineering** technique where users can specify what they want to extract from the paper(s) and get the summary. This way, the summarizer can provide a high-level summary of the important findings and conclusions. This package also allows you to process multiple PDFs simultaneously, making it particularly useful for systematic literature reviews and research synthesis.


## Features

- **PDF Extraction:** Extract text content from PDF files.
- **Text Preprocessing:** Clean and preprocess the extracted text for better summarization.
- **Section Extraction:** Identify and extract specific sections from the research paper.
- **Text Summarization:** Generate high-level summaries of the extracted sections using Open source LLMs like Llama 3 and Open AI's GPT-4 model.
- It can batch process multiple research papers at once.
- So, users just need to upload a folder containing multiple research papers and the summarizer will process all the papers and return a summary of each paper.
- The summaries are saved to a folder on your machine.
- **Streamlit Interface:** A user-friendly web interface for uploading PDF files and displaying summaries. You can access the web app via this [link](https://sum-tool.streamlit.app/).


## Usage


### Installation

Install the `res-sum` package using pip:

```bash
pip install res-sum
```

If you prefer to use a virtual environment to avoid package conflict, you can set up a virtual environment

```bash
python -m venv venv
```

Then you can activate it:

On Mac:
```bash
source venv/bin/activate  
```

On Windows:
```bash
venv\Scripts\activate
```


###  Import and Setup
After installing, you need to import the required libraries and then initialize the "ResSum" class. You'd have to download necessary NLTK resources if you haven't already:

```bash
import os
import nltk
from res_sum.research_summarizer import ResSum

# Download NLTK 'punkt' tokenizer
nltk.download('punkt_tab')

# Initialize the ResSum class
summarizer = ResSum()
```

### Set Up API Keys
You need API keys to run LLMs or the embedding. Ensure you have your API keys set up as environment variables (recommended) or specify them directly:


Obtain an API key from [Groq](https://console.groq.com/keys).

obtain an API key from [Voyage AI](https://www.voyageai.com/).


Note that Groq gives free access to their models. For this package, we currently have two Llama models (8B and 70B). We intend to add more as more LLMs become openly and freely available. Although Groq access may be limited per token per day, our method works for most articles (short or long). The effectiveness of our approach was first tested on over 750 articles, and they were processed successfully. So, while we are confident the method works and you should not max out your tokens in a single request, processing VERY long books (like textbooks) is not encouraged. Also, Voyage AI has a free version, which should be enough for personal (non-commercial) usage. You can read more on their respective website above. You can also pass the API keys directly if you have other access to Llama models (aside from Groq).

Once you have your API keys, you can set them using the .env file (recommended) or specify directly.


```bash
# Get your API keys
GROQ_API_KEY = os.getenv("Your_Groq_API_key")
VOYAGEAI_API_key = os.getenv("Your_voyageai_API_key")
model_options = ["llama3-8b-8192", "llama3-70b-8192"]
```

### Specify Input and Output Directories
You need to define the directory containing your PDF files and the output directory where the summarized DOCX files will be saved:

If you have the PDFs on your computer, you can move to the next step and specify the folder as described below. Otherwise, read this part. If you have your documents in Google Drive, you can use our package [GDriveOps python package](https://pypi.org/project/GDriveOps/) to manage those files easily, This package will bulk download your PDFs and save them to your computer, You can then use the summarizer to get the summary of the PDFs and use the [GDriveOps python package](https://pypi.org/project/GDriveOps/) to back transfer to your GoogleDrive folder. 


To use [GDriveOps python package](https://pypi.org/project/GDriveOps/), you need to get your Google Drive API Credentials. To do that:

- Create a project on the (Google Cloud Console).

- Enable the Google Drive API.

- Create credentials (OAuth 2.0 Client IDs) and download the credentials.json file.

- Place the credentials.json file in the project directory. For a full instruction on this, see [GDriveOps python package](https://pypi.org/project/GDriveOps/)



```bash
# Directory containing PDF files
pdf_directory = 'pdf_files'

# Output directory for summaries
output_directory = 'summary_files'

# You can also create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)
```

### Define Your Prompt
You need to provide a prompt for the summarization model. Here’s an example of how to set it up:

```bash
# Your custom prompt for summarization
prompt = """
Summarize the main findings of this research paper, focusing on the ABC.
"""

```

### Summarize PDFs
Run the summarize_pdfs function to process the PDF files and generate summaries:

```bash
summarizer.summarize_pdfs(
    pdf_directory, 
    output_directory, 
    prompt, 
    GROQ_API_KEY, 
    VOYAGEAI_API_key, 
    chunk_size, 
    chunk_overlap, 
    similarity_threshold, 
    num_clusters, 
    start_section
)
```


### Parameters

`pdf_directory`: Path to the folder containing the PDF files you want to summarize.

`output_directory`: Path to the folder where the summarized DOCX files will be saved.

`prompt`: Your custom prompt for guiding the summarization.

`GROQ_API_KEY`: API key for Groq models.

`VOYAGEAI_API_key`: API key for VoyageAI embeddings.

`chunk_size`: The size (in characters) of each text chunk to process (default is 8000).

`chunk_overlap`: Overlap size between chunks to avoid missing important content (default is 500).

`similarity_threshold`: Threshold for filtering out redundant chunks (default is 0.8).

`num_clusters`: Number of clusters for KMeans clustering (default is 10). If the data structure indicates that this value isn't optimal, it will be adjusted.

`start_section`: Specify where to begin the summarization (e.g., "introduction" or "methodology").

### Notes

The output will be saved as DOCX files with filenames prefixed by "Summary-" in the output_directory.
The widget interface allows users to select a model and specify the start section ("introduction" or "methodology") interactively when running in a notebook environment.




## Acknowledgments

- This project uses the API key from Groq AI for text summarization and Voyage AI for embedding.
- So, I want to thank the Groq AI for providing free tier access to interact with their models.
- Thanks to the Google Drive API for providing the tools to interact with Google Drive.

## Issues

You can report any issue on our GitHub issue page [here](https://github.com/drhammed/res_sum/issues). If you would like additional functionality, please let us know. You can also submit a pull request if you'd like to contribute. Thanks!