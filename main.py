from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from flask import Flask

import os
import re
import tiktoken
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/docx-to-markdown")
def docx_to_markdown():
    endpoint = "https://lawtrial2.cognitiveservices.azure.com/"
    key = "4a0d87861f424d4dab106baea200cc3b"
    sourcedir = "C:\\Users\\METE\\Desktop\\useful\\test_data\\docx"
    destdir = "C:\\Users\\METE\\Desktop\\useful\\test_data\\markdown"

    credential = AzureKeyCredential(key)
    document_intelligence_client = DocumentIntelligenceClient(endpoint, credential, api_version="2024-02-29-preview")

    for filename in os.listdir(sourcedir):
        if filename.endswith(".pdf"):
            f = open(sourcedir + '/' + filename, 'rb')
            poller = document_intelligence_client.begin_analyze_document("prebuilt-layout", analyze_request=f,
                                                                         locale="tr-TR",
                                                                         output_content_format="markdown",
                                                                         content_type="application/octet-stream")
            result: AnalyzeResult = poller.result()
            f.close()
            content = result.content

            content = re.sub('<!--.*?-->', '', content)
            content = content.split('===', 1)[1] if '===' in content else content
            content = content.replace('Top of Form', '')
            content = content.replace('Bottom of Form', '')
            content = content.strip()

            filename = filename[:-5]
            f = open(destdir + '/' + filename + '.md', 'w', encoding='utf-8')
            f.write(content)
            f.close()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


headers_to_split_on = [
    ('#', "H1"),
    ('##', "H2"),
    ('###', "H3"),
    ('####', "H4")
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=True)
recursive_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=4096, chunk_overlap=256)

sourcedir = "C:\\Users\\METE\\Desktop\\useful\\test_data\\markdown"
destdir = "C:\\Users\\METE\\Desktop\\useful\\test_data\\json"


@app.route("/chunking")
def chunking():
    for filename in os.listdir(sourcedir):
        if (filename.endswith('.md')):
            f = open(sourcedir + '/' + filename, 'r', encoding='utf-8')
            mdsource = f.read()
            f.close()

            filename = filename[:-3]
            title = filename.split(' ', 1)[1] if ' ' in filename else filename
            docs = markdown_splitter.split_text(mdsource)

            for i, doc in enumerate(docs):
                chunks = recursive_splitter.split_text(doc.page_content)
                for j, chunk in enumerate(chunks):

                    hierarchy = title
                    for key, value in doc.metadata.items():
                        hierarchy = hierarchy + " | " + value

                    chunk = hierarchy + "\n\n" + chunk
                    chunk_filename = filename + '' + str(i + 1) + '' + str(j + 1)
                    item_data = {
                        "id": chunk_filename,
                        "title": title,
                        "hierarchy": hierarchy,
                        "content": chunk
                    }

                    json_data = json.dumps(item_data, ensure_ascii=False)

                    with open(os.path.join(destdir, chunk_filename + '.json'), 'w', encoding='utf-8') as f:
                        f.write(json_data)

                    continue
                continue


