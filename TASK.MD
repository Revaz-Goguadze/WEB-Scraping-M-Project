Python Web Scraping
Midterm Project
Group Project Guidelines & Requirements
March 30, 2025
Python Web Scraping Midterm Project
Contents
1 Project Overview 3
1.1 Project Description . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
2 Project Requirements 3
2.1 Data Collection (5 points) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
2.2 Data Parsing (5 points) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
2.3 Object-Oriented Design (4 points) . . . . . . . . . . . . . . . . . . . . . . . . . . 3
2.4 Data Storage & Processing (3 points) . . . . . . . . . . . . . . . . . . . . . . . . 4
2.5 Project Structure & Documentation (3 points) . . . . . . . . . . . . . . . . . . . 4
3 Recommended Websites for Scraping 4
4 Collaboration Requirements 4
5 Deliverables 5
6 Submission Instructions 5
7 Grading Criteria 6
8 Bonus Points (up to 2 extra points) 6
9 Example Project Structure 7
10 Tips for Success 7
11 GitHub Repository Requirements 8
11.1 Repository Setup and Organization . . . . . . . . . . . . . . . . . . . . . . . . . . 8
11.1.1 Initial Setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
11.1.2 Branch Structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
11.2 Required GitHub Features to Use . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
11.2.1 Issue Tracking . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
11.2.2 Pull Requests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
11.2.3 Documentation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
11.3 Commit Guidelines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
12 Continuous Project Guidelines (Midterm to Final) 10
12.1 Continuous Project Benefits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
12.2 Required Enhancements for Final Extension . . . . . . . . . . . . . . . . . . . . . 10
12.2.1 1. Advanced Data Processing Extensions . . . . . . . . . . . . . . . . . . 10
12.2.2 2. Architecture & Performance Extensions . . . . . . . . . . . . . . . . . . 10
12.2.3 3. User Interface Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . 10
12.2.4 4. Extended Scraping Capabilities . . . . . . . . . . . . . . . . . . . . . . 10
12.2.5 5. Deployment & Production Extensions . . . . . . . . . . . . . . . . . . . 11
12.3 Documentation Requirements for Continuous Projects . . . . . . . . . . . . . . . 11
12.4 Evaluation Criteria for Continuous Projects . . . . . . . . . . . . . . . . . . . . . 11
12.5 Declaring Continuous Project Intention . . . . . . . . . . . . . . . . . . . . . . . 11
2
Python Web Scraping Midterm Project
1 Project Overview
In this midterm project, students will apply their knowledge of Python programming and web
scraping to create a data collection and analysis application. This project integrates key concepts
covered in the course including Python basics, object-oriented programming, HTTP fundamentals, and BeautifulSoup4 techniques.
Students will work in groups of 2-3 people and must use GitHub for collaboration and version
control. This project can be extended as a continuous project from midterm to final exam, with
appropriate scope adjustments.
Total Points: 20
1.1 Project Description
Students will create a web scraping application that collects data from a publicly available
website, processes the information, saves it to files, and performs basic analysis on the collected
data.
2 Project Requirements
2.1 Data Collection (5 points)
• Create a scraper that targets a publicly accessible website (options provided below) X
• Implement proper HTTP requests with appropriate headers X
• Handle potential request errors and exceptions X
• Implement rate limiting to prevent overwhelming the target website X
• Document the website’s robots.txt policies and ensure compliance X
2.2 Data Parsing (5 points)
• Use BeautifulSoup4 to parse the HTML content X
• Implement at least three different selection methods to extract data X
• Navigate the DOM tree to extract nested information X
• Extract at least four different types of data (text, links, attributes, etc.) X
• Implement error handling for missing elements X
2.3 Object-Oriented Design (4 points)
• Create at least two classes that model the data being collected X
• Implement appropriate constructors, properties, and methods X
• Follow proper OOP principles (encapsulation, abstraction) X
• Include appropriate documentation (docstrings, comments) X
3
Python Web Scraping Midterm Project
2.4 Data Storage & Processing (3 points)
• Save the collected data to files (CSV, JSON, or both) X
• Implement file operation error handling X
• Create a function to load and process the saved data X
• Perform at least two types of analysis or transformations on the data X
2.5 Project Structure & Documentation (3 points)
• Organize code into appropriate modules X
• Include a requirements.txt file X
• Write a comprehensive README.md with setup and usage instructions X
• Include comments explaining complex code sections X
• Document any limitations or potential improvements X
3 Recommended Websites for Scraping
The following are suggestions for websites that explicitly allow scraping or have public APIs.
Students are encouraged to explore other options or propose different websites that better suit
their project goals, as long as they comply with ethical scraping practices.
1. Books to Scrape (http://books.toscrape.com/) - A sandbox website specifically designed
for learning web scraping
2. Open Library (https://openlibrary.org/) - Public domain book information
3. Quotes to Scrape (http://quotes.toscrape.com/) - Another practice website for scraping
4. Wikipedia (with respect to their robots.txt)
5. GitHub Public Repositories (using their API)
Note: Always check the website’s Terms of Service and robots.txt before scraping. If you
choose a different website, get instructor approval first to ensure it’s appropriate for the
project.
4 Collaboration Requirements
• Work in groups of 2-3 students X
• Create a shared GitHub repository for your project X
• Use GitHub features (Issues, Pull Requests, Projects) to manage your work X
• Each team member must make meaningful contributions (visible in commit history) X
• Maintain a CONTRIBUTIONS.md file documenting each member’s specific contributions X
• All team members will receive the same grade unless there is clear evidence of unequal participation X
4
Python Web Scraping Midterm Project
5 Deliverables
1. Complete Python project with all required files in a GitHub repository X
2. CSV and/or JSON output files containing scraped data X
3. README.md file with comprehensive documentation X
4. CONTRIBUTIONS.md file detailing each team member’s contributions X
5. A brief report (500-700 words) describing:
• The website chosen and why X
• Implementation challenges and solutions X
• Analysis of the collected data X
• Potential improvements or extensions X
6. Evidence of using GitHub features (Issues, Pull Requests, etc.) X
7. Tagged release for midterm submission (”midterm-submission”) X
6 Submission Instructions
• Submit the URL of your GitHub repository via the course Teams channel by 10-11th of April,
2025
• Ensure the repository is public or shared with the instructor’s GitHub account
• Tag the midterm submission in your repository with the tag ”midterm-submission” X
• Include a README.md with setup instructions and project description X
• Ensure all dependencies are listed in requirements.txt X
5
Python Web Scraping Midterm Project
7 Grading Criteria
Component Excellent (Full
Points)
Satisfactory (Partial Points)
Needs Improvement (Minimal
Points)
Data Collection Successfully retrieves
data with error handling and rate limiting
Retrieves data but
with limited error
handling
Minimal functionality,
frequent errors
Data Parsing Effectively uses multiple BeautifulSoup
methods to extract
various data types
Basic parsing with
limited selection
methods
Incomplete parsing
with errors
OOP Design Well-structured
classes following OOP
principles with proper
documentation
Basic class implementation with some documentation
Poor structure, minimal OOP concepts
Data Storage Properly saves and
loads data with error
handling and performs
analysis
Saves data but with
limited processing capabilities
Minimal storage functionality
Project Structure Well-organized files,
comprehensive documentation
Basic organization and
documentation
Poor organization,
minimal documentation
Table 1: Grading Rubric for Midterm Project
8 Bonus Points (up to 2 extra points)
• Implement multithreading or asynchronous requests for improved performance
• Create a simple GUI using Tkinter to display the collected data
• Implement data visualization using matplotlib or another library
• Add unit tests for your main functions
6
Python Web Scraping Midterm Project
9 Example Project Structure
Below is a recommended structure for your project:
Project Directory Structure
project/
|-- main.py # Application entry point
|-- scraper/ # Web scraping modules
| |-- __init__.py
| |-- collector.py # HTTP requests handling
| |-- parser.py # HTML parsing utilities
|-- models/ # Data models
| |-- __init__.py
| |-- data_models.py # Object representations of data
|-- utils/ # Utility functions
| |-- __init__.py
| |-- file_handler.py # File operations
| |-- analyzer.py # Data analysis tools
|-- data/ # Directory for output files
| |-- (scraped data files)
|-- requirements.txt # Project dependencies
|-- README.md # Project documentation
10 Tips for Success
• Start by planning your application structure before coding
• Begin with a small subset of data to test your parsing logic
• Incrementally add features after ensuring core functionality works
• Test your code frequently with different inputs
• Document your code as you write it
• Use proper error handling throughout
• Respect website terms and implement ethical scraping practices
7
Python Web Scraping Midterm Project
11 GitHub Repository Requirements
11.1 Repository Setup and Organization
11.1.1 Initial Setup
1. Create a new public GitHub repository with a descriptive name related to your project
2. Add all team members as collaborators with appropriate permissions
3. Initialize with a README.md, .gitignore, and LICENSE file
• Use the Python .gitignore template X
• Choose an appropriate open-source license (MIT recommended)
11.1.2 Branch Structure
1. Main Branch (main) X
• Should always contain stable, working code X
• Protected from direct pushes (use Pull Requests) X
2. Development Branch (dev) X
• Primary branch for development X
• Merge to main only when features are complete and tested X
3. Feature Branches X
• Create branches for individual features or components X
• Name format: feature/feature-name or feature/github-username/feature-name X
11.2 Required GitHub Features to Use
11.2.1 Issue Tracking
1. Create issues for all features and tasks
• Use descriptive titles X
• Include acceptance criteria X
• Assign to specific team members X
• Add appropriate labels X
2. Use GitHub Project board to organize issues
• Set up columns for: To Do, In Progress, Review, Done X
• Track progress visually X
8
Python Web Scraping Midterm Project
11.2.2 Pull Requests
1. Create Pull Requests for all code changes
• Link to related issues X
• Provide detailed descriptions X
• Request reviews from team members X
2. Code Review Process
• At least one review required before merging X
• Address review comments X
• Resolve any merge conflicts X
11.2.3 Documentation
1. README.md
• Project description X
• Installation instructions X
• Usage examples X
• Technologies used X
2. CONTRIBUTIONS.md
• List each team member X
• Detail specific contributions by each member X
• Link to PRs and issues handled by each member X
3. Code Comments and Documentation
• Include docstrings for all functions and classes X
• Add inline comments for complex logic X
11.3 Commit Guidelines
1. Commit Message Format
• Use descriptive commit messages X
• Format: [TYPE]: Brief description of changes X
• Types: FEAT, FIX, DOCS, STYLE, REFACTOR, TEST, CHORE X
2. Commit Frequency
• Commit small, logical changes X
• Avoid combining unrelated changes in one commit X
• Commit often to show progress X
3. Authorship
• Use your real name and course email in Git config X
• Do not commit as another team member X
9
Python Web Scraping Midterm Project














12 Continuous Project Guidelines (Midterm to Final)
If your group chooses to extend the midterm project into a continuous project for the final exam,
please follow these guidelines to ensure appropriate scope and evaluation.
12.1 Continuous Project Benefits
• Build on existing codebase rather than starting a new project
• Implement more complex features that may be too ambitious for the midterm alone
• Develop a more comprehensive portfolio-worthy project
• Demonstrate deeper mastery of Python and web scraping concepts
12.2 Required Enhancements for Final Extension
To qualify as a continuous project, your final submission must significantly enhance the midterm
project by implementing at least three of the following extensions:
12.2.1 1. Advanced Data Processing Extensions
• Implement data visualization using matplotlib, seaborn, or plotly
• Apply statistical analysis to the scraped data
• Create a recommendation system based on the collected data
• Implement machine learning techniques (e.g., clustering, classification)
12.2.2 2. Architecture & Performance Extensions
• Convert to a multithreaded or asynchronous architecture
• Implement a proper database (SQLite, MySQL, etc.) instead of file storage
• Create a caching system to minimize duplicate requests
• Apply design patterns (Factory, Observer, Strategy, etc.)
12.2.3 3. User Interface Extensions
• Develop a web interface using Flask or Django
• Create a desktop GUI using Tkinter, PyQt, or similar
• Implement interactive data visualization dashboards
• Add user authentication and personalization features
12.2.4 4. Extended Scraping Capabilities
• Expand to multiple websites with a unified data model
• Implement a full crawler that follows links to discover content
• Add scheduled scraping with automatic updates
• Handle complex authentication or session management
10
Python Web Scraping Midterm Project
12.2.5 5. Deployment & Production Extensions
• Deploy the application to a cloud service (Heroku, AWS, etc.)
• Implement containerization using Docker
• Create comprehensive test suites (unit tests, integration tests)
12.3 Documentation Requirements for Continuous Projects
If pursuing the continuous project option, you must provide:
1. A Project Evolution Document (800-1000 words) explaining:
• Original midterm project scope and accomplishments
• Rationale for chosen extensions
• Design decisions and architectural changes
• Challenges faced and solutions implemented
• Future work beyond the final project
2. A Technical Architecture Diagram showing:
• Major components of your system
• Data flow between components
• Changes from midterm to final architecture
3. An updated README.md with:
• Clear separation between midterm and final features
• Updated installation and usage instructions
• API documentation (if applicable)
12.4 Evaluation Criteria for Continuous Projects
The final project grade will consider both the midterm foundation and the final extensions:
• Midterm Foundation (40%): The quality of the original midterm project
• Technical Extensions (40%): Implementation quality of the chosen extensions
• Architecture & Design (10%): Overall system design and architecture
• Documentation (10%): Quality and completeness of documentation
12.5 Declaring Continuous Project Intention
If your group wishes to pursue the continuous project option:
1. Include a file named CONTINUOUS PROJECT.md in your midterm submission
2. Outline which extensions you plan to implement for the final
3. Provide a brief justification for each extension
4. Include a timeline for implementation
The instructor will review your plan and provide feedback on scope and feasibility.
11