import os
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
import django


django_project_path = "/Users/romanbespalov/Dev/tg_bot/django_admin/"  # для локального запуска
# django_project_path = "/tg_bot_app"  # для Docker
sys.path.append(django_project_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_admin.settings")
django.setup()

load_dotenv()

from admin_panel.models import Clients


BOT_TOKEN = os.getenv('BOT_TOKEN_ENV')
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()
router = Router()

FAQ_DATA = {
    "Вопрос 1": "Ответ на вопрос 1.",
    "Вопрос 2": "Ответ на вопрос 2.",
    "Вопрос 3": "Ответ на вопрос 3.",
    "Вопрос 4": "Ответ на вопрос 4.",
}

CATALOG_CATEGORIES = ["Категория 1", "Категория 2", "Категория 3"]
CATALOG_UNDER_CATEGORIES_1 = ["Подкатегория 1.1", "Подкатегория 1.2", "Подкатегория 1.3"]
CATALOG_UNDER_CATEGORIES_2 = ["Подкатегория 2.1", "Подкатегория 2.2", "Подкатегория 2.3"]
CATALOG_UNDER_CATEGORIES_3 = ["Подкатегория 3.1", "Подкатегория 3.2", "Подкатегория 3.3"]

RESULTS_PER_PAGE = 3


@dp.message(Command("каталог"))
async def show_catalog(message: types.Message):
    """Показать каталог в формате инлайн кнопок с пагинацией."""
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Каталог", callback_data="catalog")
    )
    await message.answer(
        'Нажмите чтобы перейти в каталог товаров',
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(F.data == "catalog")
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for category in CATALOG_CATEGORIES:
        builder.add(types.InlineKeyboardButton(
            text=category, callback_data=f"catalog:{category}")
        )
    # await state.update_data(chosen_category=category)
    await callback.message.answer(
        'Категории товаров',
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(F.data.startswith("catalog:"))
async def under_catalog(callback: types.CallbackQuery, state: FSMContext):
    chosen_category = callback.data.split(":")[1]
    # print(await state.get_data())
    if chosen_category:
        subcategories = f'CATALOG_UNDER_CATEGORIES_{chosen_category[-1]}'
        filtered_subcategories = globals()[subcategories]

        builder = InlineKeyboardBuilder()
        for subcategory in filtered_subcategories:
            builder.row(types.InlineKeyboardButton(
                text=subcategory, callback_data=f"subcategory:{subcategory}")
            )
        await callback.message.answer(
            f'Подкатегории товаров для {chosen_category}',
            reply_markup=builder.as_markup(),
        )


@sync_to_async
def create_client(message):
    """Функция создания клиента в БД после команды '/start'."""
    user = message.from_user
    Clients.objects.get_or_create(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@dp.message(CommandStart())
async def check_subscription_group_channel(message: Message):
    """Функция проверки подписки на группу и канал."""
    try:
        await create_client(message)
    except Exception as e:
        print(f"An error occurred: {e}")
    try:
        user_id = message.from_user.id

        channel_id = '@tg_bot_2024'
        channel_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)

        group_id = '@group_for_bot_2024'
        group_member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)

        if channel_member.status == 'creator' and group_member.status == 'creator':
            await message.answer('Вы являетесь создателем группы и канала!')
        elif channel_member.status == 'member' and group_member.status == 'member':
            await message.answer('Вы являетесь участником группы и канала!')
    except Exception:
        await message.answer('Вы не являетесь участником группы и канала!')


@router.inline_query(F.query)
async def show_FAQ(inline_query: types.InlineQuery):
    """Функция для создания ответов на частозадаваемые вопросы
    в формате инлайн режима с автоматическим дополнением вопроса."""
    query = inline_query.query.lower()
    results = []
    i = -1
    for question, answer in FAQ_DATA.items():
        if query in question.lower():
            i += 1
            results.append(types.InlineQueryResultArticle(
                id=str(i),
                title=f'{question} - {answer}',
                input_message_content=types.InputTextMessageContent(message_text=answer)
            ))

    await inline_query.answer(results, is_personal=True)
    logging.info("Функция show_user_links была вызвана")


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
