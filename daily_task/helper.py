def clean(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

def create_html_body(summary):
    body = f"""
    <tr>
        <tr><td style="font-style: italic; font-weight: bold; padding-bottom: 20px">{summary["Title"]}</td></tr>
        <tr>
            <tr><td style="padding-left: 30px">Summary:</td></tr>
            <tr><td style="padding-bottom: 20px; padding-left: 30px;">{summary["Short Summary"]}</td></tr>
        </tr>
        <tr><td style="color: lightblue; padding-bottom: 10px"><a href="http://127.0.0.1:5000/summary/{summary['_id']}" style="color: #1a73e8;">Read Full Summary</a></td></tr>
        <tr><td><a href={summary["url"]}>Source</a></td></tr>
    </tr>
    """
    return body

def create_html_message(html_body, user_categories):
    categories = ""
    for category in user_categories:
        categories += f" {category},"
    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Email</title>
        </head>
        <body style="background-color: white;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;">
                <tbody>
                    <tr>
                        <td align="center">
                            <table role="presentation" max-width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #252626; padding: 20px; border-radius: 6px; font-family: Arial, sans-serif; color: white;">
                                <thead>
                                    <tr>
                                        <td align="center" style="padding-bottom: 10px;">Newsly</td>
                                    </tr>
                                    <tr>
                                        <td style="padding-bottom: 50px;">Here is your daily dose of{categories} news, summarized by AI so you don't have to waste time</td>
                                    </tr>
                                </thead>
                                <tbody>
                                    {html_body}
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """
    return html_message
