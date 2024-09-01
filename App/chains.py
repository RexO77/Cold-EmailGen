import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("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"),
            model_name="llama-3.1-8b-instant"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {Your Name}, a highly skilled and motivated {your_job} actively seeking a new opportunity. 
            Your goal is to craft a persuasive cold email to the HR or hiring manager for the job mentioned above, 
            demonstrating your expertise, achievements, and passion for excellence in your field. 
            Highlight how your proven track record and unique skill set make you an exceptional fit for the role, and convey 
            your enthusiasm for contributing to the company's continued success. 
            If applicable, mention any relevant projects, accolades, or links that showcase your outstanding qualifications: {link_list}.
            Remember, your objective is to not only capture but also retain the interest of the HR or hiring manager.
            Avoid any preamble and get straight to the point.
            ### EMAIL (NO PREAMBLE):
            Dear Hiring Manager,

            I am writing to express my genuine interest in the {job_title} position at your esteemed company. As a {your_job} with extensive experience in {key_skills}, I have consistently delivered exceptional results, 
            driving success in every project I undertake. 

            Throughout my career, I have {mention_specific_achievements}, which has honed my ability to {relevant_action_or_skill}, a quality I am eager to bring to your team. What excites me most about this 
            opportunity is {reason_for_interest_in_company_or_role}. I am confident that my combination of skills in 
            {additional_skills} and my commitment to excellence will make a meaningful impact at your company. 

            I have attached my resume, which provides further details about my professional journey and 
            accomplishments. I would be thrilled to discuss how my expertise can align with your team’s objectives 
            and help drive the company's mission forward. 

            Thank you for considering my application. I look forward to the possibility of contributing to your 
            esteemed team. 

            Warm regards,
            {Your Name}
            """
        )

        # Create the chain with the LLM
        chain_email = prompt_email | self.llm

        # Provide all required variables
        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links,
            "Your Name": "Your Name",
            "job_title": "Job Title",
            "your_job": "Your Job",
            "key_skills": "Key Skills",
            "mention_specific_achievements": "Achievements",
            "relevant_action_or_skill": "Relevant Action/Skill",
            "reason_for_interest_in_company_or_role": "Reason for Interest",
            "additional_skills": "Additional Skills"
        })
        return res.content


if __name__ == "__main__":
    chain = Chain()
    job = {"title": "Software Engineer", "description": "Developing applications", "skills": ["Python", "Django"]}
    links = ["https://portfolio-link.com/project1", "https://portfolio-link.com/project2"]

    email_content = chain.write_mail(job, links)
    print(email_content)

