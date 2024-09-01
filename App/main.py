import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    # App Title and Description
    st.title("📧 Cold Mail Generator")
    st.markdown("""
    Welcome to the Cold Mail Generator! This tool helps you craft personalized cold emails 
    tailored to specific job postings. Enter a job posting URL, and let our AI do the rest.
    """)

    # User Input Section
    with st.sidebar:
        st.header("Input Details")
        url_input = st.text_input("Job Posting URL:", value="https://jobs.nike.com/job/R-33460",
                                  help="Enter the URL of the job posting you are interested in.")
        submit_button = st.button("Generate Email")

    # Display generated emails
    if submit_button:
        with st.spinner("Processing..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                # Load portfolio and extract jobs
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                # Display each generated email
                for job in jobs:
                    st.subheader(f"Email for {job.get('role', 'Unknown Role')}")
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')

            except Exception as e:
                st.error(f"An error occurred: {e}")


def main():
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)


if __name__ == "__main__":
    main()
