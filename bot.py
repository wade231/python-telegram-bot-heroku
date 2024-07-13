from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pymongo



# Define your bot token
bot_token = '6479457005:AAFHxurm8wONJj9XpBLz6259YAkGfiU22hg'

# MongoDB connection string
mongo_uri = 'mongodb+srv://wade2001:wade2001@cluster0.wkjofrl.mongodb.net/?retryWrites=true&w=majority'

# Create a MongoDB client and connect to your database
client = pymongo.MongoClient(mongo_uri)
db = client['Cluster0']  # Replace with your database name
collection = db['Telegram_files']  # Replace with your collection name

# Replace 'SPECIFIC_GROUP_CHAT_ID' with the chat_id of the specific group
SPECIFIC_GROUP_CHAT_ID = -1001232369957  # Replace with the actual chat_id

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot is running!")

def handle_message(update: Update, context: CallbackContext):
    if update.message and update.message.chat_id == SPECIFIC_GROUP_CHAT_ID:
        text = update.message.text.lower()
        words = text.split()
        reply_count = 0
        keyboard = []

        # Query your MongoDB collection for file data
        cursor = collection.find()
        for document in cursor:
            filename = document['file_name']
            file_id = document['_id']

            # Generate a unique start parameter (for example, using the file_id)
            start_parameter = str(file_id)

            url = f"https://t.me/pusthakalasahayaka_bot?start={start_parameter}"

            # Your keyword filtering logic
            file_words = filename.split()
            ignore_words = ["pdf", "book", "පොත", "poth", "පොත්", "potha"]
            file_words = [x.lower() for x in file_words if x.lower() not in ignore_words]
            for word in file_words:
                if word in words:
                    if reply_count < 30:
                        keyboard.append([InlineKeyboardButton(filename, url=url)])
                        reply_count += 1
                    else:
                        break
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Download කරන්න යට බට්න් එක ඔබන්න 👇:", reply_markup=reply_markup)

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
