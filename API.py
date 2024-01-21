from fastapi import FastAPI, Header, Depends, status, Response, Request, APIRouter, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import random
import json

from scraping.main import scrape_list

async def not_found_error(request: Request, exc: HTTPException):
    return TEMPLATE.TemplateResponse(
        "error.html",
        {
            "request": request,
        }
    )

exception_handlers = {404: not_found_error}
app = FastAPI(exception_handlers=exception_handlers)

app.mount("/static", StaticFiles(directory="static"), name="static")
BASE_PATH = Path(__file__).resolve().parent
TEMPLATE = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# Infrastructure
# @app.get("/favicon.ico")
# async def get_favicon():
#     return FileResponse("static/assets/favicon.ico")

# index
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return TEMPLATE.TemplateResponse(
        "index.html",
        {
            "request": request,
        }
    )


def get_feedback(urls):
    return_str = [{'Navigation': [4,
   "The website features a clear top navigation bar with key sections labeled such as 'Main Page', 'Talk', 'Read', etc., aiding in straightforward navigation through core areas of the site. A search bar prominently placed at the center-top of the page is a well-established design practice that assists users in quickly finding the information they need. However, the sheer amount of links visible on the main page might overwhelm new users and potentially hinder navigation due to choice overload. Reducing the number of visible links or categorizing them more distinctly could improve navigation."],
  'Aesthetics': [3,
   'The interface employs a minimalistic and functional aesthetic which is in keeping with the encyclopedic nature of the site. The use of neutral colors and limited graphics prevents distractions while reading. However, the layout appears somewhat dated and could benefit from a more contemporary design approach that uses whitespace more effectively to separate content sections visually. Typography could also be updated for better readability and visual appeal.'],
  'Usability': [4,
   "The website is usable with clear text, a legible font size, and a logical layout that puts content at the forefront. Users can easily identify different sections like 'From today's featured article', 'In the news', etc., which are indicative of a user-centric approach to information architecture. On the downside, the depth of information available might make it harder for less experienced users to distinguish between primary and secondary content. Improving content hierarchy further could enhance usability."],
  'Consistency': [5,
   'The user interface displays strong consistency in design elements, such as color schemes, typographic choices, and button styles. This helps create a familiar environment for users, allowing for more predictable interactions and reducing cognitive load. Each section uses similar formatting for headings and links, maintaining a cohesive experience. This level of consistency contributes positively to both the usability and aesthetics of the site.']},
 {'Navigation': [2,
   "The UI provides a title 'Main Page,' which suggests a starting point for navigation. However, elements that would typically aid navigation, such as a menu or search function, are not visible in the screenshot. To improve, consider including clear navigational aids like a menu bar, breadcrumbs, or a search bar."],
  'Aesthetics': [2,
   'The UI presents a minimalistic design with a lot of white space, which can be visually appealing. However, the design lacks elements that could enhance the visual interest, such as images, color, or distinctive typography. Improving the aesthetics could involve introducing a more developed color scheme and more engaging graphical elements.'],
  'Usability': [2,
   "With only the 'Main Page' text and a partial view of what appears to be a button or input field, it's difficult to fully assess usability. The page is likely simple to understand, but it's not clear what action a user should or could take next. Adding clear cues or instructions would enhance usability."],
  'Consistency': [3,
   "The limited elements shown in the screenshot appear consistent in design. The typography for the 'Main Page' is uniform, and margins are aligned. Yet, the lack of additional UI elements makes it challenging to thoroughly evaluate consistency. Introducing more elements will help to further evaluate this category."]},
 {'error': 'Unfortunately, there is not enough information in the provided screenshot to perform a comprehensive evaluation. The screenshot seems to be cropped or incomplete, and crucial elements of the user interface, such as the main navigation menu, content areas, and other context-required elements, are missing. This lack of information makes it impossible to accurately assess the UI based on the priority categories of Navigation, Aesthetics, Usability, and Consistency.\n\nTo give meaningful feedback, a more complete view of the user interface is necessary. If you can provide a full screenshot of the UI, I would be happy to evaluate it according to the mentioned categories.'}]
    return return_str

@app.post("/process_data", response_class=HTMLResponse)
async def index(request: Request):
    body = await request.json()
    random_list = [[{'score': random.randint(0, 10), 'message': "hi"} for _ in range(4)] for i in range(len(body['configurations']))]
    filepaths = scrape_list(body['url'], body['configurations'])
    analysis = get_feedback(filepaths)


    return json.dumps({'data': analysis})

