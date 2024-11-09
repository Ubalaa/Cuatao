def get_headers():
    user_agent = UserAgent()
    headers = {
        "User-Agent": user_agent.random,
        "Accept-Language": random.choice([
            "en-US,en;q=0.9",
            "fr-FR,fr;q=0.9",
            "es-ES,es;q=0.9",
            "de-DE,de;q=0.9",
            "zh-CN,zh;q=0.9"
        ]),
        "Referer": 'https://soundcloud.com/',
        "Upgrade-Insecure-Requests": "1"
    }
    return headers

async def get_client_id():
    client_id_file = 'client_id.txt'
    if os.path.exists(client_id_file):
        with open(client_id_file, 'r') as file:
            return file.read().strip()

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get('https://soundcloud.com/', headers=get_headers())
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            script_tags = soup.find_all('script', {'crossorigin': True})
            urls = [tag.get('src') for tag in script_tags if tag.get('src') and tag.get('src').startswith('https')]
            if not urls:
                raise Exception('Không tìm thấy URL script')

            res = await client.get(urls[-1], headers=get_headers())
            res.raise_for_status()
            client_id = res.text.split(',client_id:"')[1].split('"')[0]

            with open(client_id_file, 'w') as file:
                file.write(client_id)

            return client_id
    except Exception as e:
        print(f"[LỖI] Không thể lấy client ID: {e}")
        return None

async def search_song(query):
    try:
        link_url = 'https://soundcloud.com'
        headers = get_headers()
        search_url = f'https://m.soundcloud.com/search?q={quote(query)}'
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url, headers=headers)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            url_pattern = re.compile(r'^/[^/]+/[^/]+$')
            for element in soup.select('div > ul > li > div'):
                a_tag = element.select_one('a')
                if a_tag and a_tag.has_attr('href'):
                    relative_url = a_tag['href']
                    if url_pattern.match(relative_url):
                        title = a_tag.get('aria-label', '')
                        url = link_url + relative_url
                        img_tag = element.select_one('img')
                        cover_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None
                        return url, title, cover_url
            return None, None, None
    except Exception as e:
        print(f"[LỖI] Lỗi khi tìm kiếm bài hát: {e}")
        return None, None, None

async def download(link):
    try:
        client_id = await get_client_id()
        if not client_id:
            return None
        headers = get_headers()
        api_url = f'https://api-v2.soundcloud.com/resolve?url={link}&client_id={client_id}'
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            progressive_url = next((t['url'] for t in data.get('media', {}).get('transcodings', []) if t['format']['protocol'] == 'progressive'), None)
            if not progressive_url:
                raise Exception('Không tìm thấy URL âm thanh')
            response = await client.get(f'{progressive_url}?client_id={client_id}&track_authorization={data.get("track_authorization")}', headers=headers)
            response.raise_for_status()
            return response.json().get('url')
    except Exception as e:
        print(f"[LỖI] Lỗi khi tải âm thanh: {e}")
        return None

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
async def handle_scl_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip().split()
    
    if len(message) < 2:
        return  # Không làm gì nếu không có tên bài hát.

    tenbaihat = ' '.join(message[1:])

    link, title, cover = await search_song(tenbaihat)
    if link:
        mp3_url = await download(link)
        if mp3_url:
            async with httpx.AsyncClient() as client:
                response = await client.get(mp3_url)
                safe_title = sanitize_filename(title)
                mp3_file_path = f"{safe_title}.mp3"
                with open(mp3_file_path, 'wb') as mp3_file:
                    mp3_file.write(response.content)

            with open(mp3_file_path, 'rb') as mp3_file:
                await update.message.reply_audio(audio=mp3_file, title=safe_title)

            os.remove(mp3_file_path)

            if cover:
                await update.message.reply_photo(photo=cover)
    else:
        return  # Không làm gì nếu không tìm thấy bài hát.
def in_tieu_de(tieu_de):
    print("\n" + "=" * len(tieu_de))
    print(tieu_de)
    print("=" * len(tieu_de) + "\n")
