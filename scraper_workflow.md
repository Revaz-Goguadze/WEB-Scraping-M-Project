# Scraper Workflow

This document outlines the execution flow of the web scraper.

```plantuml
@startuml
actor User
participant Main
participant AsyncCollector
participant Parser
participant FileHandler
participant Analyzer
participant Logger

== Initialization ==
User -> Main: Start main.py
Main -> AsyncCollector: Instantiate AsyncCollector(base_url, delay)
note right: Optional: SyncCollector for sync mode
Main -> AsyncCollector: check_robots_txt()
AsyncCollector -> Logger: Log robots.txt fetch attempt
alt robots.txt fetch succeeds
    AsyncCollector -> AsyncCollector: Parse robots.txt
    AsyncCollector -> Logger: Document policies (disallowed paths, crawl-delay)
    alt Disallow: / present
        AsyncCollector -> Logger: Log "Scraping disallowed"
        AsyncCollector -> Main: return False
        Main -> User: Exit
    else Allowed
        AsyncCollector -> Main: return True
    end alt
else fetch fails
    AsyncCollector -> Logger: Log error
    AsyncCollector -> Main: return True (assume allowed)
end alt

== Main Page Processing ==
Main -> AsyncCollector: fetch(main_url)
alt fetch succeeds
    AsyncCollector -> Logger: Log fetch success
    AsyncCollector -> Main: return HTML
    Main -> Parser: Parse main page HTML
    alt parse succeeds
        Parser -> Main: return Book List (Title, Price, Rel URL, Availability)
    else parse fails
        Parser -> Logger: Log parse errors
        Parser -> Main: Exit
    end alt
else fetch fails
    AsyncCollector -> Logger: Log fetch error
    AsyncCollector -> Main: Exit
end alt

== Book Detail Processing Loop ==
loop for each book in Book List
    Main -> AsyncCollector: fetch(detail_url)
    alt fetch succeeds
        AsyncCollector -> Logger: Log fetch success
        AsyncCollector -> Main: return Detail HTML
        Main -> Parser: Parse detail page HTML
        alt parse succeeds
            Parser -> Main: return Category (from breadcrumbs)
            Main -> Main: Create Book Object (Title, Price, URL, Availability, Category)
            Main -> Main: Append to Master List
        else parse fails
            Parser -> Logger: Log parse error
            Parser -> Main: Set Category=Unknown
            Main -> Main: Create Book Object
            Main -> Main: Append to Master List
        end alt
    else fetch fails
        AsyncCollector -> Logger: Log fetch error
        AsyncCollector -> Main: Set Category=Unknown
        Main -> Main: Create Book Object
        Main -> Main: Append to Master List
    end alt
end loop

== Storage & Analysis ==
Main -> FileHandler: Save Master List to JSON
alt save succeeds
    FileHandler -> Logger: Log save success
else save fails
    FileHandler -> Logger: Log save error
end alt
Main -> FileHandler: Save Master List to CSV
alt save succeeds
    FileHandler -> Logger: Log save success
else save fails
    FileHandler -> Logger: Log save error
end alt
Main -> FileHandler: Load Books from JSON
alt load succeeds
    FileHandler -> Main: return Books
else load fails
    FileHandler -> Logger: Log load error
    FileHandler -> Main: return Empty List
end alt
Main -> Analyzer: Analyze Books (stats, trends)
Analyzer -> Main: return Analysis Results
Main -> User: Print Results
Main -> User: End

@enduml
```

**Key Modules Involved:**

*   `main.py`: Orchestrates the overall process, handles command-line arguments (sync/async).
*   `scraper/collector.py`: Handles synchronous HTTP requests, rate limiting, `robots.txt`.
*   `scraper/async_collector.py`: Handles asynchronous HTTP requests using `aiohttp`, rate limiting, `robots.txt`.
*   `scraper/parser.py`: Uses BeautifulSoup4 to parse HTML and extract specific data elements.
*   `models/data_models.py`: Defines the `Book` class structure.
*   `utils/file_handler.py`: Saves and loads `Book` objects to/from JSON and CSV files.
*   `utils/analyzer.py`: Provides functions to perform analysis on the list of `Book` objects.