# Animation function for the running dots
def animate_dots():
    messages = [
        "[+] Bot running.  ",
        "[+] Bot running.. ",
        "[+] Bot running...",
    ]
    for message in messages:
        print(f"\r{message}", end="", flush=True)
        time.sleep(0.08)


# Add line breaks
def add_line_breaks(text, line_length):
    line = ""
    lines = []
    sentences = text.split(". ")

    for sentence in sentences:
        line += " " + sentence

        # check if it should add line break.
        if len(line.split(" ")) >= line_length or sentence == sentences[-1]:
            lines.append(line)
            line = ""

    # returns new text with line breakes.
    return ". \n \n".join(lines)
