import fitz  # PyMuPDF     pip install pymupdf
import os
import logging
from openai import OpenAI
from pydantic import BaseModel



# Setup logging
logging.basicConfig(level=logging.INFO)




class PDFGPT:
    
    def __init__(self, service_provider, openai_api_key):
        """
        Initializes the PDF-GPT instance with the specified service provider and OpenAI API key.

        Args:
            service_provider (str): The service provider to use. Acceptable values are "opeani" and "azure_openai".
            openai_api_key (str): The API key for accessing OpenAI services.
        """
        if service_provider not in ["opeani", "azure_openai"]:
            raise ValueError("Invalid service provider. Acceptable values are 'opeani' and 'azure_openai'.")
        self.service_provider = service_provider
        self.openai_api_key = openai_api_key
        self.openai_client = OpenAI(api_key=self.openai_api_key) 



    class OpenAIResponseFormatQAPair(BaseModel):
        question: str
        answer: str
        question_context: str
        answer_context: str

    class OpenAIResponseFormatQAPairSection(BaseModel):
        section_no: int
        section_name: str
        amount_of_QA_pairs_should_be_generated_for_this_section: int
        qa_pairs_generated_for_this_section: list['PDFGPT.OpenAIResponseFormatQAPair']
        
    class OpenAIResponseFormatQAPairsComprehensive(BaseModel):
        section_amount: int
        qa_pairs_sections_list: list['PDFGPT.OpenAIResponseFormatQAPairSection']
        

    class OpenAIResponseFormatIsTOC(BaseModel):
        steps: str
        execution_log_followying_steps: str
        final_answer: str
        yes_or_no: bool


    
    def extract_text_from_pdf(self, pdf_file_path):
        try:
            doc = fitz.open(pdf_file_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                
                # Write current page text into a txt
                with open(f"{pdf_file_path}/pdf-gpt-generated/page_{page_num + 1}.txt", 'w') as page_file:
                    page_file.write(page_text)
                                    
                text += page_text
            doc.close()
            return text
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")
            return ""
        
    
    def save_text_to_file(self, text, text_output_file):
        try:
            with open(text_output_file, 'w') as f:
                f.write(text)
        except Exception as e:
            logging.error(f"Error saving text to file: {e}")
            


    def extract_table_of_contents(self, file_path):
        # Open the PDF file
        pdf_document = fitz.open(file_path)
        
        # Get the table of contents (TOC)
        toc = pdf_document.get_toc()

        if toc:
            # Write current page text into a txt
            with open(toc_direct_file, 'w') as page_file:
                # Print or return the TOC        
                for entry in toc:
                    level, title, page_number = entry
                    string = f"Level: {level}, Title: {title}, Page: {page_number}"
                    print(string)
                    page_file.write(string)
        elif not toc:
            string = "No Direct Table of Contents found. Use DaYuan's algorithm."
            print(string)
            
            # List all files that match the pattern
            file_names = [f for f in os.listdir(folder_path) if f.startswith(f'{state}_DM.pdf_page_')]
            no_toc_counter_afterTOC = 0
            for i in range(1, len(file_names)+1):
                current_page_file_name = f"{file_path}_page_{i}.txt"
                print("\n\n------\npage file: ", current_page_file_name)
                # ALGORITHM:
                # check whether exist current_page_file_name
                # if exist, ask gpt whether this is table of content
                # if yes then record the content of this file and continue
                # if no then record counter for no. If no more than 3 times then I think we are not of 
                # table of contents.
                if os.path.exists(current_page_file_name):
                    with open(current_page_file_name, 'r') as file:
                        page_content = file.read()
                    system_prompt = "You are an AI expert of analyzing PDF file contents. For the question or task users ask you, you always firstly think of what are the steps to do it, then follow those steps and execuate one by one, then finally you provide the final answer."
                    user_prompt = f"Help me to judge whether the text contains a Table of Contents for an artichle, or is a part of Table of Contents. <text>{page_content}</text>"
                    is_toc__gpt_response = self._gpt_engine(system_prompt, user_prompt, "is_toc_or_not")
                    print("\nis_toc__gpt_response: ", is_toc__gpt_response)
                    if is_toc__gpt_response.yes_or_no:
                        with open(toc_generated_file, 'a') as toc_file:
                            toc_file.write(page_content)
                        no_toc_counter_afterTOC = 0
                        continue
                    else:
                        no_toc_counter_afterTOC += 1
                        if no_toc_counter_afterTOC >= 3:
                            break
        



    def _gpt_engine(self, system_prompt, user_input, task_type=""):

        # "gpt-4o-mini" # gpt4o-mini is now gpt-4o-mini-2024-07-18. $0.150 / 1M input tokens; $0.600 / 1M output tokens.
        # "gpt-4o" # gpt4o is now "gpt-4o-2024-08-06".  $2.50 / 1M input tokens; $10.00 / 1M output tokens.
        model = "gpt-4o-mini"
        
        prompt_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ] 
        
        if task_type == "gen_qa_pairs":
            completion = self.openai_client.beta.chat.completions.parse(
                model = model,
                messages = prompt_messages,
                temperature = 0.1,
                top_p = 0.5,
                response_format = PDFGPT.OpenAIResponseFormatQAPairsComprehensive,
            )
            print("\n\n\n gptEngine(gen_qa_pairs): GPT response:", completion.choices[0].message.parsed)
            return completion.choices[0].message.parsed
        elif task_type == "is_toc_or_not":
            completion = self.openai_client.beta.chat.completions.parse(
                model = model,
                messages = prompt_messages,
                temperature = 0.1,
                top_p = 0.5,
                response_format = PDFGPT.OpenAIResponseFormatIsTOC,
            )
            print("\n\n\n gptEngine(is_toc_or_not): GPT response:", completion.choices[0].message.parsed)
            return completion.choices[0].message.parsed
        completion = self.openai_client.chat.completions.create(
            model = model,
            messages = prompt_messages,
            temperature = 0.1,
            top_p = 0.5,
        )
        print("\n gptEngine(): GPT response:", completion.choices[0].message.content)
        return completion.choices[0].message.content
    
    
    def generate_question_answer_pairs(self, page_text):
        system_prompt = "You are an AI designed to assist users in generating question and answer pairs strictly from the text provided by the user. Do not incorporate any external information beyond what the user has provided. The generated question and answer pairs will be used to train beginners, so it is crucial to adhere to the rule of using only user-provided text when creating the pairs."
        user_input = f"How many sections can the following text be split to? For each section, how many question answer pairs should be generate to coover its main content? For each section, generate question and answer pairs based on the following text: <text>{page_text}</text>."
        return self._gpt_engine(system_prompt, user_input, "gen_qa_pairs")

