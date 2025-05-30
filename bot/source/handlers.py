from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.utils.markdown import hbold, hitalic, hcode
from aiogram.types import Message
from datetime import datetime
import logging
from api import HistDataClient
from enum import IntEnum

class MonthName(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __str__(self):
        names = {
            1: "января",
            2: "февраля",
            3: "марта",
            4: "апреля",
            5: "мая",
            6: "июня",
            7: "июля",
            8: "августа",
            9: "сентября",
            10: "октября",
            11: "ноября",
            12: "декабря",
        }
        return names[self.value]



router = Router()
data_client = HistDataClient("http://data-api:8000")

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "<b>Привет!</b>\n"
        "Я — бот-справочник по <b>Второй Мировой войне</b>.\n\n"
        "📌 <b>Команды:</b>\n"
        "• <code>/epics</code> — список доступных эпиков (ключевых этапов войны)\n"
        "• <code>/getepic &lt;epic_id&gt;</code> — подробности по выбранному эпику\n\n"
        "Пример: <code>/getepic battle_moscow</code>"
    )
    await message.answer(text)



@router.message(Command("epics"))
async def list_epics(message: Message):
    try:
        epics = await data_client.get_all_epics()
        if not epics:
            await message.answer("На данный момент никаких эпиков не добавлено")
            return

        text = (
            "<b>📜 Доступные исторические эпики:</b>\n\n"
            "Отправь команду <code>/getepic &lt;id&gt;</code>, чтобы получить подробности.\n\n"
        )
        text += "\n\n".join(
            f"🔹 <b>{e['title']}</b>\nТэг: <code>{e['epic_id']}</code>" for e in epics
        )
        await message.answer(text)
    except Exception as e:
        logging.error(str(e))
        await message.answer("Ошибка при получении данных.")



def format_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        year = dt.year
        month = dt.month
        day = dt.day

        return f"{day} {str(MonthName(month))} {year}"
    except Exception:
        return date_str



@router.message(Command("getepic"))
async def get_epic(message: Message, command: CommandObject):
    args = command.args
    if not args:
        await message.answer("Укажи ID эпика: /getepic <epic_id>")
        return

    epic_id = args.strip()
    try:
        title, description, dependencies, events = await data_client.get_epic_data(epic_id)

        text = f"<b>{title}</b>\n\n{description or 'Нет описания'}\n\n"

        if dependencies:
            text += "<b>Зависит от:</b>\n" + "\n\n".join(
                f"• {dep['title']} (<code>{dep['depends_on_epic_id']}</code>)\n<i>{dep.get('description') or 'Нет описания связи'}</i>"
                for dep in dependencies
            ) + "\n\n"

        if events:
            text += "<b>События:</b>\n" + "\n".join(
                f"📅 {format_date(e['date'])}: {e['text']}" for e in events
            )
        else:
            text += "Событий нет."

        await message.answer(text)
    except Exception as e:
        logging.error(str(e))
        await message.answer("Не удалось получить данные по эпику.")
