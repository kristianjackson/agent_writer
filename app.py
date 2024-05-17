import streamlit as st
import warnings
from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key

warnings.filterwarnings('ignore')

# Streamlit web app setup
st.title("White Paper Content Planning and Writing")

# Input text box for topic
topic = st.text_area("Enter the topic for the white paper:", height=100)

if st.button("Generate White Paper"):
    if topic:
        openai_api_key = get_openai_api_key()
        os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

        planner = Agent(
            role="Content Planner",
            goal="Plan engaging and factually accurate content on {topic}",
            backstory="You are an experienced project manager at a CPA firm, specializing in coordinating and overseeing audit engagements. "
            "You're working on planning a white paper about the topic: {topic}. "
            "You collect information that helps the audience learn something and make informed decisions. "
            "Your expertise lies in ensuring that all aspects of a project are meticulously planned and executed. "
            "Your work is the basis for the Content Writer to write a comprehensive white paper on this topic. "
            "You draw upon your extensive experience in project management within a CPA firm to structure the outline and ensure it covers all necessary points. "
            "Your planning is thorough and strategic, aimed at facilitating the Content Writer in crafting an insightful and accurate white paper. "
            "You ensure that the outline aligns with the firm's standards and provides a clear direction for the writing process.",
            allow_delegation=False,
            verbose=True
        )

        writer = Agent(
            role="Content Writer",
            goal="Write an insightful and factually accurate white paper about the topic: {topic}",
            backstory="You are a seasoned CPA with extensive experience in responding to audits. "
            "You're working on writing a comprehensive white paper about the topic: {topic}. "
            "You base your writing on the work of the Content Planner, who provides an outline "
            "and relevant context about the topic. You follow the main objectives and "
            "direction of the outline, as provided by the Content Planner. "
            "You provide objective and impartial insights and back them with information "
            "provided by the Content Planner. You also draw upon your audit experience to "
            "add depth and practical examples to your writing. You acknowledge in your white paper "
            "when your statements are opinions as opposed to objective statements.",
            allow_delegation=False,
            verbose=True
        )

        editor = Agent(
            role="Editor",
            goal="Edit a given white paper to align with "
            "the writing style of the organization.",
            backstory="You are an editor who receives a white paper "
            "from the Content Writer. Your goal is to review the white paper "
            "to ensure that it follows best practices for professional writing, "
            "provides balanced viewpoints when offering opinions or assertions, "
            "and maintains a high level of factual accuracy. You also ensure that "
            "the white paper aligns with the firm's standards, avoids major controversial topics "
            "or opinions when possible, and effectively communicates the information provided by the Content Planner and Writer.",
            allow_delegation=False,
            verbose=True
        )

        plan = Task(
            description=(
                "1. Prioritize the latest trends, key players, "
                "and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering "
                "their interests and pain points.\n"
                "3. Develop a detailed content outline for the white paper, including "
                "an introduction, key points, and a conclusion.\n"
                "4. Identify and include relevant data, sources, and case studies.\n"
                "5. Incorporate SEO keywords where appropriate."
            ),
            expected_output="A comprehensive content plan document "
            "with an outline, audience analysis, "
            "SEO keywords, relevant data, sources, and case studies.",
            agent=planner
        )

        write = Task(
            description=(
                "1. Use the content plan to craft a comprehensive "
                "white paper on {topic}.\n"
                "2. Incorporate SEO keywords naturally where appropriate.\n"
                "3. Sections/Subtitles are properly named "
                "in an informative and engaging manner.\n"
                "4. Ensure the white paper is structured with a "
                "compelling introduction, detailed and insightful body sections, "
                "and a summarizing conclusion.\n"
                "5. Integrate relevant data, sources, and case studies to support key points.\n"
                "6. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
            ),
            expected_output="A well-written white paper "
            "in markdown format, ready for publication, "
            "with each section providing in-depth analysis and insights.",
            agent=writer
        )

        edit = Task(
            description=(
                "1. Proofread the given white paper for grammatical errors and alignment with the brand's voice.\n"
                "2. Ensure the white paper follows best practices for professional writing, including clarity, coherence, and proper citation of sources.\n"
                "3. Verify that all sections are well-organized and that headings/subheadings are informative and engaging.\n"
                "4. Check that the white paper provides balanced viewpoints and accurately presents data, sources, and case studies.\n"
                "5. Ensure the introduction is compelling, the body sections are detailed and insightful, and the conclusion effectively summarizes the key points.\n"
                "6. Remove any major controversial topics or opinions that are not aligned with the brand's standards."
            ),
            expected_output="A well-written white paper in markdown format, ready for publication, with each section providing in-depth analysis and insights.",
            agent=editor
        )

        revise = Task(
            description=(
                "1. Review the feedback provided by the editor on the initial draft of the white paper.\n"
                "2. Make necessary revisions to improve clarity, coherence, and overall quality.\n"
                "3. Ensure that all grammatical errors are corrected and that the white paper aligns with the brand's voice.\n"
                "4. Incorporate any additional data, sources, or case studies as suggested by the editor.\n"
                "5. Refine the introduction, body sections, and conclusion based on the feedback.\n"
                "6. Proofread the revised draft for any remaining issues."
            ),
            expected_output="A revised and improved white paper in markdown format, addressing all feedback and ready for final editing.",
            agent=writer
        )

        final_edit = Task(
            description=(
                "1. Conduct a final proofread of the revised white paper for any remaining grammatical errors and alignment with the brand's voice.\n"
                "2. Ensure that the white paper follows best practices for professional writing, including clarity, coherence, and proper citation of sources.\n"
                "3. Verify that all sections are well-organized and that headings/subheadings are informative and engaging.\n"
                "4. Check that the white paper provides balanced viewpoints and accurately presents data, sources, and case studies.\n"
                "5. Ensure the introduction is compelling, the body sections are detailed and insightful, and the conclusion effectively summarizes the key points.\n"
                "6. Confirm that all feedback from the initial edit has been adequately addressed."
            ),
            expected_output="A final, polished white paper in markdown format, ready for publication, with each section providing in-depth analysis and insights.",
            agent=editor
        )

        crew = Crew(
            agents=[planner, writer, editor],
            tasks=[plan, write, edit, revise, final_edit],
            verbose=2
        )

        result = crew.kickoff(inputs={"topic": topic})

        # Remove the prefix from the result
        result = result.replace("my best complete final answer to the task.\n\n```markdown\n", "").strip()

        # Display the output in a textbox
        st.text_area("Generated White Paper", result, height=400)
    else:
        st.warning("Please enter a topic for the white paper.")
