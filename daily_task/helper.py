def clean(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

def create_html_body(summary):
    if summary["categories"] == "Business":
        title_image = "https://i.imgur.com/0s8tLEW.png"
    elif summary["categories"] == "World Events":
        title_image = "https://i.imgur.com/mdV4s2Q.png"
    elif summary["categories"] == "Politics":
        title_image = "https://i.imgur.com/iPM88ah.png"
    body = f"""
    <tr>
        <tr><td><hr style="margin: 50px 0;"></td></tr>
        <tr><td style="font-style: italic; font-weight: bold; padding-bottom: 20px; font-size: 20px;"><img src={title_image} style="width: 21px; height: 21px;"> {summary["Title"]}</td></tr>
        <tr>
            <tr><td style="padding-left: 30px font-weight: bold;">Summary:</td></tr>
            <tr><td style="padding-bottom: 20px; padding-left: 30px;">{summary["Short Summary"]}</td></tr>
        </tr>
        <tr><td style="padding-bottom: 10px"><img src="https://i.imgur.com/fVOFo1g.png" style="width: 18px; height: 18px;"> <a href="https://www.new-sly.com/summary/{summary['_id']}" style="color: #db0000; font-weight: bold;">Read Full Summary</a></td></tr>
        <tr><td><img src="https://i.imgur.com/mq8SJSZ.png" style="width: 18px; height: 18px;"> <a href={summary["url"]} style="color: #db0000; font-weight: bold;">Source</a></td></tr>
    </tr>
    """
    return body

def create_html_message(html_body, user_categories, utc_yesterday):
    categories = ", ".join(user_categories)
    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Newsly Summaries</title>
        </head>
        <body>
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tbody>
                    <tr>
                        <td align="center" style="background-image: url(https://i.imgur.com/JxcELle.jpeg); background-color: #330805; background-size: cover; background-position: center; background-repeat: no-repeat; font-family: 'Segoe UI', sans-serif; color: white; font-size: 17px;">
                            <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="max-width: 827px; background-color: #212121; padding: 20px; border-radius: 6px;">
                                <thead>
                                    <tr>
                                        <td align="center" style="padding-bottom: 10px; color: #db0000; font-family: Tahoma, Verdana, sans-serif; font-size: 50px;">NEWSLY</td>
                                    </tr>
                                    <tr>
                                        <td style="padding-bottom: 15px;"><span style="font-weight: bold;">Subject</span>: <img src="https://i.imgur.com/kNrlHq3.png" alt="newspaper" style="width: 18px; height: 18px;"> Your AI-Simplified News - {utc_yesterday}</td>
                                    </tr>
                                    <tr>
                                        <td>Here is your daily dose of <span style="font-weight: bold;">{categories}</span> news, summarized by AI so you don't have to waste time</td>
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
