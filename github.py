# Hàm xử lý lệnh /github
async def get_github_info(update: Update, context: CallbackContext) -> None:
    try:
        # Lấy username từ lệnh nhập vào
        username = context.args[0]  # Lấy tham số sau /github
        
        # Gửi request đến API lấy thông tin GitHub
        api_url = f'https://azig.dev/github/info?username={username}'
        response = requests.get(api_url)
        data = response.json()

        # Định dạng thông tin GitHub và gửi lại cho người dùng
        info_message = (
            "<blockquote>╭─────────────⭓\n"
            f"│ 𝗜𝗗: {html.escape(str(data['id']))}\n"
            f"│ 𝗡𝗮𝗺𝗲: <a href=\"{html.escape(data['avatar_url'])}\">{html.escape(data['name'])}</a>\n"
            f"│ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {html.escape(data['login'])}\n"
            f"│ 𝗟𝗶𝗻𝗸: <a href=\"{html.escape(data['html_url'])}\">{html.escape(data['html_url'])}</a>\n"
            f"│ 𝗡𝗴𝗮̀𝘆 𝗧𝗮̣𝗼: {html.escape(data['gio_tao'])} || {html.escape(data['ngay_tao'])}\n"
            f"│ 𝗧𝗶𝗲̂̉𝘂 𝗦𝘂̛̉: {html.escape(data['bio'])}\n"
            f"│ 𝗗𝗶𝗮̣ 𝗖𝗵𝗶̉: {html.escape(data['location'])}\n"
            f"│ 𝗡𝗴𝘂̛𝗼̛̀𝗶 𝗧𝗵𝗲𝗼 𝗗𝗼̃𝗶: {data['followers']} followers\n"
            f"│ 𝗗𝗮𝗻𝗴 𝗧𝗵𝗲𝗼 𝗗𝗼̃𝗶: {data['following']} following\n"
            f"│ 𝗥𝗲𝗽𝗼𝘀𝗶𝘁𝗼𝗿𝗶𝗲𝘀: {data['public_repos']} repositories\n"
            "╰─────────────⭓</blockquote>"
        )

        # Gửi tin nhắn chứa thông tin GitHub cho người dùng
        await update.message.reply_text(info_message, parse_mode='HTML')

    except IndexError:
        await update.message.reply_text("Vui lòng nhập tên người dùng sau lệnh /github. Ví dụ: /github dungkon2002")
    except Exception as e:
        await update.message.reply_text(f"Lỗi: {e}")
