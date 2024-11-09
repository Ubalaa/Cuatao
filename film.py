
def format_movie_name(movie_name):
    slug = unidecode.unidecode(movie_name)
    slug = slug.lower()
    slug = slug.replace(" ", "-")
    slug = re.sub(r'[^-\w]', '', slug)
    return slug.strip()

async def film(update: Update, context: CallbackContext) -> None:
    if context.args:
        movie_name = " ".join(context.args)
        formatted_name = format_movie_name(movie_name)

        url = f"{BASE_URL}{formatted_name}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            movie_data = response.json()

            if not movie_data.get("status"):
                await update.message.reply_text("Không tìm thấy thông tin phim.")
                return

            movie_info = movie_data.get("movie", {})
            name = movie_info.get("name", 'Không có tên phim')
            time = movie_info.get("time", 'Không có thời gian')
            year = movie_info.get("year", 'Không có năm sản xuất')
            poster_url = movie_info.get("poster_url")

            episodes = movie_data.get("episodes", [])
            links_embed = []
            for episode in episodes:
                server_data = episode.get("server_data", [])
                if server_data:
                    for server in server_data:
                        link_embed = server.get("link_embed")
                        if link_embed:
                            links_embed.append(link_embed)

            movie_info_message = (
                f"🎬 Tên phim: {name}\n"
                f"🎭 Thời gian: {time}\n"
                f"🎥 Năm sản xuất: {year}\n"
            )

            if poster_url:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=poster_url, caption=movie_info_message)
            else:
                await update.message.reply_text(movie_info_message)

            if links_embed:
                if len(links_embed) == 1:
                    await update.message.reply_text(f"📺 Link phim: {links_embed[0]}")
                else:
                    for i in range(0, len(links_embed), 10):
                        batch_links = links_embed[i:i + 10]
                        links_embed_text = "\n".join([f"🌟Tập {j + 1 + i}: {link}" for j, link in enumerate(batch_links)])
                        await update.message.reply_text(f"📺 Link các tập:\n{links_embed_text}")

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Lỗi HTTP: {http_err}")
            await update.message.reply_text("Có lỗi xảy ra khi lấy thông tin phim.")
        except ValueError:
            await update.message.reply_text("Lỗi khi chuyển đổi phản hồi thành JSON.")
        except Exception as err:
            logging.error(f"Lỗi: {err}")
            await update.message.reply_text("Có lỗi xảy ra.")
    else:
        await update.message.reply_text("Vui lòng cung cấp tên phim bằng Tiếng Việt.\nVí dụ: /film venom kèo cuối")