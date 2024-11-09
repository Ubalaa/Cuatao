async def process_user_request(update: Update, context: CallbackContext, username: str):
    chat_id = update.message.chat_id  # Lấy chat_id của người dùng
    current_time = datetime.now()  # Lấy thời gian hiện tại

    # Khởi tạo lại time check cho người dùng sau mỗi lần sử dụng
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    try:
        # Gọi hàm đồng bộ send_request để thực hiện truy vấn
        access = await asyncio.get_event_loop().run_in_executor(executor, send_request, 'https://tikfollowers.com/free-tiktok-followers', headers)

        if access is None or access.status_code != 200:
            await update.message.reply_text('❌ **Lỗi**: Không thể truy cập TikFollowers. Vui lòng thử lại sau!')
            return

        session = access.cookies.get('ci_session')
        if not session:
            await update.message.reply_text('❌ **Lỗi**: Không thể lấy session từ TikFollowers. Vui lòng thử lại sau!')
            return

        headers.update({'cookie': f'ci_session={session}'})
        token = access.text.split("csrf_token = '")[1].split("'")[0]

        # Gửi yêu cầu tăng follow
        data = f'{{"type":"follow","q":"@{username}","google_token":"t","token":"{token}"}}'
        search = await asyncio.get_event_loop().run_in_executor(executor, send_request, 'https://tikfollowers.com/api/free', headers, data, 'POST')

        if search and search.json().get('success', False):
            data_follow = search.json()['data']
            data = f'{{"google_token":"t","token":"{token}","data":"{data_follow}","type":"follow"}}'
            send_follow = await asyncio.get_event_loop().run_in_executor(executor, send_request, 'https://tikfollowers.com/api/free/send', headers, data, 'POST')

            if send_follow and send_follow.json().get('o') == 'Success!':
                await update.message.reply_text('✅ **Thành công!** \n\n'
                                               'Tăng Follow TikTok cho tài khoản của bạn đã thành công! 🎉')
            elif send_follow and send_follow.json().get('o') == 'Oops...':
                try:
                    thoigian = send_follow.json()['message'].split('You need to wait for a new transaction. : ')[1].split('.')[0]
                    phut = thoigian.split(' Minutes')[0]
                    giay = int(phut) * 60

                    # Thông báo cho người dùng và đợi
                    await update.message.reply_text(f'⏳ Bạn cần chờ {giay} giây nữa trước khi thực hiện lại lệnh. Hãy kiên nhẫn nhé!')
                    await asyncio.sleep(giay)
                    await update.message.reply_text('✅ **Hoàn thành!** Bạn có thể thực hiện lại lệnh bây giờ.')
                except Exception as e:
                    await update.message.reply_text('❌ **Lỗi**: Không thể tính toán thời gian chờ. Vui lòng thử lại!')
            else:
                await update.message.reply_text('❌ **Lỗi**: Đã xảy ra sự cố khi tăng follow. Vui lòng thử lại sau!')
        else:
            await update.message.reply_text('❌ **Lỗi**: Không thể lấy thông tin TikTok. Vui lòng thử lại sau.')

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text(f'❌ **Lỗi không xác định**: {str(e)}. Vui lòng thử lại sau.')

    # Reset lại thời gian cho người dùng sau khi xử lý xong lệnh
    # Điều này đảm bảo người dùng sẽ không phải đợi từ phiên trước
    # last_used_times[chat_id] = None  # Nếu bạn sử dụng last_used_times để theo dõi

# Hàm xử lý lệnh /fltt <username>
async def increase_follow(update: Update, context: CallbackContext):
    username = ' '.join(context.args)  # Lấy username từ tin nhắn của người dùng

    # Kiểm tra xem người dùng có nhập username không
    if not username:
        await update.message.reply_text('💡 **Hướng dẫn sử dụng**: \n\n'
                                       'Để tăng Follow TikTok, bạn cần nhập username TikTok. \n'
                                       'Ví dụ: `/fltt <username>`, trong đó `<username>` là tên người dùng TikTok bạn muốn tăng follow. \n\n'
                                       'Hãy thử lại và cung cấp username TikTok hợp lệ!')
        return