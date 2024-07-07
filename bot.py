import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageEnhance, ImageFilter

TOKEN = os.getenv("6787570953:AAGqZ8gqpyTlJgiVseZtmEzCSfdcfmqqsc8")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне фотографию, и я её шакалю!')

def shakal_image(image_path: str, output_path: str):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize((img.width // 4, img.height // 4), Image.NEAREST)
        img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
        img = ImageEnhance.Contrast(img).enhance(2)
        img = ImageEnhance.Sharpness(img).enhance(10)
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        img.save(output_path, "JPEG")

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('input.jpg')
    shakal_image('input.jpg', 'output.jpg')
    with open('output.jpg', 'rb') as f:
        update.message.reply_photo(photo=f)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
