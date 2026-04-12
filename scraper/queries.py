from enums import ProblemType

LOGIN_IDENTIFIER = '[data-testid="log-in--identifier"]'
LOGIN_PASSWORD = '[data-testid="log-in--password"]'
LOGIN_BUTTON = '[type="submit"]'

TOUR_BUTTON = 'button:has-text("Skip Tour")'

QUESTION_WRAPPER_BODY = '.question-wrapper__body'
PARAGRAPH = '.paragraph'
IMAGE_SUPPLEMENT_IMAGE = '.image-supplement__image'
FREE_ENTRY_INPUT_PROMPT = '.free-entry-input__prompt'

ALREADY_COMPLETED_TEXT = ':text("You achieved \\"Advanced\\" on this skill level!")'
JUST_COMPLETED_TEXT = ':text("You reached the highest level of Advanced for answering 4 of the last 5 correctly!")'

PROBLEM_TYPE_QUERIES = {
    ProblemType.MCQ: 'legend:has-text("Select one answer")',
    ProblemType.CHOOSE_ALL: 'legend:has-text("Select all that apply")',     
    ProblemType.FITB: 'legend:has-text("Select options below")',
    ProblemType.INPUT: '.free-entry-input__input-v2',
}

MCQ_OPTIONS_ALL = '[data-testid^="mcq-option-"]'
FITB_INPUT_PARAGRAPH = '.markdown-renderer-v2.fitb-input-area.fitb-input-area-dropdown .paragraph'
FITB_MENU_CONTAINER = '.o-menu.fitb-menu-container'
FITB_MENU_ITEM = '.o-menu__item'

FINISH_BUTTON = ':text("Finish")'

def mcq_string(index : int):
    return f'[data-testid="mcq-option-{index}"]'

INPUT_QUESTION_BOX = ".free-entry-input__input-v2"
SUBMIT_ANSWERS = ':text("Submit Answer")'


MOVE_ON_QUERIES = {
    "MOVE_ONA": ':text("Let\'s go")', # highest prior
    "MOVE_ONB": ':text("Review Skills")',
    "MOVE_ONC": ':text("Next Question")'
}