from typing import List, Tuple, Optional
from typing import List, Tuple
import re

def check(string: str, pattern: str = "") -> bool:
    """
    Matches a string against a custom pattern where:
    - `*` matches any sequence of characters.
    - `~value~` matches sequences that do not contain `value`.
    - `**` is treated as a literal asterisk `*`.
    - `~~` is treated as a literal tilde `~`.

    :param pattern: The custom pattern string.
    :param string: The string to match against the pattern.
    :returns: True if the string matches the pattern, False otherwise.
    """
    # Replace '**' with placeholder '__LITERAL_ASTERISK__'
    pattern = pattern.replace('**', '__LITERAL_ASTERISK__')

    # Replace '~~' with placeholder '__LITERAL_TILDE__'
    pattern = pattern.replace('~~', '__LITERAL_TILDE__')

    # Get the ~value~ segments
    no_match_segments = re.findall(r'~([^~]+)~', pattern)

    # Build the negative lookahead prefix
    regex_prefix = ''
    for segment in no_match_segments:
        regex_prefix += r'(?!.*{})'.format(re.escape(segment))

    # Remove the ~value~ segments from the pattern
    pattern_no_neg = re.sub(r'~[^~]+~', '', pattern)

    # Escape special characters for regex except for * and our placeholders
    escaped_pattern = re.escape(pattern_no_neg)
    escaped_pattern = escaped_pattern.replace(r'\*', '*')
    # Corrected the replacement here
    escaped_pattern = escaped_pattern.replace('__LITERAL_ASTERISK__', r'[*]')
    escaped_pattern = escaped_pattern.replace('__LITERAL_TILDE__', r'~')

    # Replace '*' with '.*' to match any sequence of characters
    regex_pattern = escaped_pattern.replace('*', '.*')

    # Combine the regex prefix and the regex pattern
    regex_pattern = '^' + regex_prefix + regex_pattern + '$'

    return re.match(regex_pattern, string) is not None


def _parse_pattern(pattern: str) -> List[Tuple[str, Optional[str]]]:
    """
    Parses the pattern into parts.
    Returns a list of tuples where each tuple is:
    (type, content)
    - type: '*', '~', or '' (empty string for normal text)
    - content: None for '*', the content inside '~ ~', or the literal text
    """
    parts = []
    position = 0
    length = len(pattern)

    while position < length:
        if pattern[position:position+2] == '**':
            parts.append(('', '*'))  # Literal '*'
            position += 2
        elif pattern[position:position+2] == '~~':
            parts.append(('', '~'))  # Literal '~'
            position += 2
        elif pattern[position] == '*':
            parts.append(('*', None))
            position += 1
        elif pattern[position] == '~':
            end_pos = pattern.find('~', position + 1)
            if end_pos != -1:
                content = pattern[position + 1:end_pos]
                parts.append(('~', content))
                position = end_pos + 1
            else:
                # Unmatched '~', treat as literal '~'
                parts.append(('', '~'))
                position += 1
        else:
            # Accumulate literal text
            literal = ''
            while position < length and pattern[position] not in ('*', '~'):
                # Check for '**' and '~~' to prevent breaking literals
                if pattern[position:position+2] in ('**', '~~'):
                    break
                literal += pattern[position]
                position += 1
            if literal:
                parts.append(('', literal))

    return parts


def parse(string: str, pattern: str = "") -> Optional[List[Tuple[str, str, int, int]]]:
    """
    Matches the string against the pattern and returns a list of tuples:
    (type, substring, start_index, end_index)
    - type: '*', '~', or '' (empty string for normal text)
    - substring: the matched substring from the string
    - start_index: the starting index in the string (inclusive)
    - end_index: the ending index in the string (inclusive)
    If all parts match, a final tuple of (True, "", -1, -1) is added.
    """
    parts = _parse_pattern(pattern)

    # Build the regex pattern
    regex_parts = []
    for type_, content in parts:
        if type_ == '*':
            regex_parts.append('(.*?)')  # Non-greedy match of any characters
        else:
            # Escape the content for regex
            escaped_content = re.escape(content)
            regex_parts.append('({})'.format(escaped_content))

    regex_pattern = '^' + ''.join(regex_parts) + '$'
    regex = re.compile(regex_pattern)

    # Match the string
    match = regex.match(string)
    if not match:
        return []  # No match found

    result = []
    for i, (type_, _) in enumerate(parts):
        group_num = i + 1
        substring = match.group(group_num)
        start = match.start(group_num)
        end = match.end(group_num) - 1  # Adjust to inclusive end index
        result.append((type_, substring, start, end))

    return result


def parse_multiple(strings:list[str], pattern:str = ""):
    results = []
    for string in strings:
        results.append(parse(string, pattern))

    return results