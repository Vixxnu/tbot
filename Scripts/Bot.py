from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler, JobQueue
from datetime import timedelta

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for new_user in update.message.new_chat_members:
        # Welcome message
        await update.message.reply_text(f"Hello, {new_user.first_name}, how are you?")

        # Define buttons
        keyboard = [
            [
                InlineKeyboardButton("JOIN SOCIALS", callback_data='join_socials')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message with buttons
        intro_message = await update.message.reply_text(
            "*******Welcome To Neurolov******* \n\n"
            "Neurolov is an innovative platform that connects AI developers, GPU providers, "
            "and users in a seamless manner for high-performance computing and AI model deployment. "
            "It is the world's first browser-based on-chain computing platform.",
            reply_markup=reply_markup
        )

        # Schedule message deletion after  minutes
        context.job_queue.run_once(delete_message, when=timedelta(minutes=1), data={
            'chat_id': intro_message.chat_id,
            'message_id': intro_message.message_id
        })

async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    """Function to delete a specific message."""
    job_data = context.job.data
    await context.bot.delete_message(chat_id=job_data['chat_id'], message_id=job_data['message_id'])

# Callback function to handle button presses
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    # Respond based on which button was pressed
    if query.data == 'join_socials':
        await query.edit_message_text(
            text="Official Neurolov Links: \n\n"
                 "Website: https://neurolov.ai \n\n"
                 "Wiki: https://wiki.neurolov.ai \n\n"
                 "Github: https://github.com/neuroIov \n\n"
                 "Twitter: https://twitter.com/neurolov \n\n"
                 "Reddit: https://reddit.com/r/Nlov \n\n"
                 "Discord: https://discord.gg/cyVmj2nnUq"
        )

def main():
    application = Application.builder().token("7747210473:AAENTt8_f3Ln2g3mhejo0e--Im1bdcpLE2Y").build()

    # Add handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
    