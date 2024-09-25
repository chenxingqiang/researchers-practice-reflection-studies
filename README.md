# Researchers' Practice Reflection Studies

 <img src="./imgs/logo.svg" alt="logo"/>

This repository contains the research project "Reflective Practice as a Strategy for Early Career Academics: Addressing Challenges in the Chinese Higher Education System".

## Project Structure

```bash
.
├── 01-initial-assessment
├── 02-reflective-practice-implementation
├── 03-mid-point-evaluation
├── 04-continued-practice
├── 05-final-assessment
├── docx
├── imgs
└── src
|__ data

```

## Research Phases

1. **Initial Assessment** (01-initial-assessment)
   - Literature review
   - Research design finalization
   - Ethics approval preparation

2. **Reflective Practice Implementation** (02-reflective-practice-implementation)
   - Survey distribution
   - Data collection
   - Initial data analysis

3. **Mid-point Evaluation** (03-mid-point-evaluation)
   - Preliminary findings review
   - Methodology adjustment (if necessary)
   - Interim report preparation

4. **Continued Practice** (04-continued-practice)
   - In-depth interviews
   - Continued data collection
   - Ongoing analysis

5. **Final Assessment** (05-final-assessment)
   - Comprehensive data analysis
   - Final report writing
   - Preparation for publication

## Research Methodology

This study employs a mixed-methods approach, combining quantitative and qualitative research techniques:

1. **Quantitative Component**:
   - Online survey (n=150)
   - Statistical analysis using SPSS or R

2. **Qualitative Component**:
   - Semi-structured interviews (n=20)
   - Thematic analysis using NVivo

3. **Data Integration**:
   - Triangulation of quantitative and qualitative findings
   - Comprehensive interpretation and theory development

## Project Timeline

 <img src="./imgs/02/Proposed-Longitudinal-Study-Design.png" alt="Proposed Longitudinal Study Design"/>

   This Gantt chart provides a visual timeline of a longitudinal study focused on the implementation and evaluation of reflective practice. The study spans over two years and is divided into key phases that guide the progression of reflective practice in the research context.

1. **Questionnaire Pre-test** (Week 1-2)
   - Conduct pre-test with 5-10 target group members
   - Collect feedback and adjust questionnaire

2. **Ethics Review** (Week 3-4)
   - Prepare ethics application
   - Submit to university ethics committee
   - Obtain approval

3. **Data Collection** (Week 5-12)
   - Distribute online questionnaire
   - Monitor response rate
   - Conduct follow-up reminders

4. **In-depth Interviews** (Week 13-16)
   - Design semi-structured interview guide
   - Select 15-20 representative interviewees
   - Conduct one-on-one interviews

5. **Data Analysis** (Week 17-24)
   - Quantitative data analysis
   - Qualitative data analysis
   - Integrate findings

6. **Report Writing** (Week 25-32)
   - Update literature review
   - Describe methodology and analysis
   - Write results and discussion sections

7. **Peer Review and Revision** (Week 33-36)
   - Invite 2-3 peer experts to review
   - Revise based on feedback

8. **Publication Preparation** (Week 37-40)
   - Select target journal
   - Format paper according to journal requirements
   - Submit and respond to reviewer comments

## Key Components

- **Survey**: Located in `src/survey_results.csv`
- **Data Generation**: `src/gen_data.py`
- **Document Generation**: `src/gen_doc.py`
- **Data Visualization**: `src/plot_fig*.py` files
- **Images**: Various charts and diagrams in `imgs/02/`

## How to Use

1. Clone the repository:

```bash
git clone <https://github.com/chenxingqiang/researchers-practice-reflection-studies.git>

```
   
2. Navigate to the project directory:

```bash
   cd researchers-practice-reflection-studies
```

3. Install required dependencies:

```bash
   pip install -r requirements.txt
```

4. Run the data generation script:

```bash
   python src/gen_data.py
```

5. Generate documents:

```bash
   python src/gen_doc.py
```
6. Create visualizations:
```bash
   python src/plot_fig2.py
   python src/plot_fig3.py
   python src/plot_fig4.py

```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [List any acknowledgments here]
