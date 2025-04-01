from transformers import pipeline
import torch
class TextSummarizer:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=self.device)
    
    def summarize(self, text, max_length=130, min_length=30):
        # Split the text into chunks that the model can handle
        max_input_length = 1024  # BART model's maximum input length
        chunks = [text[i:i + max_input_length] for i in range(0, len(text), max_input_length)]
        
        # Summarize each chunk and combine the results
        summaries = [self.summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text'] for chunk in chunks]
        return " ".join(summaries)




'''


import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import spacy

# Load spaCy English tokenizer
nlp = spacy.load("en_core_web_sm")

class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def chunk_text(self, text, max_tokens=1024):  # Increased token limit
        """Splits text into chunks without cutting sentences abruptly."""
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]  # Extract sentences using spaCy
        
        #print("Debug - Tokenized Sentences:", sentences)  # Debugging Output
        
        chunks, current_chunk = [], []
        current_length = 0

        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence, add_special_tokens=False))
            if current_length + sentence_tokens > max_tokens:  # Avoid empty chunks
                chunks.append(" ".join(current_chunk))
                current_chunk, current_length = [], 0
            current_chunk.append(sentence)
            current_length += sentence_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        print("Debug - Chunks before summarization:", chunks)  # Debugging
        return chunks

    def summarize(self, text):
        """Summarize text dynamically based on input length."""
        if not text.strip():
            return "Input text is empty."

        chunks = self.chunk_text(text, max_tokens=1024)
        summaries = []

        for chunk in chunks:
            inputs = self.tokenizer(chunk, return_tensors="pt", truncation=True, max_length=1024).to(self.device)
            input_length = len(inputs["input_ids"][0])

            # Adjusting summary length dynamically with a cap
            #max_summary_length = min(250, max(80, int(input_length * 0.75)))  
            #min_summary_length = min(120, max(30, int(input_length * 0.25)))  
            #max_summary_length = min(400, max(150, int(input_length * 0.9)))  
            #min_summary_length = min(200, max(40, int(input_length * 0.1)))
            max_summary_length = min(600, max(300, int(input_length * 0.9)))  
            min_summary_length = min(400, max(150, int(input_length * 0.5)))  


            summary_ids = self.model.generate(
                inputs["input_ids"], 
                max_length=max_summary_length, 
                min_length=min_summary_length, 
                num_beams=5, 
                early_stopping=True,
                #do_sample=True,
                #top_p=0.95,
            )

            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            print("Debug - Generated Summary:", summary)  # Debugging
            summaries.append(summary)

        return " ".join(summaries)

'''


'''
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import spacy

nlp = spacy.load("en_core_web_sm")

class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def chunk_text(self, text, max_tokens=1024, overlap=20):
        doc = nlp(text)
        #sentences = [sent.text.strip() for sent in doc.sents]
        sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 1]

        chunks, current_chunk = [], []
        current_length = 0

        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence, add_special_tokens=False))
            if current_length + sentence_tokens > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = current_chunk[-overlap:]
                current_length = sum(len(self.tokenizer.encode(s, add_special_tokens=False)) for s in current_chunk)

            current_chunk.append(sentence)
            current_length += sentence_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def summarize(self, text):
        if not text.strip():
            return "Input text is empty."

        chunks = self.chunk_text(text)
        summaries = []

        for chunk in chunks:
            inputs = self.tokenizer(chunk, return_tensors="pt", truncation=True, max_length=1024, padding=True).to(self.device)
            input_length = len(inputs["input_ids"][0])

            if input_length <= 150:
                #min_summary_length = max(50, int(input_length * 0.5))
                #max_summary_length = min(120, int(input_length * 0.8))
                min_summary_length = min(50, max(10, int(input_length * 0.4)))
                max_summary_length = max(min_summary_length + 10, int(input_length * 0.8))

            elif input_length <= 300:
                min_summary_length = max(80, int(input_length * 0.4))
                max_summary_length = min(200, int(input_length * 0.75))
            elif input_length <= 600:
                min_summary_length = max(100, int(input_length * 0.35))
                max_summary_length = min(350, int(input_length * 0.7))
            else:
                min_summary_length = max(150, int(input_length * 0.3))
                max_summary_length = min(500, int(input_length * 0.65))

            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_summary_length,
                min_length=min_summary_length,
                num_beams=4,
                #do_sample=True,
                #top_p=0.92,
                early_stopping=True,
            )

            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

        return " ".join(summaries)


'''