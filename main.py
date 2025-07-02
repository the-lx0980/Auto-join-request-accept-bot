import os
import logging
from pyrogram import Client, filters

# === Load Config from Environment ===
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7766441913:AAHvsqouFU932Tm7qff7We6wAY4qrQWNx10")
CHAT_ID = int(os.environ.get("CHAT_ID", "-1002585868566"))

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# === Create the Bot Client ===
app = Client("join_request_bot", bot_token=BOT_TOKEN)

@app.on_chat_join_request(filters.chat(CHAT_ID))
async def approve_join_request(client, join_request):
    """
    Auto-approve new join requests and log user info.
    """
    user = join_request.from_user
    try:
        await join_request.approve()
        name_parts = [user.first_name or ""]
        if user.last_name:
            name_parts.append(user.last_name)
        user_name = " ".join(name_parts).strip()
        if user.username:
            user_name += f" (@{user.username})"
        logging.info(f"✅ Approved: {user.id} - {user_name}")
    except Exception as e:
        logging.error(f"❌ Error approving {user.id}: {e}")

async def main():
    await app.start()
    logging.info("🚀 Bot started. Approving existing join requests...")

    try:
        success = await app.approve_all_chat_join_requests(CHAT_ID)
        if success:
            logging.info("✅ Approved all pending join requests.")
        else:
            logging.info("ℹ️ No pending join requests found.")
    except Exception as e:
        logging.error(f"❌ Error in bulk approval: {e}")

    logging.info("👂 Bot is now running...")
    await app.idle()
    await app.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
