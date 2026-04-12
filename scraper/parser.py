from playwright.sync_api import Browser, Page
from enums import ProblemType
from scraper import queries

import re
import time
import utils

def build_text_block(text: str) -> dict:
    return {"type": "text", "text": text}

def build_image_block(b64: str) -> dict:
    return {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}

def merge_blocks_to_text(blocks: list) -> str:
    text = " ".join(b["text"] for b in blocks if b.get("type") in ("text", "latex"))
    i = 0
    def _numbered(_):
        nonlocal i
        result = f"<BLANK{i}>"
        i += 1
        return result
    return re.sub(r"<BLANK>", _numbered, text)

def renumber_blanks(blocks: list) -> list:
    """Renumber <BLANKn> markers consecutively across multiple text blocks."""
    counter = 0
    result = []
    for block in blocks:
        if block.get("type") == "text":
            def _replace(_):
                nonlocal counter
                r = f"<BLANK{counter}>"
                counter += 1
                return r
            result.append(build_text_block(re.sub(r"<BLANK\d+>", _replace, block["text"])))
        else:
            result.append(block)
    return result


class Parser:
    page: Page
    browser: Browser

    def parse_question(self, problem_type) -> list:
        if problem_type in (ProblemType.MCQ, ProblemType.CHOOSE_ALL):
            return self.parse_mcq()
        elif problem_type == ProblemType.FITB:
            return self.parse_fitb()
        elif problem_type == ProblemType.INPUT:
            return self.parse_input()
        return []

    def parse_mcq(self):
        content = [build_text_block("|| Math question: ||")]
        self.append_parsed_question(content)
        content.append(build_text_block("|| Answer Choices: ||"))

        for i, option in enumerate(self.page.query_selector_all(queries.MCQ_OPTIONS_ALL)):
            content.append(build_text_block(f"[{i}]:"))

            option_text = option.query_selector(queries.PARAGRAPH)
            if option_text:
                content.append(build_text_block(self.extract_paragraph_content(option_text)))

            option_image = option.query_selector(queries.IMAGE_SUPPLEMENT_IMAGE)
            if option_image:
                src = option_image.get_attribute("src")
                content.append(build_image_block(utils.fetch_image_b64(src, self.browser)))

        return content

    def parse_fitb(self):
        content = [build_text_block("|| Math problem: ||")]
        self.append_parsed_question(content)
        para_blocks = [
            build_text_block(self.extract_paragraph_content(p))
            for p in self.page.query_selector_all(queries.FITB_INPUT_PARAGRAPH)
        ]
        content.extend(renumber_blanks(para_blocks))

        toggles = self.page.query_selector_all(queries.FITB_MENU_CONTAINER)
        for i, button in enumerate(toggles):
            content.append(build_text_block(f"|| BLANK {i} ||"))
            button.click()
            time.sleep(0.2)
            choices = button.query_selector_all(queries.FITB_MENU_ITEM)
            for j, choice in enumerate(choices):
                p = choice.query_selector(queries.PARAGRAPH) or choice
                content.append(build_text_block(f"CHOICE{j}: {self.extract_paragraph_content(p)}"))
            self.page.keyboard.press('Escape')
            time.sleep(0.1)

        return content

    def parse_input(self):
        content = [build_text_block("|| Math question: ||")]
        self.append_parsed_question(content)
        prompts = self.page.query_selector_all(queries.FREE_ENTRY_INPUT_PROMPT)
        for i, prompt in enumerate(prompts):
            content.append(build_text_block(f"INPUT {i}: {utils.clean_inner_text(prompt.inner_text())}"))
        return content

    def append_parsed_question(self, content: list):
        question = self.page.query_selector(queries.QUESTION_WRAPPER_BODY)
        if not question:
            return

        for el in question.query_selector_all(queries.QUESTION_CONTENT_SELECTOR):
            class_name = el.evaluate("el => el.className")
            if "paragraph" in class_name:
                content.append(build_text_block(self.extract_paragraph_content(el)))
            elif "markdown-table-wrapper" in class_name:
                content.append(build_text_block(self.extract_table_content(el)))
            elif "image-supplement__image" in class_name:
                src = el.get_attribute("src")
                content.append(build_image_block(utils.fetch_image_b64(src, self.browser)))

    def extract_table_content(self, wrapper_el) -> str:
        return self.page.evaluate("""
            (el) => {
                const table = el.querySelector('table');
                if (!table) return '';
                const rows = [];
                for (const row of table.querySelectorAll('tr')) {
                    const cells = Array.from(row.querySelectorAll('th, td')).map(cell => {
                        const mathScript = cell.querySelector('script[type="math/tex"]');
                        if (mathScript) return '$' + mathScript.textContent.trim() + '$';
                        return cell.textContent.trim();
                    });
                    rows.push('| ' + cells.join(' | ') + ' |');
                }
                return rows.join('\\n');
            }
        """, wrapper_el)

    def extract_paragraph_content(self, paragraph_element) -> str:
        blocks = self.page.evaluate("""
            (el) => {
                const result = [];
                for (const node of el.childNodes) {
                    if (node.nodeType === Node.TEXT_NODE) {
                        const t = node.textContent.trim();
                        if (t) result.push({type: 'text', text: t});
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.classList.contains('with-toggle__wrapper')) {
                            result.push({type: 'text', text: '<BLANK>'});
                        } else {
                            const mathScript = node.querySelector('script[type="math/tex"]');
                            if (mathScript) {
                                result.push({type: 'text', text: '$' + mathScript.textContent.trim() + '$'});
                            } else {
                                const t = node.textContent.trim();
                                if (t) result.push({type: 'text', text: t});
                            }
                        }
                    }
                }
                return result;
            }
        """, paragraph_element)
        return merge_blocks_to_text(blocks)
