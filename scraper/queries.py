from enums import ProblemType

LOGIN_IDENTIFIER = '[data-testid="log-in--identifier"]'
LOGIN_PASSWORD = '[data-testid="log-in--password"]'
LOGIN_BUTTON = '[type="submit"]'

TOUR_BUTTON = 'button:has-text("Skip Tour")'

PROBLEM_TYPE_QUERIES = {
    ProblemType.MCQ: 'legend:has-text("Select one answer")',
    ProblemType.CHOOSE_ALL: 'legend:has-text("Select all that apply")',     
    ProblemType.FITB: 'legend:has-text("Select options below")',
    ProblemType.INPUT: '.free-entry-input__input-v2',
}

def mcq_string(index : int):
    return f'[data-testid="mcq-option-{index}"]'