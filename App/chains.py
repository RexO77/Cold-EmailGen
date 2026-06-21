import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables from App/.env regardless of the working directory
# (so it works the same on macOS, Linux, and Windows, and whether launched from
# the project root or elsewhere).
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
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

    def write_mail(self, job, resume_context):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE RESUME (most relevant excerpts):
            {resume_context}

            ### INSTRUCTION:
            You are the candidate described in the resume excerpts above. Write a
            persuasive, concise cold email to the hiring manager applying for the job
            described above.

            Rules:
            - Ground EVERY claim about the candidate strictly in the resume excerpts.
              Do NOT invent employers, titles, achievements, metrics, or skills that
              are not present in the resume.
            - Connect the candidate's actual experience and skills to the specific
              requirements of the job.
            - If the resume states the candidate's name, sign off with it; otherwise
              sign off with "Best regards," and no name.
            - Keep it tight (around 150-200 words), professional, and free of clichés.
            - Return ONLY the email body. No preamble, no subject line, no commentary.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "resume_context": resume_context or "No resume context available.",
        })
        return res.content

    def assess_and_write(self, job, resume_text):
        """One call that does two honest jobs: judge whether the résumé actually
        fits the role, then draft the email. Returns a dict with the verdict,
        matched strengths, gaps, improvement suggestions, and the email."""
        prompt = PromptTemplate.from_template(
            """
            ### JOB POSTING:
            {job_description}

            ### CANDIDATE RÉSUMÉ (full text):
            {resume_text}

            ### INSTRUCTION:
            Act as a blunt but fair recruiter. First judge how well this résumé
            fits this specific job, then draft a cold email.

            Be honest above all:
            - If the candidate clearly lacks required experience or skills, say so
              plainly in `gaps` and reflect it in the `verdict`. Do not inflate.
            - Base every judgement only on what the résumé actually contains.

            The email rules (strict):
            - It is written BY the candidate TO the hiring manager, applying for
              this role. Never write it from the company's or a recruiter's side.
            - Even for a weak fit, still write an applying email — lead with genuine
              transferable strengths, never invented experience, employers, or skills.
            - Body only: no subject line, no commentary.
            - Sign off with the candidate's name if the résumé states it; otherwise
              "Best regards," with no name. Never use a "[Your Name]" placeholder.

            Return ONLY valid JSON (no preamble, no markdown) with these keys:
            - "verdict": exactly one of "Strong fit", "Possible fit", "Stretch", "Not a fit"
            - "summary": one honest sentence on the fit
            - "strengths": array of short strings — where the résumé genuinely matches the role
            - "gaps": array of short strings — missing experience, skills, or qualifications (empty array if none)
            - "improve": array of short, actionable strings — what to add or do to become a stronger candidate
            - "email": the full cold email body as a single string

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm
        res = chain.invoke({
            "job_description": str(job),
            "resume_text": resume_text or "No résumé provided.",
        })
        try:
            return JsonOutputParser().parse(res.content)
        except OutputParserException:
            raise OutputParserException("Couldn't assess this role — the response wasn't valid.")


if __name__ == "__main__":
    chain = Chain()
    job = {"role": "Senior ML Engineer", "experience": "5+ years in ML",
           "skills": ["PyTorch", "MLOps"], "description": "Build and deploy ML models at scale."}
    resume_text = "Jane Doe — Frontend Engineer, 2 years building React apps. Skills: React, TypeScript, CSS."

    import json
    print(json.dumps(chain.assess_and_write(job, resume_text), indent=2))

